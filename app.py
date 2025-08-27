# app.py
import streamlit as st
import joblib
from features import get_features
import pandas as pd

# Set the page title and icon
st.set_page_config(
    page_title="Financial PhishGuard",
    page_icon="🛡️",
    layout="centered"
)


# Load your trained model
@st.cache_resource  # This decorator caches the model so it's only loaded once
def load_model():
    model = joblib.load('model.joblib')
    return model


model = load_model()

# Create the main interface
st.title("🛡️ Financial PhishGuard")
st.markdown("""
**An AI-powered tool that analyzes websites to detect financial phishing attempts.**
Paste a URL below to check its safety.
""")

# Create a text input for the user
url_input = st.text_input("**Enter the URL to analyze:**", placeholder="e.g., https://www.example.com/login")

if url_input:
    # Add a spinning progress indicator while the model is working
    with st.spinner('Analyzing URL... This may take a few seconds.'):
        # Extract features from the URL
        features = get_features(url_input)

        # Check if feature extraction was successful
        if features.get('domain_age_days') == -1:
            st.warning("⚠️ Could not retrieve full domain information. This may affect the result.")

        # Create a DataFrame for the features (for display and prediction)
        feature_df = pd.DataFrame([features])

        # Make a prediction
        try:
            prediction = model.predict(feature_df)[0]
            probability = model.predict_proba(feature_df)[0]

            # Display the results in a clear, visual way
            st.subheader("🔍 Analysis Result")

            if prediction == 0:
                st.success(f"**✅ LEGITIMATE** (Confidence: {probability[0] * 100:.1f}%)")
                st.balloons()  # Fun celebration effect
            else:
                st.error(f"**🚨 PHISHING THREAT DETECTED!** (Confidence: {probability[1] * 100:.1f}%)")
                st.warning("**Do not enter any personal or financial information on this site!**")

            # Show a detailed breakdown of the features
            st.subheader("📊 Detailed Analysis")
            st.write("Here are the key factors that contributed to this decision:")

            # Display the extracted features in a nice table
            st.dataframe(feature_df.T.rename(columns={0: 'Value'}))  # Transpose for better viewing

            # Show the most important features for this prediction
            st.subheader("🧠 Key Decision Factors")
            feature_names = feature_df.columns
            importances = model.feature_importances_

            # Create a list of (feature, importance, value) and sort by importance
            factors = []
            for i, (name, importance) in enumerate(zip(feature_names, importances)):
                value = feature_df.iloc[0][i]
                factors.append((name, importance, value))

            # Sort by importance (highest first) and show top 5
            factors.sort(key=lambda x: x[1], reverse=True)

            for i, (name, importance, value) in enumerate(factors[:5]):
                st.write(f"{i + 1}. **{name}** (Value: {value})")

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

# Add a sidebar with information and instructions
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This tool uses machine learning to detect fake financial websites by analyzing:
    - **URL structure** (length, special characters)
    - **Domain information** (age, IP address usage)
    - **Page content** (forms, input fields, password fields)

    The AI model was trained on known legitimate and phishing URLs.
    """)

    st.header("⚠️ Disclaimer")
    st.markdown("""
    This is a academic project. While designed to be accurate, it should not be your sole source of truth for website safety.
    Always use caution when entering sensitive information online.
    """)

    st.header("👨‍💻 How It Works")
    st.markdown("""
    1. Paste a URL in the main input field
    2. The system extracts over 10 different features
    3. A trained Random Forest model makes a prediction
    4. Results show with confidence percentage and reasoning
    """)

# Add some footer information
st.markdown("---")
st.caption("Built as a final year project using Python, Scikit-learn, and Streamlit. | Model Accuracy: XX.X%")
# Note: You can update the accuracy XX.X% after you calculate it from your model training