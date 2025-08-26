# --- Flask Backend ---
from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load preprocessed data with 'Name', 'Platform', 'Genre', 'Global_Sales', and 'cluster'
data = pd.read_csv("final_clustered_games.csv")  # you need to create this from your final df

@app.route('/')
def home():
    game_names = sorted(data['Name'].unique())
    return render_template('index.html', game_names=game_names)

@app.route('/recommend', methods=['POST'])
def recommend():
    game_name = request.form.get('game_name')
    game_names = sorted(data['Name'].unique())

    if game_name not in data['Name'].values:
        return render_template('index.html', error="Game not found.", game_names=game_names)

    cluster_id = data[data['Name'] == game_name]['cluster'].values[0]
    recommended = data[
        (data['cluster'] == cluster_id) &
        (data['Name'] != game_name)
    ].sample(n=5)[['Name', 'Platform', 'Genre', 'Global_Sales']]

    return render_template('index.html',
                           game_name=game_name,
                           recommendations=recommended.to_dict(orient='records'),
                           game_names=game_names)

if __name__ == '__main__':
    app.run(debug=True)