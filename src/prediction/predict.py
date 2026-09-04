"""
Unified prediction engine for Multi-Disease Prediction System.
Handles model artifact loading, input formatting, pipeline inference,
confidence computation, and structured result generation.
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional

from src.utils.constants import DISEASE_METADATA
from src.utils.validation import validate_input
from src.preprocessing.heart_preprocessing import format_heart_input
from src.preprocessing.kidney_preprocessing import format_kidney_input
from src.preprocessing.liver_preprocessing import format_liver_input
from src.preprocessing.lung_preprocessing import format_lung_input
from src.preprocessing.breast_cancer_preprocessing import format_breast_cancer_input

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# In-memory artifact cache
_MODEL_CACHE: Dict[str, Any] = {}
_METADATA_CACHE: Dict[str, Dict[str, Any]] = {}

def get_model_path(disease: str) -> str:
    return os.path.join(MODELS_DIR, disease, "model.pkl")

def get_metadata_path(disease: str) -> str:
    return os.path.join(MODELS_DIR, disease, "metadata.json")

def load_model_and_metadata(disease: str) -> Tuple[Optional[Any], Optional[Dict[str, Any]], Optional[str]]:
    """
    Loads and caches the model pipeline and metadata for a given disease.
    Returns (model, metadata, error_message).
    """
    if disease in _MODEL_CACHE and disease in _METADATA_CACHE:
        return _MODEL_CACHE[disease], _METADATA_CACHE[disease], None

    m_path = get_model_path(disease)
    meta_path = get_metadata_path(disease)

    if not os.path.exists(m_path):
        return None, None, f"Model file for '{disease}' was not found at {m_path}. Please ensure models are trained."

    if not os.path.exists(meta_path):
        return None, None, f"Metadata file for '{disease}' was not found at {meta_path}."

    try:
        model = joblib.load(m_path)
        with open(meta_path, "r") as f:
            metadata = json.load(f)
        _MODEL_CACHE[disease] = model
        _METADATA_CACHE[disease] = metadata
        return model, metadata, None
    except Exception as e:
        return None, None, f"Error loading model for '{disease}': {str(e)}"

def format_input_for_disease(disease: str, user_input: Dict[str, Any]) -> pd.DataFrame:
    """
    Routes user input to the correct preprocessing formatter.
    """
    if disease == "heart":
        return format_heart_input(user_input)
    elif disease == "kidney":
        return format_kidney_input(user_input)
    elif disease == "liver":
        return format_liver_input(user_input)
    elif disease == "lung":
        return format_lung_input(user_input)
    elif disease == "breast_cancer":
        return format_breast_cancer_input(user_input)
    else:
        raise ValueError(f"Unsupported disease: {disease}")

def predict_disease(disease: str, user_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unified prediction function.
    Validates input, preprocesses features, runs inference, and returns rich result dictionary.
    """
    # 1. Validate disease id
    if disease not in DISEASE_METADATA:
        return {
            "status": "error",
            "message": f"Invalid disease identifier: '{disease}'."
        }

    disease_info = DISEASE_METADATA[disease]

    # 2. Validate input schema & ranges
    is_valid, validation_errors = validate_input(disease, user_input)
    if not is_valid:
        return {
            "status": "validation_error",
            "errors": validation_errors,
            "message": "Input validation failed. Please check the entered parameters."
        }

    # 3. Load model and metadata
    model, metadata, load_err = load_model_and_metadata(disease)
    if load_err:
        return {
            "status": "model_error",
            "message": load_err
        }

    # 4. Format features into DataFrame
    try:
        input_df = format_input_for_disease(disease, user_input)
    except Exception as e:
        return {
            "status": "preprocessing_error",
            "message": f"Failed to format input features: {str(e)}"
        }

    # 5. Execute Prediction
    try:
        pred = int(model.predict(input_df)[0])

        # Compute probability / confidence
        prob_pos = 0.5
        prob_neg = 0.5
        confidence = 0.0

        if hasattr(model, "predict_proba"):
            probas = model.predict_proba(input_df)[0]
            if len(probas) == 2:
                prob_neg = float(probas[0])
                prob_pos = float(probas[1])
                confidence = float(np.max(probas) * 100.0)
            elif len(probas) == 1:
                prob_pos = float(probas[0])
                confidence = float(prob_pos * 100.0)
        elif hasattr(model, "decision_function"):
            # For SVMs or linear models without proba
            decision = float(model.decision_function(input_df)[0])
            prob_pos = float(1.0 / (1.0 + np.exp(-decision)))
            prob_neg = float(1.0 - prob_pos)
            confidence = float(max(prob_pos, prob_neg) * 100.0)
        else:
            confidence = 85.0

        is_positive = (pred == 1)
        risk_level = "High Risk" if is_positive else "Low Risk"
        result_label = disease_info["positive_label"] if is_positive else disease_info["negative_label"]
        recommendation = disease_info["positive_desc"] if is_positive else disease_info["negative_desc"]

        return {
            "status": "success",
            "disease": disease,
            "disease_name": disease_info["name"],
            "disease_icon": disease_info["icon"],
            "raw_prediction": pred,
            "is_positive": is_positive,
            "risk_level": risk_level,
            "result_label": result_label,
            "confidence": round(confidence, 2),
            "probability_positive": round(prob_pos * 100, 2),
            "probability_negative": round(prob_neg * 100, 2),
            "recommendation": recommendation,
            "input_features": input_df.to_dict(orient="records")[0],
            "model_name": metadata.get("model_name", "Machine Learning Model"),
            "model_metrics": metadata
        }

    except Exception as e:
        return {
            "status": "prediction_error",
            "message": f"Inference execution failed: {str(e)}"
        }
