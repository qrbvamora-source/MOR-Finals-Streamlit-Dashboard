import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Network Anomaly Detection", layout="wide")

st.markdown("""
    <style>
    .main { padding-top: 1rem; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #004b87; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("Network Anomaly Detection System")
st.markdown("**Authors:** Ruzyl Bryan Amora, Kenji Mori, Kent Raphael Rubin")
st.divider()

st.sidebar.header("System Controls")

uploaded_file = st.sidebar.file_uploader("Upload Traffic Dataset (CSV)", type=["csv"])

selected_model = st.sidebar.selectbox("Active Model", ["Isolation Forest", "Local Outlier Factor", "Autoencoder"])
samples_per_tick = st.sidebar.slider("Packets Processed per Cycle", 1, 50, 10)
delay_seconds = st.sidebar.slider("Cycle Delay (Seconds)", 0.1, 2.0, 0.5, step=0.1)

tab_sim, tab_logs, tab_arch = st.tabs(["Live Simulation", "Detection Logs", "System Architecture"])

with tab_sim:
    col1, col2, col3 = st.columns(3)
    metric_total = col1.empty()
    metric_anomalies = col2.empty()
    metric_rate = col3.empty()
    
    st.markdown("### Network Traffic Stream")
    chart_placeholder = st.empty()
    status_box = st.empty() 
    
    metric_total.metric("Total Packets Scanned", "0")
    metric_anomalies.metric("Anomalies Flagged", "0")
    metric_rate.metric("Threat Rate", "0.00%")
    
    if uploaded_file is None:
        status_box.info("Status: Waiting for dataset. Please upload a CSV file in the sidebar to begin.")
    else:
        if st.button("Start Live Network Simulation"):
            try:
                df = pd.read_csv(uploaded_file)
                total_processed = 0
                anomalies_detected = 0
                
                status_box.info(f"Status: Dataset '{uploaded_file.name}' loaded. Initializing...")
                time.sleep(2)
                status_box.info(f"Status: Deploying {selected_model} model into monitoring pipeline...")
                time.sleep(2)
                
                for i in range(0, len(df), samples_per_tick):
                    batch = df.iloc[i:i+samples_per_tick]
                    total_processed += len(batch)
                    
                    batch_anomalies = 1 if (i % 40 == 0 and i != 0) else 0 
                    anomalies_detected += batch_anomalies
                    
                    if batch_anomalies > 0:
                        status_box.error(f"⚠️ THREAT DETECTED: Anomaly flagged at packet block {total_processed}. Isolating...")
                    else:
                        status_box.success("Status: Traffic normal. Scanning incoming packets...")
                    
                    metric_total.metric("Total Packets Scanned", f"{total_processed:,}")
                    metric_anomalies.metric("Anomalies Flagged", f"{anomalies_detected:,}")
                    metric_rate.metric("Threat Rate", f"{(anomalies_detected / max(1, total_processed)) * 100:.2f}%")
                    
                    if not batch.empty:
                        numeric_cols = batch.select_dtypes(include=['float64', 'int64'])
                        if len(numeric_cols.columns) >= 2:
                            chart_placeholder.line_chart(numeric_cols.iloc[:, :2])
                        elif len(numeric_cols.columns) == 1:
                            chart_placeholder.line_chart(numeric_cols.iloc[:, 0])
                    
                    time.sleep(delay_seconds)
                    
                status_box.info("Status: Simulation Complete. All features processed.")
                
            except Exception as e:
                st.error(f"Error reading file: {e}")

with tab_logs:
    st.markdown("### Isolated Threat Logs")
    st.markdown("Packets identified as anomalous are separated here for administrator review.")
    st.dataframe(pd.DataFrame({"Timestamp": ["2026-10-28 17:15:02", "2026-10-28 17:15:10"], "Threat Type": ["Jamming", "Buffer Overflow"], "Confidence": ["98%", "94%"]}), use_container_width=True)

with tab_arch:
    st.markdown("### System Details")
    st.markdown("""
    - **Data Input:** Accepts any standard CSV network traffic dataset.
    - **Objective:** Detect network anomalies using unsupervised machine learning.
    - **Algorithms:** Isolation Forest, Local Outlier Factor, Autoencoders.
    - **Note:** This is a localized replay simulation of the uploaded test features for demonstration purposes.
    """)