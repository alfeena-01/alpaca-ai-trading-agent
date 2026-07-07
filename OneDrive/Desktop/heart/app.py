from flask import Flask, request, render_template
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

# Load dataset
df = pd.read_csv("heart.csv")
X = df.drop(columns=['target'])
y = df['target']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
NB = GaussianNB()
NB.fit(X_train, y_train)

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect form data in the correct feature order
    feature_order = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    data = [float(request.form[key]) for key in feature_order]
    
    # Make prediction
    prediction = NB.predict([data])[0]
    probabilities = NB.predict_proba([data])[0]
    
    # Calculate confidence
    confidence = max(probabilities) * 100

    if prediction == 1:
        result = f"⚠️ The patient might have heart disease, please consult a doctor. (Confidence: {confidence:.1f}%)"
    else:
        result = f"✅ The patient is unlikely to have heart disease. (Confidence: {confidence:.1f}%)"

    return render_template('index.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)
