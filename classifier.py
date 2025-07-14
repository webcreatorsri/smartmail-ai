# classifier.py
import joblib
import os

# Load model once
model = joblib.load("email_classifier.joblib")

def classify_email(subject, sender):
    if not subject and not sender:
        return "❌ Not Important"
    
    
    
    text = f"{subject} {sender}"
    prediction = model.predict([text])[0]
   
    if prediction.lower() == "important":
        return "✅ Important"
    else:
        return "❌ Not Important"

