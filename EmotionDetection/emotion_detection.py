"""Detect emotions using the Skills Network Watson NLP service."""

import json

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the dominant emotion."""
    response = requests.post(
        URL,
        headers=HEADERS,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=30,
    )
    if response.status_code == 400:
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))

    response.raise_for_status()
    emotions = json.loads(response.text)["emotionPredictions"][0]["emotion"]
    result = {name: emotions[name] for name in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
