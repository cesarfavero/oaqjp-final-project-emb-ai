"""Servidor Flask para o projeto Emotion Detector."""

from flask import Flask, jsonify, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)




@app.route('/', methods=['GET'])
def home() -> str:
    """Renderiza a página inicial com o formulário de detecção."""
    return render_template("index.html")


@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route() -> tuple[str, int]:
    """Processa o texto enviado e retorna a análise de emoções em formato de string."""
    payload = request.get_json(silent=True)
    if not payload or not isinstance(payload, dict):
        return jsonify(error='Invalid JSON payload.'), 400

    text = payload.get('text', '')
    if not isinstance(text, str) or not text.strip():
        return jsonify(error='Text input cannot be blank.'), 400

    try:
        result = emotion_detector(text)
    except ValueError as error:
        return jsonify(error=str(error)), 400

    response_string = (
        f"anger:{result['emotions']['anger']}, "
        f"disgust:{result['emotions']['disgust']}, "
        f"fear:{result['emotions']['fear']}, "
        f"joy:{result['emotions']['joy']}, "
        f"sadness:{result['emotions']['sadness']}, "
        f"dominant_emotion:{result['dominant_emotion']}"
    )
    return response_string, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
