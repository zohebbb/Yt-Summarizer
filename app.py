from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from flask_cors import CORS
import language_tool_python
from requests.exceptions import ConnectionError

app = Flask(__name__, static_url_path='/static')
CORS(app, resources={r"/summary": {"origins": "http://127.0.0.1:3000"}})

tool = language_tool_python.LanguageTool('en-US')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['GET'])
def summary_api():
    try:
        # Get YouTube video URL from request parameters
        url = request.args.get('url', '')
        
        # Check if the URL is valid
        if not is_valid_youtube_url(url):
            return jsonify({"error": "Invalid YouTube video URL"}), 400

        # Extract video ID from the URL
        video_id = url.split('=')[1]

        # Get transcript
        transcript = get_transcript(video_id)

        # Check if transcript is available
        if not transcript:
            return jsonify({"error": "No transcript available for the video"}), 400

        # Generate summary
        summary = get_summary(transcript)

        corrected_summary = correct_text(summary)

        return corrected_summary, 200

    except ConnectionError:
        return jsonify({"error": "No internet connection"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def is_valid_youtube_url(url):
    # Check if the URL is a valid YouTube video URL
    return 'youtube.com' in url

def get_transcript(video_id):
    # Get video transcript using YouTubeTranscriptApi
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        return transcript
    except Exception as e:
        # Handle any exception that might occur when fetching the transcript
        return None

def correct_text(text):
    # Correct punctuation and capitalization
    return tool.correct(text)

def get_summary(transcript):
    # Generate summary using transformers pipeline
    summariser = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

if __name__ == '__main__':
    app.run(debug=True)
