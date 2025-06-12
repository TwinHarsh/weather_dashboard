import streamlit as st

def set_background():
    bg_url = "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1920&q=80"

    
    st.markdown(
        f"""
        <style>
        html , body, .main, .block-container , .stApp {{
            height: 100vh;
            background-image: url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }}

        [data-testid="stAppViewContainer"], 
        [data-testid="stBlock"] {{
            background-color: transparent !important;
        }}

        [data-testid="stPlotlyChart"] > div,
        [data-testid="stPlotlyChart"] > div > div,
        [data-testid="stPlotlyChart"] svg {{
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
            padding: 0 !important;
            box-shadow: none !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
