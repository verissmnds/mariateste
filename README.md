# Plataforma de Metodologia de Pesquisa 🎓

Esta é uma plataforma web interativa desenvolvida com **Streamlit** e customizada com as normas tipográficas da **ABNT** (Arial e Times New Roman), voltada para estudantes da disciplina de Metodologia de Pesquisa.

O site divide a matéria em quatro setores interativos e organizados:
1.  **Abordagem**: Pesquisa Qualitativa e Quantitativa.
2.  **Natureza**: Pesquisa Básica e Aplicada.
3.  **Objetivos**: Pesquisa Exploratória, Descritiva e Explicativa.
4.  **Procedimentos**: Pesquisa Experimental, Bibliográfica, Documental, de Campo e Etnográfica.

### 🆕 Novas Funcionalidades:
*   **Formulário de Coleta**: Os alunos podem enviar o nome, turma, título da pesquisa, pergunta de investigação, abordagem, natureza, procedimento, quantidade de dados, período e fontes.
*   **Mural de Pesquisas**: Visualização em formato de fichas acadêmicas das respostas de outros colegas, filtradas por procedimento metodológico.
*   **Integração com Google Sheets**: Os dados enviados vão automaticamente para abas específicas da planilha, de acordo com o procedimento.
*   **Fallback Local (CSV)**: Se o Google Sheets não estiver configurado, o site salva automaticamente os dados localmente em arquivos CSV dentro da pasta `dados/`, garantindo o funcionamento imediato do sistema.

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

Instale o Streamlit e as bibliotecas de integração com o Google:
```bash
pip install -r requirements.txt
```

### Passo 3: Executar o Aplicativo
Execute o comando abaixo para iniciar o servidor local:
```bash
streamlit run app.py
```
O aplicativo abrirá automaticamente no seu navegador no endereço `http://localhost:8501`.

---

## 📊 Como Configurar a Planilha do Google Sheets

Para fazer com que os dados preenchidos no formulário vão automaticamente para uma planilha no seu Google Drive, siga estes passos:

### Passo 1: Criar a Planilha
1. Acesse o seu Google Drive e crie uma nova planilha (Google Sheets).
2. Dê um nome à planilha (ex: `Pesquisas Metodologia`).
3. Copie o link completo da planilha da barra de endereço do seu navegador.

### Passo 2: Criar as Credenciais na Google Cloud Platform (GCP)
1. Acesse o [Console do Google Cloud](https://console.cloud.google.com/) com a sua conta Google.
2. Crie um novo projeto (ex: `metodologia-pesquisa-app`).
3. No painel de pesquisa, busque por **Google Sheets API** e clique em **Ativar**.
4. Busque por **Google Drive API** e clique em **Ativar**.
5. No menu lateral esquerdo, vá em **APIs e Serviços > Credenciais**.
6. Clique em **Criar Credenciais** e selecione **Conta de Serviço**.
7. Preencha as informações básicas (nome) e conclua a criação.
8. Na lista de Contas de Serviço criadas, clique sobre o e-mail correspondente para abrir suas configurações.
9. Acesse a aba **Chaves**, clique em **Adicionar Chave > Criar nova chave** e selecione o formato **JSON**.
10. O arquivo JSON será baixado no seu computador. Abra este arquivo no Bloco de Notas: ele contém chaves como `client_email` e `private_key`.

### Passo 3: Compartilhar a Planilha
1. Abra a planilha do Google Sheets que você criou no **Passo 1**.
2. Clique no botão azul **Compartilhar** no canto superior direito.
3. No campo de convite, insira o e-mail da Conta de Serviço (o campo `client_email` que está no JSON baixado, ex: `sua-conta-de-servico@seu-projeto.iam.gserviceaccount.com`).
4. Dê a permissão de **Editor** a esse e-mail e clique em Enviar.

### Passo 4: Configurar os Segredos (Secrets) no Streamlit

#### A) Rodando Localmente (.streamlit/secrets.toml)
Crie uma pasta chamada `.streamlit` na raiz do seu projeto local, e dentro dela, crie um arquivo chamado `secrets.toml`. Insira o seguinte conteúdo, preenchendo com as informações do seu JSON baixado e o link da sua planilha:

```toml
spreadsheet_url = "COLE_AQUI_O_LINK_COMPLETO_DA_SUA_PLANILHA"

[gcp_service_account]
type = "service_account"
project_id = "seu-projeto-id"
private_key_id = "sua-chave-privada-id"
private_key = "-----BEGIN PRIVATE KEY-----\nCOLE_AQUI_A_SUA_CHAVE_PRIVADA_COMPLETA_SUBSTITUINDO_QUEBRAS_DE_LINHA_POR_N\n-----END PRIVATE KEY-----\n"
client_email = "seu-email-servico@seu-projeto.iam.gserviceaccount.com"
client_id = "123456..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```
*(Importante: No campo `private_key`, certifique-se de que a chave está em uma única linha e as quebras de linha reais estão representadas pelo caractere literal `\n`, idêntico ao arquivo JSON baixado).*

#### B) Rodando em Produção (Streamlit Community Cloud)
Quando você fizer o deploy no Streamlit Cloud através do GitHub:
1. Vá nas configurações do seu App no painel do Streamlit Cloud.
2. Acesse a seção **Secrets**.
3. Cole o mesmo conteúdo do arquivo `secrets.toml` acima.
4. Clique em **Salvar**. O aplicativo irá reiniciar automaticamente e a integração estará ativa em produção!
