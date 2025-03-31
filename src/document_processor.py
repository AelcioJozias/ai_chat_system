import PyPDF2
from typing import List
import re

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extrai texto de um arquivo PDF."""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
        return text

    @staticmethod
    def clean_text(text: str) -> str:
        """Limpa e normaliza o texto."""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)  # Remove espaços múltiplos
        text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
        return text.strip()

    @staticmethod
    def split_text(text: str, chunk_size: int = 1000) -> List[str]:
        """Divide o texto em chunks menores."""
        words = text.split()
        chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        return chunks