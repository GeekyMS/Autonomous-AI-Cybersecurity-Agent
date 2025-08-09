import openai
import json

class ThreatAnalyzer:
    def __init__(self, key):
        self.client = openai.OpenAI(api_key=key)
    
    def _get_llm_response(self, prompt):

        try:
            response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            raise
    
    def _default_safe_response(self, ml_prediction, ml_confidence, threat_level):

        return {
            "llm_assessment": {
                "prediction": ml_prediction, 
                "confidence": ml_confidence,
                "threat_level": threat_level,
                "attack_type": "Analysis Failed"
            },
            "ml_comparison": {
                "agrees_with_ml": True,
                "reasoning": "LLM analysis failed - using ML model result"
            },
            "explanations": {
                "technical": f"ML model classified as {'MALICIOUS' if ml_prediction == 1 else 'BENIGN'} with {ml_confidence:.3f} confidence. LLM validation unavailable.",
                "user_friendly": "Automatic analysis temporarily unavailable. Using backup classification."
            },
            "recommendations": {
                "immediate_actions": ["Manual review recommended - automated analysis failed"],
                "priority": "Medium"
            }
        }
    
    def analyze_flow(self, flow_data, ml_prediction, ml_confidence, threat_level):
        prompt = f"""You are a cybersecurity analyst analyzing network traffic flows.

    NETWORK FLOW DATA:
    - Duration: {flow_data['flow_duration']} seconds
    - Total Packets: {flow_data['total_packets']}
    - Packets/Second: {flow_data['packets_per_second']}
    - Total Bytes: {flow_data['total_bytes']}
    - Bytes/Second: {flow_data['bytes_per_second']}

    ML MODEL ASSESSMENT:
    - Prediction: {'MALICIOUS' if ml_prediction == 1 else 'BENIGN'}
    - Confidence: {ml_confidence:.3f}
    - Threat Level: {threat_level}

    CONFIDENCE SCALE:
    - 0.9-1.0: Very certain
    - 0.7-0.9: Confident  
    - 0.5-0.7: Moderately certain
    - 0.3-0.5: Uncertain
    - 0.0-0.3: Very uncertain

    TASK: Analyze this traffic independently and provide your assessment.

    RETURN ONLY VALID JSON:
    {{
    "llm_assessment": {{
        "prediction": 0 or 1,
        "confidence": 0.0-1.0,
        "threat_level": "LOW/MEDIUM/HIGH/CRITICAL",
        "attack_type": "specific type or 'Normal Traffic'"
    }},
    "ml_comparison": {{
        "agrees_with_ml": true/false,
        "reasoning": "why you agree or disagree"
    }},
    "explanations": {{
        "technical": "detailed analysis for SOC analysts",
        "user_friendly": "simple explanation for general users"
    }},
    "recommendations": {{
        "immediate_actions": ["action1", "action2"],
        "priority": "Immediate/High/Medium/Low"
    }}
    }}

CRITICAL: Return ONLY the JSON object. No additional text before or after."""


        try:
            response1 = self._get_llm_response(prompt)
            return json.loads(response1)
        except json.JSONDecodeError:

            try:
                response2 = self._get_llm_response(prompt + "\n\nIMPORTANT: Last response was invalid JSON. Return ONLY valid JSON with no additional text.")
                return json.loads(response2)
            except json.JSONDecodeError:

                return self._default_safe_response(ml_prediction, ml_confidence, threat_level)