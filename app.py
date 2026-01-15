from flask import Flask, render_template, request, jsonify
from find_players import get_ratings_for_names

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ratings', methods=['POST'])
def ratings():
    data = request.get_json()
    if not data or 'names' not in data:
        return jsonify({'error': 'No names provided'}), 400
    
    names = data['names']
    # Filter out empty strings
    names = [n for n in names if n.strip()]
    
    # Process using the refactored logic
    results = get_ratings_for_names(names)
    
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
