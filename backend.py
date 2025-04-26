from flask import Flask, request, jsonify
from agents.autopipeline import AutoPipeline

app = Flask(__name__)
pipeline = AutoPipeline()  # load once

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_text = data.get('text', '')

    prediction = pipeline.predict(input_text)  # actual prediction
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
