import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

st.set_page_config(
    page_title="Auditor de Contratos", 
    page_icon="📄",
    layout="wide"
)

st.title("Auditor de Contratos")
st.markdown("Faça o upload de um contrato (`.txt` ou `.pdf`) para extrair dados estruturados automaticamente.")

uploaded_files = st.file_uploader("Escolha os arquivos de contrato", type=["txt", "pdf"], accept_multiple_files=True)

if uploaded_files:
    st.info(f"{len(uploaded_files)} arquivo(s) selecionado(s).")

    if st.button("Extrair Dados", type="primary"):
        with st.spinner("Analisando o(s) contrato(s)..."):
            
            files_payload = []
            for file in uploaded_files:
                files_payload.append(
                    ("docs", (file.name, file.getvalue(), file.type))
                )
            
            try:
                response = requests.post(API_URL, files=files_payload)
                response.raise_for_status()
                
                batch_result = response.json()
                results_list = batch_result.get("results", [])
                
                st.success(f"Processamento concluído! {batch_result['successful']} sucessos, {batch_result['failed']} falhas.")

                flat_data = []
                for item in results_list:
                    data = item.get("extracted_data", {})
                    flat_data.append({
                        "Arquivo": item.get("filename"),
                        "Status": item.get("status"),
                        "Contratante": data.get("contractor"),
                        "Contratada": data.get("contractee"),
                        "Valor Total (R$)": data.get("total_value"),
                        "Data Assinatura": data.get("signature_date"),
                        "Tem Multa?": "Sim" if data.get("has_penalty_clause") else "Não",
                        "Confiança": data.get("confidence_score")
                    })            

                df = pd.DataFrame(flat_data)

                st.subheader("Painel de Extração de Dados")
                st.dataframe(df, width='stretch')

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Baixar Resultados como CSV",
                    data=csv,
                    file_name="extracao_contratos.csv",
                    mime="text/csv",
                )
                
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao se comunicar com a API: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    st.error(f"Detalhes do 422: {e.response.text}")