# Autonomous AI Cybersecurity Agent

This project is a work in progress. It aims to create an autonomous agent for network security analysis that uses machine learning and large language models (LLMs) to detect, analyze, and report on potential cybersecurity threats in real-time.

## Overview

The system captures network traffic, processes it into flows, and uses a trained machine learning model to classify each flow as either benign or malicious. For flows identified as potential threats, a large language model provides a detailed analysis, explanation, and recommendation. The results are then streamed to a live dashboard for monitoring.

## Features

* **Real-time Packet Sniffing**: Captures live network traffic for analysis.
* **Flow Analysis**: Groups packets into flows and extracts key features for classification.
* **ML-Based Threat Detection**: Uses a trained XGBoost model to classify network flows and identify potential threats.
* **LLM-Powered Threat Explanation**: For each potential threat, a large language model provides:
    * An assessment of the attack type.
    * A comparison with the ML model's prediction.
    * Technical and user-friendly explanations of the threat.
    * Recommendations for immediate action.
* **Live Cybersecurity Dashboard**: A React-based web interface that displays detected threats in real-time, color-coded by threat level.

## Project Status

This project is currently under development. The core features for packet sniffing, classification, and the display of mock data on the dashboard are in place. The integration of the LLM for detailed analysis is also a key feature.

## How It Works

1.  **Packet Sniffing**: The `sniff.py` script captures network packets in real-time.
2.  **Flow Extraction**: The captured packets are grouped into flows by the `flow.py` script, which also extracts features like flow duration, total packets, and bytes per second.
3.  **Classification**: The extracted features are fed into a pre-trained XGBoost model in `classify.py`, which predicts whether the flow is malicious and provides a confidence score.
4.  **LLM Analysis**: The `explain.py` script takes the flow data and the ML model's prediction and uses a large language model to provide a detailed, human-readable analysis of the threat.
5.  **Backend Server**: A Flask server (`server.py`) streams the analysis results to the frontend.
6.  **Frontend Dashboard**: A React application (`cybersecurity-dashboard/`) receives the data and displays it on a live dashboard.

## Getting Started

### Prerequisites

* Python 3.x
* Node.js and npm

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/geekyms/autonomous-ai-cybersecurity-agent.git](https://github.com/geekyms/autonomous-ai-cybersecurity-agent.git)
    cd autonomous-ai-cybersecurity-agent
    ```

2.  **Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Frontend dependencies:**
    ```bash
    cd cybersecurity-dashboard
    npm install
    ```

### Running the Application

1.  **Start the backend server:**
    ```bash
    python server.py
    ```

2.  **Start the frontend development server:**
    ```bash
    cd cybersecurity-dashboard
    npm run dev
    ```

3.  Open your browser and navigate to `http://localhost:5173` to view the dashboard.

## Future Work

* Implement a mechanism for retraining the model with new data.
* Expand the recommendation and automated response capabilities.