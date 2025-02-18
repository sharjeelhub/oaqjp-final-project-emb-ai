import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    data = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json=data, headers=headers)
    
    # New formatting logic
    formatted = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }
    
    if response.status_code == 200:
        json_response = json.loads(response.text)
        emotions = json_response['emotion_predictions'][0]['emotion']
        
        formatted['anger'] = emotions['anger']
        formatted['disgust'] = emotions['disgust']
        formatted['fear'] = emotions['fear']
        formatted['joy'] = emotions['joy']
        formatted['sadness'] = emotions['sadness']
        
        # Find dominant emotion
        dominant = max(emotions.items(), key=lambda x: x[1])[0]
        formatted['dominant_emotion'] = dominant
    
    return formatted