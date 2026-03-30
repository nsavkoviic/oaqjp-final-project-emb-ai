"""
server.py

Flask web application to detect emotions from text input using the
emotion_detector function from the EmotionDetection module.

Author: Nemanja
"""

from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

# Create Flask app instance
app = Flask(__name__)


@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotion_detector_route():
    """
    Handle emotion detection requests.

    GET: Reads 'textToAnalyze' from query parameters.
    POST: Reads JSON body with key 'text'.

    Returns:
        tuple: Formatted response string and HTTP status code.
    """
    text_to_analyze = ""

    if request.method == 'GET':
        text_to_analyze = request.args.get("textToAnalyze", "")
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            text_to_analyze = data.get("text", "")

    result = emotion_detector(text_to_analyze)

    if result['dominant_emotion'] is None:
        return "Invalid text! Please try again!", 400

    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return response_text, 200


@app.route('/')
def home():
    """
    Render the home page with input form.

    Returns:
        str: Rendered HTML template for the homepage.
    """
    return render_template('index.html')


if __name__ == "__main__":
    # Run the Flask application
    app.run(host='localhost', port=5000, debug=True)
