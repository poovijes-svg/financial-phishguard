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
        if hasattr(features, 'to_dict'):
            features = features.to_dict()

        # Extract feature values
        url_length = features.get('url_length', 0)
        has_ip = features.get('has_ip', 0)
        num_special_chars = features.get('num_special_chars', 0)
        suspicious_keywords = features.get('suspicious_keywords', 0)
        num_subdomains = features.get('num_subdomains', 0)

        # Advanced rule-based detection with weighted scoring
        score = 0

        # 1. URL length (phishing URLs are often longer)
        if url_length > 50:
            score += 1
        if url_length > 75:
            score += 2  # Extra points for very long URLs

        # 2. IP address (highly suspicious)
        if has_ip == 1:
            score += 4  # Very strong indicator

        # 3. Special characters (common in phishing)
        if num_special_chars > 3:
            score += 2
        if num_special_chars > 6:
            score += 2  # Extra points for many special chars

        # 4. Suspicious keywords (very important)
        if suspicious_keywords > 0:
            score += suspicious_keywords * 2  # Weighted by count

        # 5. Subdomain count (phishing sites often use many subdomains)
        if num_subdomains > 2:
            score += 2

        # 6. Check for brand names in suspicious contexts
        brand_names = ['paypal', 'bank', 'facebook', 'google', 'apple', 'amazon', 'microsoft']
        url_lower = features.get('url', '').lower()
        for brand in brand_names:
            if brand in url_lower:
                score += 3  # Strong indicator of brand impersonation
                break

        # Decision threshold (adjust as needed)
        return 1 if score >= 6 else 0

    def predict_proba(self, features):
        prediction = self.predict(features)
        # Convert score to probability (simple mapping)
        if prediction == 1:
            return np.array([[0.2, 0.8]])  # 80% confidence it's phishing
        else:
            return np.array([[0.8, 0.2]])  # 80% confidence it's legitimate


# Initialize the model immediately after its definition
model = SimplePhishingDetector()


# Simple feature extraction function
def get_features(url):
    features = {}

    # Store the original URL for brand detection
    features['url'] = url

    # Existing features
    features['url_length'] = len(url)

    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        # IP address check
        is_ip = 1 if (hostname and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname)) else 0
        features['has_ip'] = is_ip

        # Count subdomains
        if hostname and not is_ip:
            subdomains = hostname.split('.')
            features['num_subdomains'] = len(subdomains) - 2  # Subtract domain and TLD
        else:
            features['num_subdomains'] = 0

        # Check for suspicious keywords
        suspicious_keywords = ['login', 'secure', 'verify', 'confirm', 'account', 'bank', 'paypal', 'facebook']
        features['suspicious_keywords'] = 0
        if hostname:
            for keyword in suspicious_keywords:
                if keyword in hostname.lower():
                    features['suspicious_keywords'] += 1

    except:
        features['has_ip'] = 0
        features['num_subdomains'] = 0
        features['suspicious_keywords'] = 0

    # Special characters count
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
    # Add a spinning progress indicator while analyzing
    with st.spinner('Analyzing URL... This may take a few seconds.'):
        try:
            # Extract features from the URL
            features = get_features(url_input)

            # DEBUG: Show extracted features
            st.subheader("🔍 Debug: Extracted Features")
            st.write("These are the features extracted from the URL:")
            st.json(features)

            # Calculate and show the detection score
            if hasattr(model, 'predict'):
                score = 0
                url_length = features.get('url_length', 0)
                has_ip = features.get('has_ip', 0)
                num_special_chars = features.get('num_special_chars', 0)
                suspicious_keywords = features.get('suspicious_keywords', 0)
                num_subdomains = features.get('num_subdomains', 0)

                # Apply the same scoring logic as in your predict method
                if url_length > 50: score += 1
                if url_length > 75: score += 2
                if has_ip == 1: score += 4
                if num_special_chars > 3: score += 2
                if num_special_chars > 6: score += 2
                if suspicious_keywords > 0: score += suspicious_keywords * 2
                if num_subdomains > 2: score += 2

                # Check for brand names
                brand_names = ['paypal', 'bank', 'facebook', 'google', 'apple', 'amazon', 'microsoft']
                url_lower = features.get('url', '').lower()
                for brand in brand_names:
                    if brand in url_lower:
                        score += 3
                        break

                st.write(f"Detection score: {score}/16")
                st.write("Threshold for phishing: ≥6")

            # Create a DataFrame for the features
            feature_df = pd.DataFrame([features])

            # Make a prediction
            probability = model.predict_proba(feature_df)[0]
            prediction = model.predict(feature_df)[0]

            # Display the results
            st.subheader("🔍 Analysis Result")

            if prediction == 0:
                st.success(f"✅ **LEGITIMATE** (Confidence: {probability[0] * 100:.1f}%)")
            else:
                st.error(f"🚨 **PHISHING THREAT DETECTED!** (Confidence: {probability[1] * 100:.1f}%)")
                st.warning("**Do not enter any personal or financial information on this site!**")

            # Show a detailed breakdown of the features
            st.subheader("📊 Extracted Features")
            st.write("Here are the characteristics we analyzed:")
            st.dataframe(feature_df.T.rename(columns={0: 'Value'}))

        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
# Add some information
with st.sidebar:
    st.header("About")
    st.markdown("This tool analyzes URLs for potential phishing attempts using simple heuristics.")