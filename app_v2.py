# app_v2.py
import streamlit as st
import numpy as np


# Define the model class at the VERY TOP
class SimplePhishingDetector:
    def predict(self, features):
        # Simple rule-based detection
        score = 0

        # URL length check
        if features.get('url_length', 0) > 75:
            score += 1

        # IP address check
        if features.get('has_ip', 0) == 1:
            score += 2

        # Special characters check
        if features.get('num_special_chars', 0) > 5:
            score += 1

        # Simple threshold-based decision
        return 1 if score >= 2 else 0

    def predict_proba(self, features):
        prediction = self.predict(features)
        if prediction == 1:
            return np.array([[0.3, 0.7]])  # 70% confidence it's phishing
        else:
            return np.array([[0.7, 0.3]])  # 70% confidence it's legitimate


# Initialize the model immediately after its definition
model = SimplePhishingDetector()

# Now create the app
st.title("Phishing Detector v2")
st.write("Now with model definition added.")

url = st.text_input("Enter a URL to analyze")

if url:
    st.write(f"You entered: {url}")
    st.write("Model is defined and ready to use!")
    st.write(f"Model type: {type(model).__name__}")