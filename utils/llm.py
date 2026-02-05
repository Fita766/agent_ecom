from langchain_ollama import OllamaLLM
from crewai.llms.base_llm import BaseLLM

from utils.config import settings


class CrewOllamaLLM(BaseLLM):
    """
    Petit adaptateur pour utiliser OllamaLLM (LangChain) avec CrewAI.
    CrewAI attend un objet avec une méthode .call(prompt, **kwargs).
    """

    model: str

    def call(self, prompt: str, **kwargs) -> str:
        """
        Méthode appelée par CrewAI pour obtenir une réponse du LLM.
        On catch toutes les erreurs et on renvoie toujours une string non vide
        pour éviter le fameux: 'Invalid response from LLM call - None or empty'.
        """
        try:
            llm = OllamaLLM(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=0.7,
                num_predict=8192,  # Augmenté pour les réponses longues (campagnes marketing)
                repeat_penalty=1.1,
                # timeout n'est pas un paramètre valide pour OllamaLLM, on le retire
            )
            
            # FIX: Si le prompt arrive sous forme de liste (possible avec certains agents CrewAI), on le convertit
            if isinstance(prompt, list):
                prompt = "\n".join([str(p) for p in prompt])
                
            # Ajouter une instruction explicite pour forcer une réponse
            enhanced_prompt = prompt + "\n\nIMPORTANT: You MUST provide a detailed response. Do not return empty or generic messages. Provide specific, actionable information based on the task requirements."
            
            result = llm.invoke(enhanced_prompt)
            
            # Vérifier si la réponse est vide ou générique
            if not result or result.strip() == "":
                # Réessayer avec un prompt plus court si le prompt original est trop long
                if len(prompt) > 4000:
                    # Extraire seulement les parties essentielles du prompt
                    lines = prompt.split('\n')
                    essential_parts = []
                    for line in lines:
                        if any(keyword in line.lower() for keyword in ['task', 'description', 'expected_output', 'important', 'critical', 'extract']):
                            essential_parts.append(line)
                    simplified_prompt = '\n'.join(essential_parts[:50])  # Prendre les 50 premières lignes essentielles
                    simplified_prompt += "\n\nIMPORTANT: Provide a detailed response with specific data. Do not return generic messages."
                    result = llm.invoke(simplified_prompt)
                    
                    if not result or result.strip() == "" or "Summary: Workflow completed" in result:
                        # Dernier recours : retourner un message d'erreur explicite
                        return f"ERROR: LLM returned empty response. Task may require more context or the prompt was too complex. Original prompt length: {len(prompt)} characters. Please check task description and context availability."
            
            # Vérifier si la réponse est le message générique (ce qui indique un problème)
            if result and "Summary: Workflow completed. All previous tasks executed successfully" in result:
                # Le LLM a peut-être retourné le message par défaut, réessayer
                retry_prompt = prompt + "\n\nCRITICAL: You must provide actual task output, not a generic summary. Extract data from context and provide specific results."
                retry_result = llm.invoke(retry_prompt)
                if retry_result and retry_result.strip() and "Summary: Workflow completed" not in retry_result:
                    return retry_result
            
            return result if result else "ERROR: Empty response from LLM. Please check Ollama connection and model availability."
            
        except Exception as e:
            # On renvoie l'erreur sous forme de texte au lieu de laisser planter CrewAI
            error_msg = f"ERROR in LLM call: {str(e)}. Type: {type(e).__name__}. Please check Ollama connection at {settings.OLLAMA_BASE_URL} with model {settings.OLLAMA_MODEL}."
            print(f"[LLM ERROR] {error_msg}")
            return error_msg


def get_ollama_llm() -> CrewOllamaLLM:
    """Retourne un LLM compatible CrewAI qui route vers ton Ollama local."""
    return CrewOllamaLLM(model="ollama-local")
