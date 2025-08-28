# app.py
import streamlit as st
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import re

# Set the page title and icon
st.set_page_config(
    page_title="Financial PhishGuard",
    page_icon="🛡️",
    layout="centered"
)


# Simple phishing detector class
class SimplePhishingDetector:
    def predict(self, features):
        # Make sure we're working with a dictionary
        if hasattr(features, 'to_dict'):
            features = features.to_dict()

        # Extract values from the features
        url = str(features.get('url', '')).lower()
        url_length = int(features.get('url_length', 0))
        has_ip = int(features.get('has_ip', 0))
        num_special_chars = int(features.get('num_special_chars', 0))
        suspicious_keywords = int(features.get('suspicious_keywords', 0))
        num_subdomains = int(features.get('num_subdomains', 0))

        # Calculate detection score
        score = 0

        # 1. Brand impersonation
        brands = ['paypal', 'bank', 'facebook', 'google', 'apple', 'amazon', 'microsoft']
        for brand in brands:
            if brand in url:
                score += 5
                break

        # 2. Suspicious keywords
        suspicious_terms = ['login', 'secure', 'verify', 'confirm', 'account', 'security']
        for term in suspicious_terms:
            if term in url:
                score += 2

        # 3. URL structure indicators
        if has_ip == 1:
            score += 4

        if num_special_chars > 3:
            score += 2

        if num_subdomains > 2:
            score += 2

        if url_length > 60:
            score += 1

        # 4. HTTP vs HTTPS
        if not url.startswith('https'):
            score += 2

        # Decision
        return 1 if score >= 6 else 0

    def predict_proba(self, features):
        prediction = self.predict(features)
        if prediction == 1:
            return np.array([[0.1, 0.9]])  # 90% confidence it's phishing
        else:
            return np.array([[0.9, 0.1]])  # 90% confidence it's legitimate


# Feature extraction function
def get_features(url):
    features = {}
    features['url'] = url
    features['url_length'] = len(url)

    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        # Check if URL uses an IP address
        is_ip = 1 if (hostname and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname)) else 0
        features['has_ip'] = is_ip

        # Count subdomains
        if hostname and not is_ip:
            subdomains = hostname.split('.')
            features['num_subdomains'] = len(subdomains) - 2
        else:
            features['num_subdomains'] = 0

        # Check for suspicious keywords
        suspicious_keywords = ['login', 'secure', 'verify', 'confirm', 'account', 'security']
        features['suspicious_keywords'] = 0
        if hostname:
            for keyword in suspicious_keywords:
                if keyword in hostname.lower():
                    features['suspicious_keywords'] += 1

    except:
        features['has_ip'] = 0
        features['num_subdomains'] = 0
        features['suspicious_keywords'] = 0

    # Count special characters
    features['num_special_chars'] = url.count('@') + url.count('?') + url.count('=') + url.count('-')

    return features


# Initialize the model
model = SimplePhishingDetector()

# Create the main interface
st.title("🛡️ Financial PhishGuard")
st.markdown("""
**An AI-powered tool that analyzes websites to detect financial phishing attempts.**
Paste a URL below to check its safety.
""")

# Create a text input for the user
url_input = st.text_input("**Enter the URL to analyze:**", placeholder="e.g., https://www.example.com/login")

if url_input:
    # Add a spinning progress indicator while analyzing
    with st.spinner('Analyzing URL... This may take a few seconds.'):
        try:
            # Extract features from the URL
            features = get_features(url_input)

            # Make a prediction
            probability = model.predict_proba(features)[0]
            prediction = model.predict(features)

            # Display the results
            st.subheader("🔍 Analysis Result")

            if prediction == 0:
                st.success(f"✅ **LEGITIMATE** (Confidence: {probability[0] * 100:.1f}%)")
            else:
                st.error(f"🚨 **PHISHING THREAT DETECTED!** (Confidence: {probability[1] * 100:.1f}%)")
                st.warning("**Do not enter any personal or financial information on this site!**")

            # Show a detailed breakdown of the features
            st.subheader("📊 Extracted Features")
            feature_df = pd.DataFrame([features])
            st.dataframe(feature_df.T.rename(columns={0: 'Value'}))

        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")

# Add a sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This tool analyzes websites to detect potential phishing attempts by examining:
    - **URL structure** (length, special characters)
    - **Domain information** (IP address usage)
    - **Suspicious keywords** in the domain name
    """)

    st.header("⚠️ Disclaimer")
    st.markdown("""
    This is a demonstration tool. While it can help identify potential threats, 
    it should not be your only source of truth for website safety.
    Always use caution when entering sensitive information online.
    """)

# Add some footer information
st.markdown("---")
st.caption("Built as a demonstration project using Python and Streamlit")