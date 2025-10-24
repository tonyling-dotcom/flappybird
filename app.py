from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# High score file
HIGH_SCORE_FILE = 'highscore.json'

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as f:
            return json.load(f).get('high_score', 0)
    return 0

def save_high_score(score):
    current_high_score = load_high_score()
    if score > current_high_score:
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump({'high_score': score}, f)
        return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config')
def get_config():
    with open('levels.json', 'r') as f:
        config = json.load(f)
    return jsonify(config)

@app.route('/api/highscore', methods=['GET'])
def get_high_score():
    return jsonify({'high_score': load_high_score()})

@app.route('/api/highscore', methods=['POST'])
def update_high_score():
    data = request.get_json()
    score = data.get('score', 0)
    is_new_high = save_high_score(score)
    return jsonify({
        'success': True,
        'is_new_high': is_new_high,
        'high_score': load_high_score()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

