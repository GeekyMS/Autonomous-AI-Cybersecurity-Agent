from flask import Flask, Response
import time
import json
from datetime import datetime
import random
from flask_cors import CORS
from classify import load_model, make_prediction, determine_threat_level


app = Flask(__name__)
CORS(app, resources={r"/events": {"origins": "http://localhost:5173"}})
@app.route('/')
def index():
    return "Cybersecurity Dashboard Server - Visit /events for SSE stream"

@app.route('/events')
def events():
    def event_generator():
        while True:

            mock_features = {
                'flow_duration': random.uniform(0.1, 10),
                'total_packets': random.randint(10, 1000),
                'packets_per_second': random.uniform(10, 5000),
                'total_bytes': random.randint(100, 100000),
                'bytes_per_second': random.uniform(1000, 50000)
            }
            
            try:
                prediction, confidence = make_prediction(mock_features)
                threat_level = determine_threat_level(prediction, confidence)
                threat = {
                    "attack_type": "DDoS" if prediction == 1 else "Benign",
                    "ip": f"192.168.1.{random.randint(1, 255)}",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "confidence": round(float(confidence),2),
                    "threat_level": threat_level,
                    "is_mock": True 
                }
            except Exception as e:
                threat = {
                    "error": str(e),
                    "is_mock": True
                }

            sse_data = f"data: {json.dumps(threat)}\n\n"
            yield sse_data
            

            time.sleep(2)
    
    return Response(event_generator(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(port=5001)