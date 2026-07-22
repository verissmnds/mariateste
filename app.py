# -*- coding: utf-8 -*-

import streamlit as st
import os
from content import INTRODUCAO_TEXT, SETORES

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Metodologia de Pesquisa - Plataforma Acadêmica",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para carregar o arquivo CSS customizado
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback caso o arquivo CSS não seja encontrado por algum motivo
        st.markdown("""
        <style>
        html, body, [class*="css"] { font-family: "Arial", sans-serif !important; }
        h1 { border-bottom: 2px solid #0284c7; padding-bottom: 10px; color: #0f172a; }
        blockquote { border-left: 5px solid #0284c7; padding-left: 20px; margin-left: 20px; }
        </style>
        """, unsafe_allow_html=True)

# Injetar o CSS customizado
load_css("styles.css")

# Inicializar o estado da página na sessão
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Apresentação"

# Função callback para alterar a página ao clicar nos botões dos cartões
def navigate_to(page_name):
    st.session_state.current_page = page_name

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("## 🎓 Metodologia")
    st.markdown("Plataforma Interativa de Metodologia de Pesquisa para Estudantes Universitários.")
    st.write("---")
    
    # Navegação por botões de rádio associados ao estado
    page_options = [
        "🏠 Apresentação",
        "🔍 Abordagem",
        "🧪 Natureza",
        "🎯 Objetivos",
        "📋 Procedimentos"
    ]
    
    # Encontrar o índice da página atual no vetor
    try:
        current_index = page_options.index(st.session_state.current_page)
    except ValueError:
        current_index = 0
        
    selected_page = st.radio(
        "Navegue pelos Setores:",
        options=page_options,
        index=current_index,
        key="navigation_radio"
    )
    
    # Sincronizar o estado da página com o botão de rádio
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()

    st.write("---")
    st.markdown("### 📌 Norma ABNT")
    st.markdown(
        """
        Esta plataforma utiliza:
        *   Fonte: **Arial**
        *   Alinhamento: **Justificado**
        *   Espaçamento de linha acadêmico
        *   Citações com recuo de **4cm**
        """
    )

# --- CORPO PRINCIPAL DO SITE ---

# Função auxiliar para renderizar o iframe de vídeo do YouTube de forma bonita e responsiva
def render_youtube_video(video_url):
    video_html = f"""
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1); margin: 20px 0;">
        <iframe src="{video_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
    """
    st.components.v1.html(video_html, height=450)

# Renderização do conteúdo conforme a página selecionada
if st.session_state.current_page == "🏠 Apresentação":
    st.title("Metodologia de Pesquisa Científica")
    st.markdown(INTRODUCAO_TEXT, unsafe_allow_html=True)
    
    st.markdown("### Conheça os Setores da Plataforma")
    st.write("Clique nas categorias abaixo para explorar as classificações teóricas de forma detalhada:")
    
    # Criar grade de cartões (Cards) interativos para os 4 setores principais
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class="category-card">
                <h3>🔍 Abordagem</h3>
                <p>Estude a diferença entre as formas de coletar e analisar dados em pesquisas acadêmicas.</p>
                <ul>
                    <li><b>Pesquisa Qualitativa</b></li>
                    <li><b>Pesquisa Quantitativa</b></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Explorar Abordagem", key="btn_abordagem", use_container_width=True):
            navigate_to("🔍 Abordagem")
            st.rerun()
            
    with col2:
        st.markdown(
            f"""
            <div class="category-card">
                <h3>🧪 Natureza</h3>
                <p>Compreenda a diferença entre a geração de teorias puras e a aplicação prática do conhecimento.</p>
                <ul>
                    <li><b>Pesquisa Básica</b></li>
                    <li><b>Pesquisa Aplicada</b></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Explorar Natureza", key="btn_natureza", use_container_width=True):
            navigate_to("🧪 Natureza")
            st.rerun()

    with col3:
        st.markdown(
            f"""
            <div class="category-card">
                <h3>🎯 Objetivos</h3>
                <p>Aprenda a classificar sua pesquisa quanto ao nível de profundidade e metas desejadas.</p>
                <ul>
                    <li><b>Pesquisa Exploratória</b></li>
                    <li><b>Pesquisa Descritiva</b></li>
                    <li><b>Pesquisa Explicativa</b></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Explorar Objetivos", key="btn_objetivos", use_container_width=True):
            navigate_to("🎯 Objetivos")
            st.rerun()

    with col4:
        st.markdown(
            f"""
            <div class="category-card">
                <h3>📋 Procedimentos</h3>
                <p>Descubra os delineamentos práticos e estratégias de campo para operacionalizar seu estudo.</p>
                <ul>
                    <li><b>Pesquisa Experimental, Bibliográfica, Documental</b></li>
                    <li><b>Pesquisa de Campo e Etnográfica</b></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Explorar Procedimentos", key="btn_procedimentos", use_container_width=True):
            navigate_to("📋 Procedimentos")
            st.rerun()

else:
    # Mapear o nome amigável da página para a chave no dicionário SETORES
    setor_key = st.session_state.current_page.split(" ")[1] # Extrai 'Abordagem', 'Natureza', etc.
    setor_data = SETORES[setor_key]
    
    st.title(setor_data["title"])
    st.markdown(f"*{setor_data['description']}*")
    st.write("---")
    
    # Criar abas horizontais (tabs) para cada sub-tópico do setor
    subtopicos_names = list(setor_data["subtopicos"].keys())
    subtopicos_tabs = st.tabs([f"🔹 {name}" for name in subtopicos_names])
    
    # Preencher cada sub-tópico com suas abas de Teoria, Vídeo e Estudo de Caso
    for idx, tab_el in enumerate(subtopicos_tabs):
        sub_name = subtopicos_names[idx]
        sub_data = setor_data["subtopicos"][sub_name]
        
        with tab_el:
            # Abas internas de conteúdo
            content_tabs = st.tabs(["📖 Conceito", "🎥 Recursos Visuais", "💼 Estudo de Caso"])
            
            with content_tabs[0]:
                st.markdown(sub_data["conceito"], unsafe_allow_html=True)
                
            with content_tabs[1]:
                st.subheader(f"Vídeo Explicativo: {sub_name}")
                render_youtube_video(sub_data["video_url"])
                st.info("💡 Dica: Assista ao vídeo acima para consolidar a base teórica antes de analisar o estudo de caso prático.")
                
            with content_tabs[2]:
                st.markdown(
                    f"""
                    <div class="case-study-box">
                        <div class="case-study-title">Estudo de Caso Prático</div>
                        {sub_data['estudo_caso']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# --- RODAPÉ ACADÊMICO ---
st.markdown(
    """
    <div class="footer-text">
        Plataforma Acadêmica de Metodologia de Pesquisa | Desenvolvido para auxílio pedagógico de estudantes universitários | © 2026
    </div>
    """,
    unsafe_allow_html=True
)
