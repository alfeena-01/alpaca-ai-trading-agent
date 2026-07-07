# CardioPredict - Heart Disease Prediction System

## 🏥 Overview

**CardioPredict** is an advanced machine learning-powered web application that predicts the risk of heart disease based on patient health metrics. The system uses a **Gaussian Naive Bayes** model trained on comprehensive medical data to provide accurate risk assessments.

> **⚠️ Medical Disclaimer:** This application is for educational and research purposes only. Predictions should not be considered as medical advice. Always consult with a qualified healthcare professional for accurate diagnosis and treatment.

---

## ✨ Features

- 🎯 **Accurate Predictions**: Uses Gaussian Naive Bayes ML model trained on real medical data
- 💫 **Beautiful UI**: Modern, responsive, and user-friendly interface with intuitive form organization
- 📱 **Fully Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- 🔒 **Data Privacy**: All predictions are processed locally on your server
- 📊 **Comprehensive Inputs**: Evaluates 13 important cardiac health indicators
- ⚡ **Fast Processing**: Real-time prediction results
- 🎨 **Professional Design**: Clean, modern interface with smooth animations and gradients

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the repository**
   ```bash
   cd path/to/heart
   ```

2. **Install required dependencies**
   ```bash
   pip install flask pandas scikit-learn
   ```

3. **Ensure you have the dataset**
   - The `heart.csv` file should be in the root directory
   - This dataset contains historical heart disease data used to train the model

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   - Open your browser and navigate to: `http://localhost:5000`
   - You should see the CardioPredict interface

---

## 📋 Input Parameters

The application collects 13 medical parameters organized in intuitive sections:

### Demographic Information
- **Age**: Patient age in years (18-120)
- **Sex**: Gender (Female=0, Male=1)

### Cardiac Symptoms & History
- **Chest Pain Type**: 
  - 0: Typical Angina
  - 1: Atypical Angina
  - 2: Non-anginal Pain
  - 3: Asymptomatic
- **Exercise Induced Angina**: Whether chest pain occurs with exercise (No=0, Yes=1)

### Blood Pressure & Cholesterol
- **Resting Blood Pressure**: In mmHg
- **Serum Cholesterol**: In mg/dl

### Metabolic & Electrical Indicators
- **Fasting Blood Sugar**: Whether > 120 mg/dl (No=0, Yes=1)
- **Resting Electrocardiogram**:
  - 0: Normal
  - 1: ST Abnormality
  - 2: LV Hypertrophy

### Heart Rate & ST Segment
- **Maximum Heart Rate Achieved**: In beats per minute (bpm)
- **ST Depression**: Induced by exercise (continuous value)

### Advanced Cardiac Indicators
- **ST Segment Slope**:
  - 0: Upsloping
  - 1: Flat
  - 2: Downsloping
- **Number of Major Vessels**: Colored by fluoroscopy (0-3)
- **Thalassemia**:
  - 0: Normal
  - 1: Fixed Defect
  - 2: Reversible Defect

---

## 🎯 How to Use

1. **Fill in Patient Information**
   - Start with demographic information
   - Progress through each section systematically
   - Use dropdown menus for categorical values
   - Use number inputs for continuous measurements

2. **Submit the Form**
   - Click the **"Predict Risk"** button to analyze the patient data
   - The AI model will process the inputs instantly

3. **Interpret Results**
   - ✅ **Low Risk**: Patient is unlikely to have heart disease
   - ⚠️ **High Risk**: Patient might have heart disease; medical consultation is strongly recommended

4. **Clear Form**
   - Use the **"Clear Form"** button to reset all fields for a new patient

---

## 🧠 Machine Learning Model

### Algorithm: Gaussian Naive Bayes

**Why Gaussian Naive Bayes?**
- Fast training and prediction
- Works well with continuous variables
- Probabilistic model with interpretable results
- Efficient for medical datasets

### Model Performance
- **Training Set Accuracy**: ~85-90% (varies with data splits)
- **Test Set Accuracy**: ~80-85%
- **Dataset Size**: 303 patients with 13 features

### Training Process
```python
# Data splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = GaussianNB()
model.fit(X_train, y_train)
```

---

## 📁 Project Structure

```
heart/
├── app.py                 # Flask application & ML model
├── heart.csv             # Dataset for model training
├── README.md             # This file
├── templates/
│   └── index.html        # HTML template with form and results
└── static/
    └── style.css         # Professional CSS styling
```

### File Descriptions

- **app.py**: 
  - Loads and trains the Gaussian Naive Bayes model
  - Defines Flask routes for web interface
  - Handles form submissions and predictions

- **heart.csv**: 
  - UCI Heart Disease Dataset
  - Contains 303 patient records
  - 13 clinical features + target variable

- **index.html**: 
  - Responsive HTML form with organized sections
  - Displays prediction results
  - Uses Font Awesome icons for better UX

- **style.css**: 
  - Modern gradient backgrounds
  - Smooth animations and transitions
  - Mobile-responsive grid layout
  - Professional color scheme

---

## 🛠️ Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.x** | Backend programming language |
| **Flask** | Lightweight web framework |
| **Pandas** | Data manipulation and analysis |
| **Scikit-learn** | Machine learning library |
| **HTML5** | Semantic markup for forms |
| **CSS3** | Modern styling with flexbox & grid |
| **Font Awesome 6.4** | Icon library |

---

## 🎨 UI/UX Highlights

- **Modern Design**: Linear gradients, smooth transitions, and professional color palette
- **Organized Form**: Inputs grouped into 7 logical sections with clear legends
- **Visual Feedback**: Hover effects, focus states, and animated results
- **Accessibility**: Semantic HTML, proper labels, and clear instructions
- **Responsive**: Adapts beautifully to all screen sizes (mobile to desktop)
- **Performance**: Lightweight CSS with no external dependencies (except Font Awesome)

### Color Scheme
- **Primary Red**: `#e74c3c` - Heart disease warnings
- **Secondary Blue**: `#3498db` - Secondary actions
- **Success Green**: `#27ae60` - Positive results
- **Light Gray**: `#f8f9fa` - Backgrounds

---

## 📊 Data Source

**UCI Heart Disease Dataset**
- Source: UCI Machine Learning Repository
- Samples: 303 patients
- Features: 13 clinical variables
- Target: Binary classification (0=No disease, 1=Disease present)
- Attributes: Age, Sex, Chest Pain, Blood Pressure, Cholesterol, Heart Rate, etc.

---

## 🔧 Configuration & Customization

### Changing the Model
To use a different ML algorithm, edit `app.py`:

```python
# Replace Gaussian Naive Bayes with another model
from sklearn.ensemble import RandomForestClassifier

# model = GaussianNB()  # Old model
model = RandomForestClassifier(n_estimators=100)  # New model
model.fit(X_train, y_train)
```

### Modifying Styling
Edit `static/style.css` to customize:
- Colors (update CSS variables in `:root`)
- Fonts and typography
- Spacing and layout
- Animations and transitions

### Adding More Features
Edit `templates/index.html` to add more input fields and update `app.py` accordingly.

---

## 🐛 Troubleshooting

### Issue: Flask server won't start
**Solution**: 
```bash
pip install --upgrade flask
python app.py
```

### Issue: "heart.csv not found" error
**Solution**: 
- Ensure `heart.csv` is in the same directory as `app.py`
- Check file name spelling and format

### Issue: Predictions seem inaccurate
**Possible causes**:
- Invalid input values outside normal ranges
- Data not normalized properly
- Model needs retraining on fresh data
- Check that input features match the training dataset

### Issue: Page styling looks broken
**Solution**:
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- Clear browser cache
- Ensure Font Awesome CDN is accessible

---

## 📈 Model Training Details

### Train/Test Split
- **Training Set**: 80% of data (243 samples)
- **Test Set**: 20% of data (60 samples)
- **Random State**: 42 (for reproducibility)

### Model Evaluation Metrics
- **Accuracy**: Overall correct predictions
- **Precision**: True positives vs all positive predictions
- **Recall**: True positives vs all actual positives
- **F1-Score**: Harmonic mean of precision and recall

### Feature Scaling
- Gaussian Naive Bayes assumes normal distribution
- Features are NOT scaled (model is scale-invariant)
- This simplifies the pipeline and improves interpretability

---

## 🚀 Deployment

### Local Development
```bash
python app.py
# App runs on http://localhost:5000
```

### Production Deployment

**Using Gunicorn**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

**Using Heroku**:
1. Create `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

3. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

**Using Docker**:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
```

---

## 📝 API Reference

### POST /predict

**Request**:
```
Form Data:
- age: number
- sex: 0|1
- cp: 0|1|2|3
- trestbps: number
- chol: number
- fbs: 0|1
- restecg: 0|1|2
- thalach: number
- exang: 0|1
- oldpeak: decimal
- slope: 0|1|2
- ca: 0|1|2|3
- thal: 0|1|2
```

**Response**:
- HTML page with prediction result
- Message indicates risk level and recommendation

---

## 📚 Learning Resources

- [Gaussian Naive Bayes Documentation](https://scikit-learn.org/stable/modules/naive_bayes.html#gaussian-naive-bayes)
- [Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/Heart+Disease)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn Guide](https://scikit-learn.org/stable/)

---

## 🤝 Contributing

To improve this project:

1. Improve model accuracy with different algorithms
2. Add more medical parameters
3. Implement data visualization (charts, graphs)
4. Add patient history tracking
5. Integrate with real medical databases
6. Implement user authentication

---

## ⚖️ License

This project is provided as-is for educational purposes.

---

## 👨‍⚕️ Medical Disclaimer

**IMPORTANT NOTICE:**

This CardioPredict application is a machine learning model trained on historical data and is provided **FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY**. It is:

- ❌ **NOT** a substitute for professional medical advice
- ❌ **NOT** a diagnostic tool
- ❌ **NOT** approved by medical regulatory bodies
- ❌ **NOT** to be used for clinical decision-making

**ALWAYS:**
- 🩺 Consult with a qualified healthcare professional for medical concerns
- 📋 Use actual medical tests and examinations for diagnosis
- ⚠️ Never rely solely on this application for health decisions

**Liability**: The creators of this application are not liable for any damages, health consequences, or decisions made based on the predictions of this system.

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Check the Troubleshooting section above
- Review Flask and Scikit-learn documentation
- Verify your dataset format matches the UCI Heart Disease Dataset

---

## 🎓 Educational Value

This project demonstrates:
- ✅ Machine learning model implementation
- ✅ Web application development with Flask
- ✅ Data science workflows
- ✅ Responsive web design
- ✅ Form validation and data handling
- ✅ Model deployment on the web

Perfect for learning:
- Python programming
- Machine learning fundamentals
- Web development
- Medical AI applications
- Full-stack development

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Active Development

---

*Remember: Health is wealth. When in doubt, consult a doctor! 💚*
