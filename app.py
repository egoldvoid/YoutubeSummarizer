from flask import Flask, request, jsonify
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import os
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/summarize', methods=['POST'])
def summarize_video():
    try:
        # Get the video URL from the request body
        data = request.json
        video_url = data.get('url')

        # Ensure a URL was provided
        if not video_url:
            return jsonify({'error': 'No video URL provided'}), 400

        # Extract the video ID from the URL
        video_id = video_url.split('v=')[-1]
        
        # Get the transcript using YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([entry['text'] for entry in transcript])

        # Summon GPT to summarize the transcript
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize this text: {full_text}",
            max_tokens=250,
            temperature=0.7
        )

        # Get the summary from the response
        summary = response.choices[0].text.strip()
        return jsonify({'summary': summary})

    except YouTubeTranscriptApi.CouldNotRetrieveTranscript as yt_error:
        return jsonify({'error': f"Could not retrieve transcript: {str(yt_error)}"}), 404
    except openai.error.OpenAIError as openai_error:
        return jsonify({'error': f"OpenAI API error: {str(openai_error)}"}), 500
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999, debug=True)
