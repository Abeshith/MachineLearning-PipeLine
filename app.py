from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model on startup
try:
    model = joblib.load("artifacts/model_trainer/model.joblib")
    print("Model loaded successfully")
except:
    model = None
    print("Model not found - using fallback")

def prepare_features(sex, age, height, weight, duration, heart_rate, body_temp):
    """Prepare 11 features for model prediction"""
    sex_numeric = 1 if sex.lower() == 'male' else 0
    bmi = weight / ((height / 100) ** 2)
    met_estimate = (heart_rate - 60) / 20 + 1
    estimated_calories_per_min = met_estimate * weight * 3.5 / 200
    age_weight = age * weight
    heart_temp = heart_rate * body_temp
    
    return np.array([[sex_numeric, age, height, weight, duration, heart_rate, 
                     body_temp, bmi, estimated_calories_per_min, age_weight, heart_temp]])

def fallback_calories(sex, age, height, weight, duration, heart_rate):
    """Simple fallback calculation"""
    if sex == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    met = 6.0 if heart_rate < 140 else 8.0
    calories_per_minute = (met * weight * 3.5) / 200
    return round(calories_per_minute * duration, 2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        sex = request.form.get('sex', '').lower()
        age = float(request.form.get('age', 0))
        height = float(request.form.get('height', 0))
        weight = float(request.form.get('weight', 0))
        duration = float(request.form.get('duration', 0))
        heart_rate = float(request.form.get('heart_rate', 0))
        body_temp = float(request.form.get('body_temp', 0))
        
        # Prepare features and predict
        features = prepare_features(sex, age, height, weight, duration, heart_rate, body_temp)
        
        if model is not None:
            prediction = model.predict(features)[0]
            prediction = max(0, round(prediction, 2))
        else:
            prediction = fallback_calories(sex, age, height, weight, duration, heart_rate)
        
        return jsonify({'success': True, 'prediction': prediction})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
