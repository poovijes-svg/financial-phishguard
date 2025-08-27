# test_upgraded_model.py
import joblib
from features import get_features

# Load the supercharged model you just trained
model = joblib.load('model.joblib')

# Test it on a URL you haven't used before
test_url = "https://www.facebook.com/login"  # A legitimate login page
# test_url = "http://faceb00k-login.secure-auth.com" # You can test a fake one like this later

print(f"Testing URL: {test_url}")
features = get_features(test_url)
print("Extracted Features:", features)

# Make a prediction
prediction = model.predict([list(features.values())])
probability = model.predict_proba([list(features.values())])

# Show the result
if prediction[0] == 0:
    print(f"✅ Result: LEGITIMATE (Confidence: {probability[0][0]*100:.1f}%)")
else:
    print(f"🚨 Result: PHISHING THREAT (Confidence: {probability[0][1]*100:.1f}%)")

# Show the top reasons for the decision (using feature importances)
print("\nTop reasons for this decision:")
feature_names = list(features.keys())
importances = model.feature_importances_
# Combine feature names with their importance scores and sort them
feature_importance_list = list(zip(feature_names, importances))
feature_importance_list.sort(key=lambda x: x[1], reverse=True)  # Sort by importance, high to low

# Print the top 3 most important features for this prediction
for feature, importance in feature_importance_list[:3]:
    print(f" - '{feature}' was a key factor (Importance: {importance:.2%})")