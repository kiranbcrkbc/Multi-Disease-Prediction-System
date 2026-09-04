"""
Liver Disease Prediction Page — Multi-Disease Prediction System
"""
import streamlit as st
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.utils.constants import LIVER_FIELDS, DISEASE_METADATA
from src.utils.ui_components import inject_custom_css, render_disclaimer, render_model_info_expander, render_prediction_result
from src.prediction.predict import predict_disease

st.set_page_config(
    page_title="Liver Disease Prediction | MDPS",
    page_icon="🫀",
    layout="wide"
)

inject_custom_css()

# Header
st.markdown("## 🫀 Liver Disease Risk Assessment")
st.markdown(
    "Assess hepatic impairment and liver disease risk based on biochemical blood markers, liver enzymes, bilirubin levels, and serum protein ratios."
)

render_disclaimer()

# Presets
st.markdown("##### ⚡ Quick Demonstration Presets")
c_preset1, c_preset2, c_preset3 = st.columns([1.5, 1.5, 3])

if "liver_data" not in st.session_state:
    st.session_state.liver_data = {k: v["default"] for k, v in LIVER_FIELDS.items()}

with c_preset1:
    if st.button("🟢 Load Normal / Low Risk Sample"):
        st.session_state.liver_data = {
            "Age": 28, "Gender": "Female", "TB": 0.7, "DB": 0.2, "Alkphos": 155,
            "Sgpt": 22, "Sgot": 24, "TP": 7.3, "ALB": 4.0, "A_G_Ratio": 1.2
        }
        st.rerun()

with c_preset2:
    if st.button("🔴 Load Elevated / Hepatic Risk Sample"):
        st.session_state.liver_data = {
            "Age": 58, "Gender": "Male", "TB": 6.8, "DB": 3.4, "Alkphos": 490,
            "Sgpt": 145, "Sgot": 160, "TP": 5.6, "ALB": 2.4, "A_G_Ratio": 0.7
        }
        st.rerun()

with c_preset3:
    if st.button("🔄 Reset Defaults"):
        st.session_state.liver_data = {k: v["default"] for k, v in LIVER_FIELDS.items()}
        st.rerun()

st.markdown("---")

with st.form("liver_form"):
    st.markdown("#### 📋 Hepatic Diagnostic Markers")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**1. Patient Demographics & Bilirubin**")
        Age = st.number_input("Age (years)", min_value=4, max_value=95, value=int(st.session_state.liver_data.get("Age", 45)))
        Gender = st.selectbox("Gender", options=["Male", "Female"], index=["Male", "Female"].index(st.session_state.liver_data.get("Gender", "Male")))
        TB = st.number_input("Total Bilirubin - TB (mg/dl)", min_value=0.4, max_value=75.0, value=float(st.session_state.liver_data.get("TB", 1.2)), step=0.1, help="Normal reference: 0.2 - 1.2 mg/dl")
        DB = st.number_input("Direct Bilirubin - DB (mg/dl)", min_value=0.1, max_value=20.0, value=float(st.session_state.liver_data.get("DB", 0.4)), step=0.1, help="Normal reference: 0.0 - 0.3 mg/dl")

    with c2:
        st.markdown("**2. Hepatic Enzymes**")
        Alkphos = st.number_input("Alkaline Phosphatase - ALP (IU/L)", min_value=60, max_value=2200, value=int(st.session_state.liver_data.get("Alkphos", 200)), help="Normal reference: 44 - 147 IU/L")
        Sgpt = st.number_input("Alamine Aminotransferase - ALT / SGPT (IU/L)", min_value=10, max_value=2000, value=int(st.session_state.liver_data.get("Sgpt", 35)), help="Normal reference: 7 - 56 IU/L")
        Sgot = st.number_input("Aspartate Aminotransferase - AST / SGOT (IU/L)", min_value=10, max_value=5000, value=int(st.session_state.liver_data.get("Sgot", 40)), help="Normal reference: 10 - 40 IU/L")

    with c3:
        st.markdown("**3. Serum Proteins & Ratios**")
        TP = st.number_input("Total Proteins - TP (g/dl)", min_value=2.5, max_value=10.0, value=float(st.session_state.liver_data.get("TP", 6.8)), step=0.1, help="Normal reference: 6.0 - 8.3 g/dl")
        ALB = st.number_input("Albumin - ALB (g/dl)", min_value=0.8, max_value=6.0, value=float(st.session_state.liver_data.get("ALB", 3.4)), step=0.1, help="Normal reference: 3.5 - 5.0 g/dl")
        A_G_Ratio = st.number_input("Albumin and Globulin Ratio (A/G)", min_value=0.3, max_value=3.0, value=float(st.session_state.liver_data.get("A_G_Ratio", 1.0)), step=0.05, help="Normal reference: 1.0 - 2.2")

    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("🫀 Run Liver Disease Prediction", use_container_width=True)

if submit_btn:
    user_payload = {
        "Age": Age,
        "Gender": Gender,
        "TB": TB,
        "DB": DB,
        "Alkphos": Alkphos,
        "Sgpt": Sgpt,
        "Sgot": Sgot,
        "TP": TP,
        "ALB": ALB,
        "A_G_Ratio": A_G_Ratio
    }

    with st.spinner("Analyzing hepatic enzyme concentrations..."):
        prediction_res = predict_disease("liver", user_payload)
        render_prediction_result(prediction_res)

st.markdown("---")
render_model_info_expander("liver")
