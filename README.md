# 📄 Extrator de Dados para Contratos

Uma aplicação básica desenvolvida com **FastAPI**, **LangChain** e **Streamlit** que utiliza LLMs para analisar e extrair dados estruturados de contratos em formato PDF e TXT.

## 🚀 Tecnologias

**Backend:**

- **Python 3 & FastAPI:** Framework assíncrono para APIs.
- **asyncio:** Utilizado para Processamento em lote.
- **LangChain:** Responsável pelo pipeline de extração com o LLM.
- **Pydantic:** Validação de tipagem dos dados de saída.
- **PyPDF:** Extração de texto de PDFs.

**Frontend:**

- **Streamlit:** Framework para criação do dashboard.
- **Pandas:** Transformação dos dados em DataFrames e exportação para CSV.

## 🌟 Principais Funcionalidades

- **Processamento em Lote (Batch Processing):** É possível fazer upload de vários arquivos simultaneamente. A API processa todos em paralelo, reduzindo drasticamente o tempo de espera.
- **Extração Estruturada (JSON):** O LLM é forçado via sistema a retornar os dados estritamente dentro do schema do Pydantic.
- **Human-in-the-Loop (HITL) - Score de Confiança:** O sistema avalia sua própria extração gerando um _Confidence Score_ (1 a 10). A interface exibe alertas visuais para indicar ao operador humano se a extração requer revisão manual.
- **Exportação de Dados:** Os resultados do lote são compilados em uma tabela interativa que pode ser exportada para CSV.

## ⚙️ Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/eduardoviana11/extrator-dados-contratos.git
cd extrator-dados-contratos
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto e adicione sua chave de API:

```bash
GOOGLE_API_KEY=sua_chave_aqui
```

### 3. Rodar o Backend (FastAPI)

Em um terminal, instale as dependências e inicie o servidor:

```bash
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

A API estará rodando em http://127.0.0.1:8000. Acesse /docs para ver a documentação interativa (Swagger).

### 4. Rodar o Frontend (Streamlit)

Abra um novo terminal, ative o ambiente virtual novamente, instale as dependências do front e rode a aplicação:

```bash
# Ative o venv novamente
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

A interface gráfica abrirá automaticamente no seu navegador.

---
