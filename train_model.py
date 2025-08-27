# train_model.py
from features import get_features  # Import the function we just created
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Lists to hold our data and labels
data = []
labels = []

print("Reading good URLs...")
# Read the good URLs and extract features
with open('good_urls.txt', 'r') as f:
    for url in f.readlines():
        url = url.strip()  # Remove any extra spaces or newline characters
        if url:  # Make sure the URL is not empty
            features = get_features(url)
            data.append(features)
            labels.append(0)  # 0 for good
            print(f"Processed good URL: {url}")

print("Reading bad URLs...")
# Read the bad URLs and extract features
with open('bad_urls.txt', 'r') as f:
    for url in f.readlines():
        url = url.strip()  # Remove any extra spaces or newline characters
        if url:  # Make sure the URL is not empty
            features = get_features(url)
            data.append(features)
            labels.append(1)  # 1 for bad
            print(f"Processed bad URL: {url}")

# Create a DataFrame (like a spreadsheet) from the data
df = pd.DataFrame(data)
df['label'] = labels

# Save the dataset to a CSV file to examine it
df.to_csv('dataset.csv', index=False)
print("Dataset created with", len(df), "entries.")
print("\nFirst few rows of the dataset:")
print(df.head())  # Show the first 5 rows

# Check if we have enough data to train a model
if len(df) < 10:
    print("\nWarning: You have very little data. The model may not be accurate.")
    print("Please add more URLs to your good_urls.txt and bad_urls.txt files.")
else:
    # Split the data into features (X) and target (y)
    X = df.drop('label', axis=1)
    y = df['label']

    # Split into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train a Random Forest model
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Test the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.2%}")

    # Save the trained model to a file
    joblib.dump(model, 'model.joblib')
    print("Model saved as 'model.joblib'")

    # Show feature importances
    print("\nFeature Importances:")
    importances = model.feature_importances_
    feature_names = X.columns
    for i, imp in enumerate(importances):
        print(f"{feature_names[i]}: {imp:.2%}")