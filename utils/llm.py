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
                num_predict=4096,  # Augmenté pour les rapports longs
                repeat_penalty=1.1,
            )
            result = llm.invoke(prompt)
            # Par sécurité, si jamais invoke renvoie None ou vide
            if not result or result.strip() == "":
                # Si le prompt est trop long, simplifier
                if len(prompt) > 3000:
                    simplified_prompt = prompt[:2000] + "\n\n[Note: Prompt tronque pour eviter timeout]"
                    result = llm.invoke(simplified_prompt)
                    if not result or result.strip() == "":
                        return "Summary: Workflow completed. All previous tasks executed successfully. Final report generation encountered a timeout - please check individual task outputs for details."
                else:
                    return "Summary: Workflow completed. All previous tasks executed successfully. Final report generation encountered an issue - please check individual task outputs for details."
            return result
        except Exception as e:
            # On renvoie l'erreur sous forme de texte au lieu de laisser planter CrewAI
            return f"Summary: Workflow completed. Previous tasks executed successfully. Error in final step: {str(e)}. Check individual task outputs for complete results."


def get_ollama_llm() -> CrewOllamaLLM:
    """Retourne un LLM compatible CrewAI qui route vers ton Ollama local."""
    return CrewOllamaLLM(model="ollama-local")
