"""Testes unitários para o pacote EmotionDetection e o servidor Flask."""

import unittest

from EmotionDetection import emotion_detector
from server import app


class EmotionDetectionTests(unittest.TestCase):
    """Conjunto de testes para a aplicação de detecção de emoções."""

    def test_emotion_detector_returns_formatted_output(self):
        """Verifica se a saída da função tem o formato esperado."""
        result = emotion_detector('Eu estou muito feliz hoje')
        self.assertIsInstance(result, dict)
        self.assertEqual(result['input_text'], 'Eu estou muito feliz hoje')
        self.assertIn('emotions', result)
        self.assertIn('dominant_emotion', result)
        self.assertIn('confidence', result)
        self.assertIsInstance(result['emotions'], dict)
        self.assertSetEqual(
            set(result['emotions'].keys()),
            {'anger', 'disgust', 'fear', 'joy', 'sadness'},
        )
        self.assertGreaterEqual(result['confidence'], 0.0)

    def test_emotion_detector_raises_error_for_blank_input(self):
        """Verifica que uma entrada vazia retorna erro de validação."""
        with self.assertRaises(ValueError):
            emotion_detector('   ')

    def test_emotion_detection_package_import(self):
        """Verifica a importação do pacote EmotionDetection."""
        self.assertTrue(hasattr(__import__('EmotionDetection'), 'emotion_detector'))

    def test_flask_blank_input_returns_400(self):
        """Verifica que o servidor Flask responde com 400 para texto em branco."""
        client = app.test_client()
        response = client.post('/emotionDetector', json={'text': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Invalid input! Try again.')


if __name__ == '__main__':
    unittest.main()
