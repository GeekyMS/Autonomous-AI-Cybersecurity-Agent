from flask import Flask, Response
import time
import json
from datetime import datetime
import random
from flask_cors import CORS
from classify import load_model, make_prediction, determine_threat_level
from sniff import PacketSniffer
from classify import make_prediction
from explain import ThreatAnalyzer
from config import Config


app = Flask(__name__)
CORS(app, resources={r"/events": {"origins": Config.CORS_ORIGINS}})
@app.route('/')
def index():
    return {
        "message": "Cybersecurity Dashboard API Server",
        "status": "running",
        "endpoints": {
            "events": "/events - SSE stream for real-time threat data",
            "health": "/health - Server health check",
            "shutdown": "/shutdown - Graceful server shutdown (POST)"
        },
        "frontend": "React app should connect to /events endpoint",
        "port": 5001
        }

@app.route('/events')
def events():

    sniffer = PacketSniffer()
    sniffer.start_sniffing()
    key = True if Config.OPENAI_API_KEY else False
    if not key:
        print("Warning: OPENAI_API_KEY not found in environment variables")
        print("LLM analysis will be disabled")


    def event_generator():
        while True:

            flow_features_list = sniffer.get_latest_packets()
            
            for features in flow_features_list:
                ip_address = features.pop('ip', 'NA')
                prediction, confidence = make_prediction(features)
                threat_level = determine_threat_level(prediction, confidence)
                

                llm_analysis = None
                if prediction == 1 and key:
                    analyzer = ThreatAnalyzer()
                    llm_analysis = analyzer.analyze_flow(features, prediction, confidence, threat_level)
                
                threat = {
                    "ip": ip_address,
                    "attack_type": "Malicious" if prediction == 1 else "Benign",
                    "confidence": round(float(confidence),2),
                    "threat_level": threat_level,
                    "llm_analysis": llm_analysis,
                    "flow_stats": sniffer.get_flow_stats(),
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "is_mock": False
                }
                
                yield f"data: {json.dumps(threat)}\n\n"
            
            time.sleep(5) 
    
    return Response(event_generator(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(port=Config.FLASK_PORT)