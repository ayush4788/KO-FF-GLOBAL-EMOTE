# Vercel's app.py

from flask import Flask, render_template, request, jsonify
import json
import os
import requests # Use requests to call your bot API

app = Flask(__name__)

# This is the public URL of your bot running on Railway/Render
BOT_API_BASE_URL = "https://your-bot-project-name.up.railway.app" # <--- IMPORTANT: Change this!
BOT_API_PORT = "30151" # The port your bot's Flask app is running on

@app.route('/')
def index():
    try:
        with open('emotes.json', 'r') as f:
            emotes = json.load(f)
        return render_template('index.html', emotes=emotes)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/send_emote', methods=['POST'])
def send_emote():
    try:
        data = request.get_json()
        team_code = data.get('team_code')
        emote_id = data.get('emote_id')
        uids = data.get('uids', [])

        if not all([team_code, emote_id, uids]):
            return jsonify({'message': 'Error: Missing data'}), 400

        # Build the parameters for the API call to your bot
        # http://.../join?uid1=...&uid2=...&emote_id=...&tc=...
        params = {
            'emote_id': emote_id,
            'tc': team_code
        }
        for i, uid in enumerate(uids):
            params[f'uid{i+1}'] = uid

        # Make the request to the bot running on Railway
        api_url = f"{BOT_API_BASE_URL}:{BOT_API_PORT}/join"
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status() # Raise an error for bad responses

        return jsonify({
            'message': 'Emote request sent successfully to the bot!',
            'api_response': response.json()
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'message': f'Error communicating with the bot API: {e}'}), 500
    except Exception as e:
        return jsonify({'message': f'An internal server error occurred: {e}'}), 500
