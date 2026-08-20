# 📄 Extrator de Dados para Contratos

Uma aplicação básica desenvolvida com **FastAPI** e **Streamlit** que utiliza modelos fundacionais (LLMs) para analisar e extrair dados estruturados de contratos jurídicos em formato PDF e TXT.

Este projeto demonstra a aplicação de **Engenharia de Prompt**, **Structured Outputs** (forçando respostas determinísticas do LLM) e o conceito de **Human-in-the-Loop (HITL)** através de métricas de confiança geradas pela própria IA.

## 🚀 Funcionalidades

* **Extração Determinística:** Utiliza `Pydantic` e a funcionalidade `with_structured_output` do LangChain para garantir que o modelo retorne exclusivamente um JSON válido e estritamente tipado, eliminando alucinações de formatação.
* **Processamento de PDFs em Memória:** Leitura de arquivos PDF via `io.BytesIO` e `PyPDF`, garantindo segurança e alta performance sem a necessidade de gravar arquivos temporários no disco do servidor.
* **Avaliação de Confiança (Confidence Score):** O LLM é instruído a autoavaliar sua extração, gerando uma nota de 1 a 10. A interface alerta visualmente o usuário caso a extração possua baixo grau de certeza (HITL).
* **Arquitetura Desacoplada:** Backend construído como uma API RESTful independente (FastAPI) e Frontend interativo desenvolvido em Streamlit.

## 🛠️ Tecnologias Utilizadas

**Backend:**
* Python 3.10+
* FastAPI & Uvicorn (Roteamento assíncrono e API REST)
* LangChain & LangChain Google GenAI (Orquestração do LLM)
* Pydantic (Validação e tipagem rigorosa de dados)
* PyPDF (Extração de texto de PDFs)

**Frontend:**
* Streamlit (Interface de usuário reativa)
* Requests (Comunicação HTTP com a API)

## ⚙️ Como Executar Localmente

### 1. Clone o repositório
```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
cd NOME_DO_REPOSITORIO
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
