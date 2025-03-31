from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List
import os


class ChatSystem:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.chain = self._initialize_chain()

    def _initialize_chain(self):
        """Inicializa a cadeia de prompts usando a nova sintaxe do LangChain."""
        template = """
        Você é um assistente útil que responde perguntas com base no contexto fornecido.

        Contexto:
        {context}

        Pergunta: {question}

        Resposta:"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

        llm = ChatGoogleGenerativeAI(
            google_api_key=self.api_key,
            model=self.model_name,
            temperature=0.7
        )

        return (
                {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
                | prompt
                | llm
        )

    def generate_response(self, question: str, context: List[str]) -> str:
        """Gera uma resposta com base na pergunta e no contexto."""
        if not context:
            return "Desculpe, não encontrei informações relevantes para responder sua pergunta."

        combined_context = "\n".join(context)
        response = self.chain.invoke({"context": combined_context, "question": question})
        return response.content