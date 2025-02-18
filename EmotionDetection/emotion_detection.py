import requests
import json

def emotion_detector(text_to_analyze):
    # Return default for blank input
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    data = {"raw_document": {"text": text_to_analyze}}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        # Handle API errors
        if response.status_code != 200:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }

        json_response = response.json()
        emotions = json_response['emotionPredictions'][0]['emotion']
        
        # Extract scores
        anger = emotions['anger']
        disgust = emotions['disgust']
        fear = emotions['fear']
        joy = emotions['joy']
        sadness = emotions['sadness']
        
        # Find dominant emotion
        emotion_scores = [anger, disgust, fear, joy, sadness]
        emotion_names = ['anger', 'disgust', 'fear', 'joy', 'sadness']
        dominant_index = emotion_scores.index(max(emotion_scores))
        
        return {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness,
            'dominant_emotion': emotion_names[dominant_index]
        }

    except Exception as e:
        print(f"Error: {e}")
        return None