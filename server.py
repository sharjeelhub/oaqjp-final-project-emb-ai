from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector
import locale  # Add this import
# Set locale to prevent number formatting issues
locale.setlocale(locale.LC_ALL, 'C')

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def emotion_analysis():
    text_to_analyze = request.args.get('textToAnalyze', '').strip()
    if not text_to_analyze:
        return jsonify({
            "error": "Invalid text! Please try again!",
            "response": None
        })
    analysis = emotion_detector(text_to_analyze)
    if not analysis or analysis.get('dominant_emotion') is None:
        return jsonify({
            "error": "Text analysis failed! Please try again.",
            "response": None
        })
    # Format numbers with forced decimal points
    def format_num(x):
        return locale.format_string("%.3f", x, grouping=False)
    response_message = (
        f"<div class='analysis-results'>"
        f"<div class='result-title'>Analysis Results:</div>"
        f"<div class='emotion-grid'>"
        f"<div class='emotion-item'><span>Anger:</span> <span class='emotion-value'>{format_num(analysis['anger'])}</span></div>"
        f"<div class='emotion-item'><span>Disgust:</span> <span class='emotion-value'>{format_num(analysis['disgust'])}</span></div>"
        f"<div class='emotion-item'><span>Fear:</span> <span class='emotion-value'>{format_num(analysis['fear'])}</span></div>"
        f"<div class='emotion-item'><span>Joy:</span> <span class='emotion-value'>{format_num(analysis['joy'])}</span></div>"
        f"<div class='emotion-item'><span>Sadness:</span> <span class='emotion-value'>{format_num(analysis['sadness'])}</span></div>"
        f"</div>"
        f"<div class='dominant-emotion-box'>"
        f"🏆 Dominant Emotion: <span class='dominant-emotion'>{analysis['dominant_emotion'].capitalize()}</span>"
        f"</div>"
        f"</div>"
    )
    return jsonify({
        "error": None,
        "response": response_message
    })
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
