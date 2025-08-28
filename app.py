# app.py
import streamlit as st
import pandas as pd
import numpy as np

# Set the page title and icon
st.set_page_config(
    page_title="Financial PhishGuard",
    page_icon="🛡️",
    layout="centered"
)


# First, define a simple fallback model that will always be available
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


# Initialize model with the simple detector as a fallback
model = SimplePhishingDetector()

# Now try to import dependencies and load a better model if possible
try:
    from features import get_features
except ImportError:
    # Define a dummy get_features function if the import fails
    def get_features(url):
        return {'url_length': len(url), 'has_ip': 0, 'num_special_chars': 0}

try:
    import joblib

    # Try to load a pre-trained model
    try:
        model = joblib.load('model.joblib')
        st.success("✅ Loaded pre-trained model")
    except FileNotFoundError:
        st.warning("⚠️ No pre-trained model found. Using simple rule-based detector.")
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
except ImportError:
    st.warning("Joblib not available. Using simple rule-based detector.")

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

            # Create a DataFrame for the features
            feature_df = pd.DataFrame([features])

            # Make a prediction
            if hasattr(model, 'predict_proba'):
                probability = model.predict_proba(feature_df)[0]
                prediction = model.predict(feature_df)[0]
            else:
                # Fallback for simple model
                probability = model.predict_proba(features)[0]
                prediction = model.predict(features)

            # Display the results
            st.subheader("🔍 Analysis Result")

            if prediction == 0:
                st.success(f"**✅ LEGITIMATE** (Confidence: {probability[0] * 100:.1f}%)")
            else:
                st.error(f"**🚨 PHISHING THREAT DETECTED!** (Confidence: {probability[1] * 100:.1f}%)")
                st.warning("**Do not enter any personal or financial information on this site!**")

            # Show a detailed breakdown of the features
            st.subheader("📊 Extracted Features")
            st.write("Here are the characteristics we analyzed:")
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
    - **Page content** (forms, input fields)
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