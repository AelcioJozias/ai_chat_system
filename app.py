import streamlit as st
from src.document_processor import DocumentProcessor
from src.knowledge_base import KnowledgeBase
from src.llm_chain import ChatSystem
import os
from dotenv import load_dotenv
import shutil

# Configuração inicial
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Inicializa os componentes
document_processor = DocumentProcessor()
chat_system = ChatSystem(api_key=GOOGLE_API_KEY)


# Configuração da sessão do Streamlit
def initialize_chat():
    """Reinicia o chat mantendo a base de conhecimento"""
    st.session_state.messages = []


def initialize_full():
    """Reinicia completamente, incluindo a base de conhecimento"""
    st.session_state.messages = []
    st.session_state.knowledge_loaded = False
    st.session_state.knowledge_base = KnowledgeBase()
    st.session_state.uploaded_files = []
    # Limpa a pasta de dados
    if os.path.exists("data"):
        shutil.rmtree("data")
    os.makedirs("data", exist_ok=True)


if "messages" not in st.session_state:
    initialize_full()

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Interface Streamlit
st.title("📚 Sistema de Respostas com IA Generativa")
st.write("Faça upload de arquivos PDF para criar sua base de conhecimento e converse com ela.")

# Sidebar para upload de arquivos
with st.sidebar:
    st.header("⚙️ Configurações")

    # Botão para limpar o chat
    if st.button("🧹 Limpar Chat", key="clear_chat"):
        initialize_chat()
        st.rerun()

    st.header("📂 Gerenciamento de Arquivos")

    # Upload de arquivos
    uploaded_files = st.file_uploader(
        "Carregue arquivos PDF",
        type=["pdf"],
        accept_multiple_files=True,
        help="Você pode selecionar múltiplos arquivos PDF"
    )

    # Lista de arquivos carregados com opção de remoção
    if st.session_state.uploaded_files:
        st.subheader("Arquivos Carregados")
        files_to_remove = []

        for file_name in st.session_state.uploaded_files:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(file_name)
            with col2:
                if st.button(f"❌", key=f"remove_{file_name}"):
                    files_to_remove.append(file_name)

        # Processa remoção de arquivos
        if files_to_remove:
            try:
                # Remove arquivos da lista
                st.session_state.uploaded_files = [
                    f for f in st.session_state.uploaded_files
                    if f not in files_to_remove
                ]

                # Remove arquivos do sistema de arquivos
                for file_name in files_to_remove:
                    file_path = f"data/{file_name}"
                    if os.path.exists(file_path):
                        os.remove(file_path)

                # Reconstrói a base de conhecimento se houver arquivos restantes
                if st.session_state.uploaded_files:
                    with st.spinner("Atualizando base de conhecimento..."):
                        all_texts = []
                        for file_name in st.session_state.uploaded_files:
                            file_path = f"data/{file_name}"
                            text = document_processor.extract_text_from_pdf(file_path)
                            cleaned_text = document_processor.clean_text(text)
                            chunks = document_processor.split_text(cleaned_text)
                            all_texts.extend(chunks)

                        st.session_state.knowledge_base.create_knowledge_base(all_texts)
                        st.session_state.knowledge_loaded = True
                        st.success("Base de conhecimento atualizada!")
                else:
                    st.session_state.knowledge_loaded = False
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "ℹ️ Todos os documentos foram removidos. Por favor, carregue novos arquivos PDF."
                    })

                st.rerun()
            except Exception as e:
                st.error(f"Erro ao remover arquivos: {str(e)}")

    process_button = st.button("Processar Documentos", key="process_button")

    if process_button:
        if uploaded_files:
            with st.spinner("Processando documentos..."):
                try:
                    all_texts = []
                    st.session_state.uploaded_files = []

                    for uploaded_file in uploaded_files:
                        # Salva o arquivo temporariamente
                        file_path = f"data/{uploaded_file.name}"
                        os.makedirs("data", exist_ok=True)

                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        st.session_state.uploaded_files.append(uploaded_file.name)

                        # Processa o PDF
                        text = document_processor.extract_text_from_pdf(file_path)
                        cleaned_text = document_processor.clean_text(text)
                        chunks = document_processor.split_text(cleaned_text)
                        all_texts.extend(chunks)

                    # Cria a base de conhecimento
                    if all_texts:
                        st.session_state.knowledge_base.create_knowledge_base(all_texts)
                        st.session_state.knowledge_loaded = True
                        st.success("Base de conhecimento criada com sucesso!")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "✅ Base de conhecimento pronta! Agora você pode fazer perguntas sobre os documentos."
                        })
                    else:
                        st.error("Nenhum texto válido foi extraído dos documentos.")

                except Exception as e:
                    st.error(f"Erro ao processar documentos: {str(e)}")
        else:
            st.warning("⚠️ Por favor, selecione pelo menos um arquivo PDF.")

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Faça sua pergunta sobre os documentos..."):
    # Adiciona a pergunta do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Exibe a pergunta do usuário
    with st.chat_message("user"):
        st.markdown(prompt)

    # Verifica se a base de conhecimento foi carregada
    if not st.session_state.knowledge_loaded:
        response = "📝 Por favor, carregue e processe seus documentos PDF primeiro. Use a barra lateral à esquerda para enviar seus arquivos e clique em 'Processar Documentos' para criar a base de conhecimento."
    else:
        with st.spinner("🔍 Buscando informações..."):
            try:
                # Busca documentos relevantes
                relevant_docs = st.session_state.knowledge_base.search_documents(prompt)

                # Gera a resposta
                response = chat_system.generate_response(prompt, relevant_docs)

            except Exception as e:
                response = f"⚠️ Ocorreu um erro ao processar sua pergunta: {str(e)}\n\nPor favor, verifique se os documentos foram carregados corretamente e tente novamente."

    # Adiciona a resposta ao histórico e exibe
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)