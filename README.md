# Plataforma de Metodologia de Pesquisa 🎓

Esta é uma plataforma web interativa desenvolvida com **Streamlit** e customizada com as normas tipográficas da **ABNT** (Arial e Times New Roman), voltada para estudantes da disciplina de Metodologia de Pesquisa.

O site divide a matéria em quatro setores interativos e organizados:
1.  **Abordagem**: Pesquisa Qualitativa e Quantitativa.
2.  **Natureza**: Pesquisa Básica e Aplicada.
3.  **Objetivos**: Pesquisa Exploratória, Descritiva e Explicativa.
4.  **Procedimentos**: Pesquisa Experimental, Bibliográfica, Documental, de Campo e Etnográfica.

Cada tópico oferece:
*   **Conceito (Teoria)**: Uma fundamentação científica clara.
*   **Recursos Visuais**: Vídeos incorporados do YouTube sobre o assunto.
*   **Estudo de Caso**: Casos práticos simulando aplicações do método no mundo real.

---

## 🛠️ Como Executar Localmente

### Passo 1: Pré-requisitos
Certifique-se de ter o **Python 3.8 ou superior** instalado em sua máquina.

### Passo 2: Instalação das Dependências
Abra o terminal na pasta do projeto e crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
```
Ative o ambiente virtual:
*   **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
*   **Linux/macOS:** `source venv/bin/activate`

Instale o Streamlit:
```bash
pip install -r requirements.txt
```

### Passo 3: Executar o Aplicativo
Execute o comando abaixo para iniciar o servidor local:
```bash
streamlit run app.py
```
O aplicativo abrirá automaticamente no seu navegador padrão no endereço `http://localhost:8501`.

---

## 🚀 Como Publicar no GitHub e Fazer Deploy no Streamlit Cloud

### Passo 1: Publicar no GitHub
1.  Crie um novo repositório vazio no seu **GitHub** (ex: `metodologia-pesquisa`).
2.  No seu terminal local (dentro da pasta deste projeto), execute os seguintes comandos para subir os arquivos:
    ```bash
    git init
    git add .
    git commit -m "feat: estrutura inicial da plataforma de metodologia"
    git branch -M main
    git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
    git push -u origin main
    ```
    *(Substitua `SEU_USUARIO` e `NOME_DO_REPOSITORIO` pelos seus dados correspondentes).*

### Passo 2: Deploy no Streamlit Community Cloud
1.  Acesse o site: [https://share.streamlit.io/](https://share.streamlit.io/)
2.  Faça login utilizando a sua conta do **GitHub**.
3.  Clique no botão **"Create app"** ou **"New app"** no canto superior direito.
4.  Preencha as configurações do repositório:
    *   **Repository**: Selecione o repositório que você acabou de subir (ex: `SEU_USUARIO/metodologia-pesquisa`).
    *   **Branch**: Escolha `main`.
    *   **Main file path**: Digite `app.py`.
5.  Clique no botão **"Deploy!"**.
6.  Em poucos minutos, seu site estará no ar com um link público (ex: `https://metodologia-pesquisa.streamlit.app/`) que você poderá compartilhar diretamente com seus alunos!
