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
                num_predict=2048,
                repeat_penalty=1.1,
            )
            result = llm.invoke(prompt)
            # Par sécurité, si jamais invoke renvoie None ou vide
            if not result:
                return "LLM returned an empty response to the prompt. Please try rephrasing or simplifying the request."
            return result
        except Exception as e:
            # On renvoie l'erreur sous forme de texte au lieu de laisser planter CrewAI
            return f"LLM error while processing prompt: {e}"


def get_ollama_llm() -> CrewOllamaLLM:
    """Retourne un LLM compatible CrewAI qui route vers ton Ollama local."""
    return CrewOllamaLLM(model="ollama-local")
