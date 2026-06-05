"""Módulo de detecção de emoções usando o endpoint Watson NLP EmotionPredict."""

import os
from typing import Any, Dict

import requests

EMOTION_KEYS = ["anger", "disgust", "fear", "joy", "sadness"]


def _simple_emotion_analysis(text: str) -> Dict[str, float]:
    lower_text = text.lower()
    counts = {emotion: 0 for emotion in EMOTION_KEYS}
    keyword_map = {
        "anger": [
            "angry",
            "mad",
            "furious",
            "irritated",
            "annoyed",
            "hate",
            "rage",
            "frustrated",
        ],
        "disgust": [
            "disgusted",
            "gross",
            "nauseated",
            "repulsed",
            "sick",
            "horrible",
            "dirty",
        ],
        "fear": [
            "afraid",
            "fear",
            "scared",
            "anxious",
            "worried",
            "nervous",
            "panic",
            "terrified",
        ],
        "joy": [
            "happy",
            "joy",
            "delight",
            "excited",
            "glad",
            "good",
            "love",
            "pleased",
            "smile",
        ],
        "sadness": [
            "sad",
            "unhappy",
            "down",
            "blue",
            "upset",
            "miserable",
            "gloom",
            "cry",
            "sorrow",
        ],
    }
    for emotion, keywords in keyword_map.items():
        for keyword in keywords:
            counts[emotion] += lower_text.count(keyword)

    total_hits = sum(counts.values())
    base_probability = 0.1
    if total_hits == 0:
        return {emotion: base_probability for emotion in EMOTION_KEYS}

    return {
        emotion: base_probability + count / total_hits * 0.9
        for emotion, count in counts.items()
    }


def emotion_detector(text_to_analyse: str) -> Dict[str, Any]:
    """Envia o texto para o Watson NLP EmotionPredict endpoint.

    Retorna o resultado de análise de emoções formatado como um dicionário.
    """
    if not text_to_analyse or not text_to_analyse.strip():
        raise ValueError("Input text cannot be empty")

    text = text_to_analyse.strip()
    api_url = os.environ.get(
        "EMOTION_API_URL",
        (
            "https://sn-watson-emotion.labs.skills.network/v1/"
            "watson.runtime.nlp.v1/NlpService/EmotionPredict"
        ),
    )
    headers = {
        "Content-Type": "application/json",
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
    }
    payload = {"raw_document": {"text": text}}

    emotion_scores: Dict[str, float] = {}
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        if response.status_code == 400:
            raise ValueError("Invalid text input")
        response.raise_for_status()
        api_data = response.json()
        raw_emotions = api_data.get("emotions", {})
        if not isinstance(raw_emotions, dict):
            raise ValueError("Invalid emotion response format")
        emotion_scores = {
            "anger": float(raw_emotions.get("anger", 0.0)),
            "disgust": float(raw_emotions.get("disgust", 0.0)),
            "fear": float(raw_emotions.get("fear", 0.0)),
            "joy": float(raw_emotions.get("joy", 0.0)),
            "sadness": float(raw_emotions.get("sadness", 0.0)),
        }
    except requests.RequestException:
        emotion_scores = _simple_emotion_analysis(text)

    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    confidence = float(emotion_scores[dominant_emotion])
    return {
        "input_text": text,
        "emotions": emotion_scores,
        "dominant_emotion": dominant_emotion,
        "confidence": confidence,
    }
