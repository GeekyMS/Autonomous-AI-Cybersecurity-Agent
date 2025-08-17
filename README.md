# Autonomous AI Cybersecurity Agent

This project is an autonomous agent for real-time network security analysis. It uses a machine learning model and a large language model (LLM) to detect, analyze, and report on potential cybersecurity threats as they happen.

## Overview

The system captures live network traffic, processes it into flows, and uses a trained XGBoost model to classify each flow as either benign or malicious. For flows identified as potential threats, a large language model provides a detailed analysis, explanation, and recommendation. The results are then streamed to a live, dark-mode dashboard for monitoring.

## Features

  * **Real-time Packet Sniffing**: Captures live network traffic for immediate analysis.
  * **Flow Analysis**: Groups packets into flows and extracts key features for classification.
  * **ML-Based Threat Detection**: Uses a trained XGBoost model to classify network flows and identify potential threats with a confidence score.
  * **LLM-Powered Threat Explanation**: For each potential threat, a large language model provides a detailed, human-readable analysis of the threat.
  * **Live Cybersecurity Dashboard**: A React-based web interface that displays detected threats in real-time, color-coded by threat level.

## How It Works

1.  **Packet Sniffing**: The `sniff.py` script captures network packets in real-time.
2.  **Flow Extraction**: The captured packets are grouped into flows by the `flow.py` script, which also extracts features like flow duration, total packets, and bytes per second.
3.  **Classification**: The extracted features are fed into a pre-trained XGBoost model in `classify.py`, which predicts whether the flow is malicious and provides a confidence score.
4.  **LLM Analysis**: If a threat is detected, the `explain.py` script uses a large language model to provide a detailed analysis.
5.  **Backend Server**: A Flask server (`server.py`) streams the analysis results to the frontend via Server-Sent Events (SSE).
6.  **Frontend Dashboard**: A React application (`cybersecurity-dashboard/`) receives the data and displays it on a live, auto-updating dashboard.

## Getting Started

### Prerequisites

  * Python 3.x
  * Node.js and npm
  * An OpenAI API key (for LLM analysis)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/geekyms/autonomous-ai-cybersecurity-agent.git
    cd autonomous-ai-cybersecurity-agent
    ```

2.  **Set up the backend:**

      * Install Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```
      * **Create a `.env` file** in the root directory of the project. This is crucial for securely storing your API key.
      * Add your OpenAI API key to the `.env` file like this:
        ```
        OPENAI_API_KEY="your_openai_api_key_here"
        ```

3.  **Set up the frontend:**

    ```bash
    cd cybersecurity-dashboard
    npm install
    ```

### Running the Application

1.  **Start the backend server:**

      * From the root directory, run:
        ```bash
        python server.py
        ```

2.  **Start the frontend development server:**

      * In a new terminal, navigate to the `cybersecurity-dashboard` directory and run:
        ```bash
        npm run dev
        ```

3.  Open your browser and navigate to `http://localhost:5173` to view the dashboard.