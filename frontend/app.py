import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1/extract"

st.set_page_config(
    page_title="Auditor de Contratos", 
    page_icon="📄",
    layout="wide"
)

st.title("Auditor de Contratos")
st.markdown("Faça o upload de um contrato (`.txt` ou `.pdf`) para extrair dados estruturados automaticamente.")

uploaded_file = st.file_uploader("Escolha um arquivo de contrato", type=["txt", "pdf"])

if uploaded_file is not None:
    if st.button("Extrair Dados", type="primary"):
        with st.spinner("Analisando o contrato..."):
            
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }
            
            try:
                response = requests.post(API_URL, files=files)
                response.raise_for_status()
                
                result = response.json()
                data = result.get("extracted_data", {})
                
                st.success("Extração completa!")
                
                st.subheader("Informações Extraídas")
                
                col1, col2, col3 = st.columns(3)
                
                col1.metric("Contratante", data.get("contractor"))
                col2.metric("Contratada", data.get("contractee"))
                col3.metric("Valor Total", f"R$ {data.get('total_value')}")
                
                st.divider()
                
                col4, col5, col6 = st.columns(3)
                col4.metric("Data de Assinatura", data.get("signature_date"))
                col5.metric("Possui multa?", "Sim" if data.get("has_penalty_clause") else "Não")
                
                score = data.get("confidence_score", 0)
                score_color = "green" if score >= 8 else "orange" if score >= 5 else "red"
                col6.markdown(f"### Grau de Confiança: :{score_color}[{score}/10]")
                
                st.divider()
                
                st.subheader("Resumo do Contrato")
                st.info(data.get("summary"))
                
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao se comunicar com a API: {e}")