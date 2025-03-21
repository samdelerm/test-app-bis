from flask import Flask, render_template, jsonify, request
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_matches')
def get_matches():
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get("https://app-rsk.onrender.com/get_matches")
            response.raise_for_status()
            matches = response.json()
            return jsonify(matches)
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur lors de la recuperation des matchs (tentative {attempt + 1}/{retries}): {e}")
            if attempt == retries - 1:
                return jsonify({"error": "Erreur lors de la recuperation des matchs apres plusieurs tentatives"}), 500

@app.route('/get_team_info')
def get_team_info():
    match_id = request.args.get('match_id')
    logging.info(f"Received match_id: {match_id}")  # Add this line to log the match_id
    try:
        response = requests.get(f"https://app-rsk.onrender.com/get_team_info?match_id={match_id}")
        response.raise_for_status()
        team_info = response.json()
        return jsonify(team_info)
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la recuperation des informations de l'equipe: {e}")
        return jsonify({"error": "Erreur lors de la recuperation des informations de l'equipe"}), 500

@app.route('/stop_reload')
def stop_reload():
    return jsonify({"message": "Reload stopped"}), 200

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", 1000, app)
