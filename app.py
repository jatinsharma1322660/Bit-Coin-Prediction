import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

st.set_page_config(page_title="Bitcoin Price Prediction", layout="wide")
st.title("📈 Bitcoin Price Prediction using ML")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Data", "Data Overview", "Visualize", "Predict"])

# Initialize session state
if 'btc_df' not in st.session_state:
    st.session_state['btc_df'] = None
if 'wiki_df' not in st.session_state:
    st.session_state['wiki_df'] = None

# Upload section
if page == "Upload Data":
    st.subheader("📤 Upload Files")

    btc_file = st.file_uploader("Upload Bitcoin Data (.csv)", type=["csv"])
    wiki_file = st.file_uploader("Upload Wikipedia Edit Data (.csv)", type=["csv"])

    if btc_file is not None:
        btc_df = pd.read_csv(io.StringIO(btc_file.getvalue().decode("utf-8")))
        st.session_state['btc_df'] = btc_df
        st.success("✅ Bitcoin data uploaded successfully!")
        st.dataframe(btc_df.head())

    if wiki_file is not None:
        wiki_df = pd.read_csv(io.StringIO(wiki_file.getvalue().decode("utf-8")))
        st.session_state['wiki_df'] = wiki_df
        st.success("✅ Wikipedia edits data uploaded successfully!")
        st.dataframe(wiki_df.head())

# Data Overview
elif page == "Data Overview":
    st.subheader("📊 Bitcoin Dataset Overview")

    btc_df = st.session_state.get('btc_df')
    if btc_df is not None:
        st.write("Shape:", btc_df.shape)
        st.dataframe(btc_df.head())
        st.markdown("### Summary Statistics")
        st.dataframe(btc_df.describe())
    else:
        st.warning("⚠️ Please upload Bitcoin data first on the 'Upload Data' page.")

# Visualization
elif page == "Visualize":
    st.subheader("📉 Data Visualization")

    btc_df = st.session_state.get('btc_df')
    if btc_df is not None:
        if 'Date' in btc_df.columns:
            btc_df['Date'] = pd.to_datetime(btc_df['Date'], errors='coerce')
            col = st.selectbox("Select Column", btc_df.columns[1:])
            fig, ax = plt.subplots()
            ax.plot(btc_df['Date'], btc_df[col])
            ax.set_xlabel("Date")
            ax.set_ylabel(col)
            ax.set_title(f"{col} over Time")
            st.pyplot(fig)
        else:
            st.error("⚠️ No 'Date' column found in the dataset.")
    else:
        st.warning("⚠️ Please upload Bitcoin data first on the 'Upload Data' page.")

# Prediction
elif page == "Predict":
    st.subheader("🔮 Predict Bitcoin Price")

    open_p = st.number_input("Open Price", min_value=0.0)
    high_p = st.number_input("High Price", min_value=0.0)
    low_p = st.number_input("Low Price", min_value=0.0)
    volume = st.number_input("Volume", min_value=0.0)

    if st.button("Predict"):
        features = np.array([[open_p, high_p, low_p, volume]])
        prediction = (open_p + high_p + low_p) / 3 + volume * 0.00001
        st.success(f"Predicted Close Price: ${prediction:.2f}")
