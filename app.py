# -*- coding: utf-8 -*-

import streamlit as st
import os
import csv
from datetime import datetime
import pandas as pd
import json
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
        st.markdown("""
        <style>
        html, body, [class*="css"] { font-family: "Arial", sans-serif !important; }
        h1 { border-bottom: 2px solid #0284c7; padding-bottom: 10px; color: #0f172a; }
        blockquote { border-left: 5px solid #0284c7; padding-left: 20px; margin-left: 20px; }
        </style>
        """, unsafe_allow_html=True)

# Injetar o CSS customizado
load_css("styles.css")

# --- CONEXÃO GOOGLE SHEETS / FALLBACK CSV ---

# Diretório para armazenamento local
DADOS_DIR = "dados"
os.makedirs(DADOS_DIR, exist_ok=True)

# Colunas do formulário
COLUNAS = [
    "Nome", "Turma", "Nome da Pesquisa", "Pergunta", 
    "Abordagem", "Natureza", "Procedimento", 
    "Quantidade de Dados", "Período", "Fontes", "Data de Envio"
]

def get_sheets_client():
    """Tenta autenticar com a API do Google Sheets usando Streamlit Secrets (suporta formato TOML e JSON)."""
    # Verificar se as secrets mínimas estão presentes
    has_toml = "gcp_service_account" in st.secrets and "spreadsheet_url" in st.secrets
    has_json = "gcp_service_account_json" in st.secrets and "spreadsheet_url" in st.secrets
    
    if not has_toml and not has_json:
        return None, None
        
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # 1. Tentar ler do formato JSON direto (mais seguro contra erros de formatação PEM)
        if has_json:
            creds_info = json.loads(st.secrets["gcp_service_account_json"])
        # 2. Fallback para o formato TOML estruturado
        else:
            creds_info = dict(st.secrets["gcp_service_account"])
            if "private_key" in creds_info:
                pk = creds_info["private_key"]
                if "\\n" in pk:
                    pk = pk.replace("\\n", "\n")
                creds_info["private_key"] = pk
                
        credentials = Credentials.from_service_account_info(creds_info, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(st.secrets["spreadsheet_url"])
        return client, sheet
    except Exception as e:
        # Gerar informações detalhadas para o diagnóstico na barra lateral
        pk_info = "Nenhuma credencial configurada"
        if has_json:
            pk_info = f"Formato: JSON bruto | Tamanho: {len(st.secrets['gcp_service_account_json'])} chars"
        elif has_toml and "private_key" in st.secrets["gcp_service_account"]:
            pk = st.secrets["gcp_service_account"]["private_key"]
            pk_info = (
                f"Formato: TOML estruturado | Tamanho: {len(pk)} chars | "
                f"Começa com BEGIN: {pk.startswith('-----BEGIN PRIVATE KEY-----')} | "
                f"Quebras de linha (\\n): {pk.count(chr(10))} | "
                f"Literais (\\\\n): {pk.count('\\\\n')}"
            )
        st.sidebar.warning(f"Erro ao conectar ao Google Sheets: {e}\n\n🔍 Diagnóstico da Chave:\n{pk_info}")
        return None, None

def salvar_resposta(dados):
    """Salva a resposta no Google Sheets. Caso falhe ou não esteja configurado, salva localmente em CSV."""
    procedimento = dados["Procedimento"]
    client, sheet = get_sheets_client()
    
    # Formatar dados para a linha
    linha = [
        dados["Nome"], dados["Turma"], dados["Nome da Pesquisa"], dados["Pergunta"],
        dados["Abordagem"], dados["Natureza"], dados["Procedimento"],
        dados["Quantidade de Dados"], dados["Período"], dados["Fontes"], dados["Data de Envio"]
    ]
    
    if sheet is not None:
        try:
            try:
                worksheet = sheet.worksheet(procedimento)
            except Exception:
                worksheet = sheet.add_worksheet(title=procedimento, rows="100", cols="15")
                worksheet.append_row(COLUNAS)
            
            worksheet.append_row(linha)
            return True, "Google Sheets"
        except Exception as e:
            st.error(f"Falha ao gravar no Google Sheets: {e}. Salvando em backup local...")
            
    # Fallback: Gravar no CSV local
    csv_path = os.path.join(DADOS_DIR, f"respostas_{procedimento.lower().replace(' ', '_')}.csv")
    arquivo_existe = os.path.exists(csv_path)
    
    try:
        with open(csv_path, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if not arquivo_existe:
                writer.writerow(COLUNAS)
            writer.writerow(linha)
        return True, "Local CSV"
    except Exception as e:
        st.error(f"Erro ao salvar localmente: {e}")
        return False, None

def carregar_respostas(procedimento):
    """Carrega as respostas de um determinado procedimento (do Sheets ou do CSV)."""
    client, sheet = get_sheets_client()
    
    if sheet is not None:
        try:
            try:
                worksheet = sheet.worksheet(procedimento)
                records = worksheet.get_all_records()
                if records:
                    return pd.DataFrame(records)
                else:
                    return pd.DataFrame(columns=COLUNAS)
            except Exception:
                return pd.DataFrame(columns=COLUNAS)
        except Exception as e:
            st.error(f"Erro ao ler do Google Sheets: {e}. Lendo dados locais...")
            
    # Fallback local
    csv_path = os.path.join(DADOS_DIR, f"respostas_{procedimento.lower().replace(' ', '_')}.csv")
    if os.path.exists(csv_path):
        try:
            return pd.read_csv(csv_path, encoding="utf-8")
        except Exception as e:
            st.error(f"Erro ao ler CSV local: {e}")
            return pd.DataFrame(columns=COLUNAS)
    return pd.DataFrame(columns=COLUNAS)

# --- SESSÃO DO STREAMLIT ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Apresentação"

# Função callback para alterar a página
def navigate_to(page_name):
    st.session_state.current_page = page_name

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("## 🎓 Metodologia")
    st.markdown("Plataforma Interativa de Metodologia de Pesquisa para Estudantes Universitários.")
    st.write("---")
    
    # Navegação do menu lateral
    page_options = [
        "🏠 Apresentação",
        "🔍 Abordagem",
        "🧪 Natureza",
        "🎯 Objetivos",
        "📋 Procedimentos",
        "📝 Enviar Minha Pesquisa",
        "📊 Mural de Pesquisas"
    ]
    
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
    
    # Sincronizar o estado da página
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()

    st.write("---")
    
    # --- DIAGNÓSTICO DE CONEXÃO NO SIDEBAR ---
    st.markdown("### 🔌 Conexão Google Sheets")
    client_test, sheet_test = get_sheets_client()
    if "gcp_service_account" not in st.secrets and "gcp_service_account_json" not in st.secrets:
        st.info("⚠️ Usando Banco de Dados Local (CSV).\n\nPara usar o Google Sheets, configure o arquivo `.streamlit/secrets.toml`.")
    elif client_test is None or sheet_test is None:
        st.error("❌ Erro de Conexão com o Google Sheets! Verifique as credenciais ou o e-mail compartilhado.")
    else:
        st.success("✅ Conectado ao Google Sheets com sucesso!")

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
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        st.markdown(
            """
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
            """
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
            """
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
            """
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

# --- ABA DE FORMULÁRIO DE ENVIO ---
elif st.session_state.current_page == "📝 Enviar Minha Pesquisa":
    st.title("📝 Envio de Dados de Pesquisa")
    st.markdown("Utilize o formulário abaixo para registrar os detalhes e a classificação da sua pesquisa científica.")
    
    with st.form("form_pesquisa", clear_on_submit=True):
        col_inf1, col_inf2 = st.columns(2)
        with col_inf1:
            nome = st.text_input("Seu Nome Completo *")
            turma = st.text_input("Sua Turma *")
        with col_inf2:
            nome_pesquisa = st.text_input("Nome da Pesquisa *")
            periodo = st.text_input("Período de Tempo da Pesquisa (Ex: Março a Junho de 2026) *")
            
        pergunta = st.text_area("Pergunta de Pesquisa (Problema de Investigação) *")
        
        st.write("---")
        st.markdown("### Classificação Metodológica")
        
        col_met1, col_met2, col_met3 = st.columns(3)
        with col_met1:
            abordagem = st.selectbox("Abordagem da Pesquisa", ["Qualitativa", "Quantitativa"])
        with col_met2:
            natureza = st.selectbox("Natureza da Pesquisa", ["Básica", "Aplicada"])
        with col_met3:
            procedimento = st.selectbox(
                "Procedimento Metodológico *", 
                ["Experimental", "Bibliográfica", "Documental", "De Campo", "Etnográfica"]
            )
            
        st.write("---")
        st.markdown("### Informações Adicionais sobre a Coleta")
        
        quantidade_dados = st.text_input("Quantidade de Dados Coletados (Ex: 15 entrevistas, 50 questionários, 20 artigos) *")
        fontes = st.text_area("Fontes de Dados (Ex: Google Acadêmico, Diário Oficial, Entrevistas presenciais, etc.) *")
        
        st.markdown("<small>* Campos obrigatórios</small>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Submeter Pesquisa para o Mural")
        
        if submitted:
            if not nome or not turma or not nome_pesquisa or not pergunta or not quantidade_dados or not periodo or not fontes:
                st.error("⚠️ Por favor, preencha todos os campos obrigatórios sinalizados com *.")
            else:
                dados_envio = {
                    "Nome": nome.strip(),
                    "Turma": turma.strip(),
                    "Nome da Pesquisa": nome_pesquisa.strip(),
                    "Pergunta": pergunta.strip(),
                    "Abordagem": abordagem,
                    "Natureza": natureza,
                    "Procedimento": procedimento,
                    "Quantidade de Dados": quantidade_dados.strip(),
                    "Período": periodo.strip(),
                    "Fontes": fontes.strip(),
                    "Data de Envio": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
                
                with st.spinner("Gravando dados..."):
                    sucesso, local = salvar_resposta(dados_envio)
                    
                if sucesso:
                    st.success(f"🎉 Pesquisa submetida com sucesso! Gravado via: **{local}**")
                    st.balloons()
                else:
                    st.error("❌ Ocorreu um erro ao salvar sua pesquisa. Tente novamente.")

# --- ABA MURAL DE PESQUISAS ---
elif st.session_state.current_page == "📊 Mural de Pesquisas":
    st.title("📊 Mural de Pesquisas dos Colegas")
    st.markdown("Visualize as classificações e delineamentos de pesquisas enviados por outros alunos da turma.")
    st.write("---")
    
    procedimentos_disponiveis = ["Experimental", "Bibliográfica", "Documental", "De Campo", "Etnográfica"]
    filtro_proc = st.selectbox("Selecione o Procedimento para filtrar as pesquisas:", procedimentos_disponiveis)
    
    with st.spinner("Carregando pesquisas..."):
        df_respostas = carregar_respostas(filtro_proc)
        
    if df_respostas.empty:
        st.info(f"ℹ️ Nenhuma pesquisa cadastrada para o procedimento **{filtro_proc}** ainda. Seja o primeiro a enviar!")
    else:
        st.success(f"Foram encontradas **{len(df_respostas)}** pesquisas cadastradas em **{filtro_proc}**:")
        
        for _, row in df_respostas.iterrows():
            nome_aluno = row.get("Nome", "Não informado")
            turma_aluno = row.get("Turma", "Não informado")
            titulo_pesquisa = row.get("Nome da Pesquisa", "Sem título")
            pergunta_pesquisa = row.get("Pergunta", "Sem problema formulado")
            abordagem_pesquisa = row.get("Abordagem", "Não especificado")
            natureza_pesquisa = row.get("Natureza", "Não especificado")
            qtd_dados = row.get("Quantidade de Dados", "Não especificado")
            periodo_pesquisa = row.get("Período", "Não especificado")
            fontes_pesquisa = row.get("Fontes", "Não especificado")
            data_envio = row.get("Data de Envio", "Não registrado")
            
            ficha_html = f"""
            <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #0369a1; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <h4 style="margin: 0 0 8px 0; color: #0f172a; font-family: Arial, sans-serif; font-size: 1.2rem; text-transform: uppercase;">📕 {titulo_pesquisa}</h4>
                <p style="margin: 0 0 10px 0; font-size: 0.92rem; color: #475569;"><b>Pesquisador(a):</b> {nome_aluno} | <b>Turma:</b> {turma_aluno}</p>
                <div style="background: #ffffff; border-left: 3px solid #64748b; padding: 12px; margin: 12px 0; font-style: italic; color: #334155; font-size: 0.98rem; text-align: justify;">
                    "{pergunta_pesquisa}"
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-top: 10px; font-size: 0.9rem; color: #334155;">
                    <div><b>Abordagem:</b> {abordagem_pesquisa}</div>
                    <div><b>Natureza:</b> {natureza_pesquisa}</div>
                    <div><b>Dados Coletados:</b> {qtd_dados}</div>
                    <div><b>Período:</b> {periodo_pesquisa}</div>
                </div>
                <div style="margin-top: 10px; font-size: 0.9rem; color: #334155;">
                    <b>Fontes:</b> {fontes_pesquisa}
                </div>
                <div style="margin-top: 15px; font-size: 0.8rem; color: #94a3b8; text-align: right;">
                    Submetido em: {data_envio}
                </div>
            </div>
            """
            st.markdown(ficha_html, unsafe_allow_html=True)
            
        with st.expander("👁️ Visualizar dados brutos em formato de tabela"):
            st.dataframe(df_respostas, use_container_width=True)

# --- SETORES CONCEITUAIS ---
else:
    setor_key = st.session_state.current_page.split(" ")[1]
    setor_data = SETORES[setor_key]
    
    st.title(setor_data["title"])
    st.markdown(f"*{setor_data['description']}*")
    st.write("---")
    
    subtopicos_names = list(setor_data["subtopicos"].keys())
    subtopicos_tabs = st.tabs([f"🔹 {name}" for name in subtopicos_names])
    
    for idx, tab_el in enumerate(subtopicos_tabs):
        sub_name = subtopicos_names[idx]
        sub_data = setor_data["subtopicos"][sub_name]
        
        with tab_el:
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
