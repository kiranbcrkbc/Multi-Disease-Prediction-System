"""
Lung Disease Prediction Page — Multi-Disease Prediction System
"""
import streamlit as st
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.utils.constants import LUNG_FIELDS, DISEASE_METADATA
from src.utils.ui_components import inject_custom_css, render_disclaimer, render_model_info_expander, render_prediction_result
from src.prediction.predict import predict_disease

st.set_page_config(
    page_title="Lung Disease Prediction | MDPS",
    page_icon="🫁",
    layout="wide"
)

inject_custom_css()

# Header
st.markdown("## 🫁 Lung Disease & Cancer Risk Screening")
st.markdown(
    "Screen for preliminary respiratory risk based on lifestyle exposure, chronic environmental factors, and symptomatic clinical presentations."
)

st.info(
    "ℹ️ **Scope Note:** This module is a symptom/lifestyle-based machine learning screening prototype and does **not** analyze CT scans, chest X-rays, or medical radiological imaging."
)

render_disclaimer()

# Presets
st.markdown("##### ⚡ Quick Demonstration Presets")
c_preset1, c_preset2, c_preset3 = st.columns([1.5, 1.5, 3])

if "lung_data" not in st.session_state:
    st.session_state.lung_data = {k: v["default"] for k, v in LUNG_FIELDS.items()}

with c_preset1:
    if st.button("🟢 Load Low-Risk Lifestyle Sample"):
        st.session_state.lung_data = {
            "GENDER": "Female", "AGE": 32, "SMOKING": "No", "YELLOW_FINGERS": "No",
            "ANXIETY": "No", "PEER_PRESSURE": "No", "CHRONIC_DISEASE": "No",
            "FATIGUE": "No", "ALLERGY": "No", "WHEEZING": "No", "ALCOHOL_CONSUMING": "No",
            "COUGHING": "No", "SHORTNESS_OF_BREATH": "No", "SWALLOWING_DIFFICULTY": "No",
            "CHEST_PAIN": "No"
        }
        st.rerun()

with c_preset2:
    if st.button("🔴 Load High-Risk Symptom Sample"):
        st.session_state.lung_data = {
            "GENDER": "Male", "AGE": 68, "SMOKING": "Yes", "YELLOW_FINGERS": "Yes",
            "ANXIETY": "Yes", "PEER_PRESSURE": "Yes", "CHRONIC_DISEASE": "Yes",
            "FATIGUE": "Yes", "ALLERGY": "No", "WHEEZING": "Yes", "ALCOHOL_CONSUMING": "Yes",
            "COUGHING": "Yes", "SHORTNESS_OF_BREATH": "Yes", "SWALLOWING_DIFFICULTY": "Yes",
            "CHEST_PAIN": "Yes"
        }
        st.rerun()

with c_preset3:
    if st.button("🔄 Reset Defaults"):
        st.session_state.lung_data = {k: v["default"] for k, v in LUNG_FIELDS.items()}
        st.rerun()

st.markdown("---")

with st.form("lung_form"):
    st.markdown("#### 📋 Lifestyle & Symptom Assessment")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**1. Demographics & Lifestyle**")
        GENDER = st.selectbox("Gender", options=["Male", "Female"], index=["Male", "Female"].index(st.session_state.lung_data.get("GENDER", "Male")))
        AGE = st.number_input("Age (years)", min_value=18, max_value=100, value=int(st.session_state.lung_data.get("AGE", 60)))
        SMOKING = st.selectbox("Smoking History", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("SMOKING", "No")))
        ALCOHOL_CONSUMING = st.selectbox("Regular Alcohol Consumption", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("ALCOHOL_CONSUMING", "No")))
        PEER_PRESSURE = st.selectbox("Peer Smoking Pressure Exposure", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("PEER_PRESSURE", "No")))

    with c2:
        st.markdown("**2. Physical & Clinical Signs**")
        YELLOW_FINGERS = st.selectbox("Yellow Fingers (Nicotine Staining)", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("YELLOW_FINGERS", "No")))
        CHRONIC_DISEASE = st.selectbox("Chronic Respiratory / Other Disease", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("CHRONIC_DISEASE", "No")))
        ALLERGY = st.selectbox("Allergy History", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("ALLERGY", "No")))
        WHEEZING = st.selectbox("Wheezing or Stridor", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("WHEEZING", "No")))
        ANXIETY = st.selectbox("Anxiety Symptoms", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("ANXIETY", "No")))

    with c3:
        st.markdown("**3. Respiratory Symptoms**")
        FATIGUE = st.selectbox("Persistent Fatigue / Weakness", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("FATIGUE", "No")))
        COUGHING = st.selectbox("Chronic / Persistent Coughing", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("COUGHING", "No")))
        SHORTNESS_OF_BREATH = st.selectbox("Shortness of Breath (Dyspnea)", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("SHORTNESS_OF_BREATH", "No")))
        SWALLOWING_DIFFICULTY = st.selectbox("Swallowing Difficulty (Dysphagia)", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("SWALLOWING_DIFFICULTY", "No")))
        CHEST_PAIN = st.selectbox("Chest Pain / Pressure", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.lung_data.get("CHEST_PAIN", "No")))

    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("🫁 Run Lung Disease Assessment", use_container_width=True)

if submit_btn:
    user_payload = {
        "GENDER": GENDER,
        "AGE": AGE,
        "SMOKING": SMOKING,
        "YELLOW_FINGERS": YELLOW_FINGERS,
        "ANXIETY": ANXIETY,
        "PEER_PRESSURE": PEER_PRESSURE,
        "CHRONIC_DISEASE": CHRONIC_DISEASE,
        "FATIGUE": FATIGUE,
        "ALLERGY": ALLERGY,
        "WHEEZING": WHEEZING,
        "ALCOHOL_CONSUMING": ALCOHOL_CONSUMING,
        "COUGHING": COUGHING,
        "SHORTNESS_OF_BREATH": SHORTNESS_OF_BREATH,
        "SWALLOWING_DIFFICULTY": SWALLOWING_DIFFICULTY,
        "CHEST_PAIN": CHEST_PAIN
    }

    with st.spinner("Processing symptom profile and lifestyle risk factors..."):
        prediction_res = predict_disease("lung", user_payload)
        render_prediction_result(prediction_res)

st.markdown("---")
render_model_info_expander("lung")
