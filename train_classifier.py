import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

# Load your dataset
data = pd.read_csv("email_data.csv")

# Combine subject and sender
data["text"] = data["subject"] + " " + data["sender"]

# Use plain labels without emoji (optional for cleaner ML)
data["label"] = data["label"].str.replace("✅ ", "").str.replace("⚫ ", "").str.strip()

# Split data
X_train, X_test, y_train, y_test = train_test_split(data["text"], data["label"], test_size=0.2, random_state=42)

# Build model pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

# Train model
model.fit(X_train, y_train)

# Save model to file
joblib.dump(model, "email_classifier.joblib")

print("✅ Model trained and saved to email_classifier.joblib")
