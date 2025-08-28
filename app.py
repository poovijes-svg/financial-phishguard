# app_v2.py
import streamlit as st
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import re


# Define the model class at the VERY TOP
class SimplePhishingDetector:
    def predict(self, features):
        # Convert Pandas Series to dictionary if needed
        if hasattr(features, 'to_dict'):  # This is a Pandas Series
            features = features.to_dict()

        # Now we can safely use .get() method
        score = 0

        # URL length check
        if features.get('url_length', 0) > 50:
            score += 1

        # IP address check
        if features.get('has_ip', 0) == 1:
            score += 3

        # Special characters check
        if features.get('num_special_chars', 0) > 3:
            score += 1

        # Check for suspicious keywords in domain
        if features.get('suspicious_keywords', 0) > 0:
            score += 2

        # Check for multiple subdomains
        if features.get('num_subdomains', 0) > 2:
            score += 1

        # Adjust threshold as needed
        return 1 if score >= 3 else 0

    def predict_proba(self, features):
        prediction = self.predict(features)
        if prediction == 1:
            return np.array([[0.3, 0.7]])  # 70% confidence it's phishing
        else:
            return np.array([[0.7, 0.3]])  # 70% confidence it's legitimate


# Initialize the model immediately after its definition
model = SimplePhishingDetector()


# Simple feature extraction function
def get_features(url):
    features = {}

    # Feature 1: Length of URL
    features['url_length'] = len(url)

    # Feature 2: Check if URL uses an IP address
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        # Check if hostname looks like an IP address
        is_ip = 1 if (hostname and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname)) else 0
        features['has_ip'] = is_ip
    except:
        features['has_ip'] = 0

    # Feature 3: Count special characters
    features['num_special_chars'] = url.count('@') + url.count('?') + url.count('=') + url.count('-')

    return features


# Create the app interface
st.set_page_config(
    page_title="Financial PhishGuard",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Financial PhishGuard")
st.markdown("Analyze URLs to detect potential phishing attempts")

url_input = st.text_input("Enter a URL to analyze:", placeholder="https://example.com")

if url_input:
    with st.spinner('Analyzing URL...'):
        try:
            # Extract features
            features = get_features(url_input)

            # Make prediction
            probability = model.predict_proba(features)[0]
            prediction = model.predict(features)

            # Display results
            if prediction == 0:
                st.success(f"✅ **LEGITIMATE** (Confidence: {probability[0] * 100:.1f}%)")
            else:
                st.error(f"🚨 **PHISHING THREAT DETECTED!** (Confidence: {probability[1] * 100:.1f}%)")
                st.warning("Do not enter any personal information on this site!")

            # Show the features that were analyzed
            st.subheader("Analysis Details")
            feature_df = pd.DataFrame([features])
            st.dataframe(feature_df.T.rename(columns={0: 'Value'}))

        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")

# Add some information
with st.sidebar:
    st.header("About")
    st.markdown("This tool analyzes URLs for potential phishing attempts using simple heuristics.")