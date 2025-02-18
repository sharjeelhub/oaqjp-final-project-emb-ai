from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])  # Changed from POST to GET
def emotion_detector_endpoint():
    # Get text from URL parameter (not JSON body)
    text = request.args.get('textToAnalyze', '')  # Changed from request.json
    
    if not text.strip():
        return jsonify({"error": "Invalid text! Please try again!"}), 400
    
    analysis = emotion_detector(text)
    
    if not analysis or analysis['dominant_emotion'] is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400
    
    # Format response
    response = (
        f"For the given statement, the system response is "
        f"'anger': {analysis['anger']}, "
        f"'disgust': {analysis['disgust']}, "
        f"'fear': {analysis['fear']}, "
        f"'joy': {analysis['joy']} and "
        f"'sadness': {analysis['sadness']}. "
        f"The dominant emotion is {analysis['dominant_emotion']}."
    )
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)