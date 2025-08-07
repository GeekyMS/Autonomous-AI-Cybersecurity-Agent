import pickle
import pandas as pd

model = None

def load_model():
    global model
    try:
        with open('cybersecurity_model.pkl', 'rb') as f:
            model = pickle.load(f)
            print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

def make_prediction(input_data):
    if model is None:
        load_model()
    
    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0]

    confidence = probability[int(prediction)]

    return prediction, confidence

def determine_threat_level(prediction, confidence):
    if prediction == 0:
        if confidence > 0.8:
            return "LOW"
        else:
            return "MEDIUM"
    else:
        if confidence > 0.9:
            return "CRITICAL"
        elif confidence > 0.75:
            return "HIGH"
        else:
            return "MEDIUM"