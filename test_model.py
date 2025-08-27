# test_model.py
import joblib
import os

# Check if the file actually exists
if os.path.exists('model.joblib'):
    print("✅ SUCCESS: The 'model.joblib' file exists!")

    # Now try to load it
    try:
        model = joblib.load('model.joblib')
        print("✅ SUCCESS: The model was loaded without any errors!")
        print(f"Model type: {type(model)}")
        # This proves the file is valid and working.

    except Exception as e:
        print(f"❌ ERROR: Could not load the model. Error: {e}")
else:
    print("❌ ERROR: The 'model.joblib' file was not found.")
