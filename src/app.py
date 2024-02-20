from flask import Flask, request, jsonify
from flask_cors import CORS
from play_chsh import simulate_chsh_game  # Adjust this import based on your project structure
from .ebitCreator import create_entangled_pair, apply_alice_bob_operations, measure_and_get_results

app = Flask(__name__)
CORS(app)

@app.route('/play_chsh', methods=['POST'])
def play_chsh():
    data = request.json
    ruleset = data.get('ruleset', 'default')
    a_input = data.get('a_input')
    b_input = data.get('b_input')
    mode = data.get('mode', 'quantum')
    iterations = data.get('iterations', 1000)

    if a_input is None or b_input is None:
        return jsonify({'error': 'Missing inputs for players'}), 400

    win_count = 0

    for _ in range(iterations):
        outcome = simulate_chsh_game(a_input, b_input, mode)
        if outcome == "win":
            win_count += 1

    win_rate = (win_count / iterations) * 100

    return jsonify({
        'win_count': win_count,
        'total_games': iterations,
        'win_rate': win_rate,
        'mode': mode
    })

@app.route('/api/performOperation', methods=['POST'])
def perform_operation():
    data = request.json
    choice = data['choice']
    
    # Simplified example, adjust according to your actual logic
    qc = create_entangled_pair()
    qc = apply_alice_bob_operations(qc, choice)
    results = measure_and_get_results(qc)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)