# 📚 Sistema de Respostas com IA Generativa

## ✨ Visão Geral
Sistema inteligente para análise e conversação com documentos PDF utilizando IA generativa, desenvolvido com:

- **Google Generative AI** (Gemini) para respostas inteligentes
- **LangChain** para orquestração de fluxos de IA
- **Streamlit** para interface web moderna

## 🚀 Funcionalidades

### 📤 Upload de Documentos
- Suporte a múltiplos PDFs simultâneos
- Pré-processamento automático do texto
- Extração e limpeza de conteúdo

### 💬 Chat Inteligente
- Histórico de conversação persistente
- Respostas baseadas no contexto dos documentos
- Visualização dos trechos mais relevantes

### ⚙️ Gerenciamento
- Remoção individual de documentos
- Limpeza seletiva do histórico
- Reinicialização completa do sistema

## 🛠️ Stack Tecnológica

| Componente         | Versão   | Descrição                                  |
|--------------------|----------|--------------------------------------------|
| Python             | 3.10+    | Linguagem base do sistema                  |
| Streamlit          | 1.32+    | Framework para interfaces web              |
| LangChain          | 0.1+     | Integração com modelos de LLM              |
| Google GenerativeAI| 0.0.11+  | Conexão com a API do Gemini                |
| PyPDF2             | 3.0+     | Processamento de arquivos PDF              |
| SentenceTransformers| 2.2+    | Geração de embeddings para busca semântica |

## 🚀 Começando

### Pré-requisitos
- Python 3.10 ou superior
- Conta no [Google AI Studio](https://ai.google.dev/)
- Chave de API válida do Gemini

### Instalação

1. **Clonar repositório**:
   ```bash
   git clone https://github.com/seu-usuario/ai-chat-system.git
   cd ai-chat-system
   
2. **Clonar repositório**:
   ```bash
   python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
   
3. **Clonar repositório**:
   ```bash
   pip install -r requirements.txt
   
4. Configurar variáveis de ambiente:
   Crie um arquivo .env com: GOOGLE_API_KEY=sua_chave_aqui
   
5. ### 🖥️Executando o Sistema:
   #### streamlit run app.py


# 🎮 Guia de Uso
### Carregar Documentos:

- Acesse a sidebar

- Selecione um ou mais arquivos PDF

- Clique em "Processar Documentos"

### Interagir com o Chat:

- Digite perguntas na caixa de mensagem

O sistema responderá com base nos documentos

### Gerenciamento:

- 🗑️ Remover arquivos individuais

- 🧹 Limpar histórico de conversa

- 🔄 Reiniciar completamente
