from flask import Flask, request, jsonify
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/summarize', methods=['POST'])
def summarize_video():
    try:
        data = request.json
        video_url = data.get('url')

        if not video_url:
            return jsonify({'error': 'No video URL provided'}), 400

        # Debug: Print video URL
        print(f"Video URL: {video_url}")

        video_id = video_url.split('v=')[-1]

        # Debug: Print video ID
        print(f"Video ID: {video_id}")
        
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([entry['text'] for entry in transcript])

        # Debug: Print fetched transcript
        print(f"Transcript: {full_text[:100]}...")  # Print only first 100 characters to avoid overflow

        # Use ChatCompletion for gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize this text: {full_text}"}
            ],
            max_tokens=250,
            temperature=0.7
        )

        summary = response.choices[0].message['content'].strip()

        # Debug: Print summary result
        print(f"Summary: {summary}")

        return jsonify({'summary': summary})

    except Exception as yt_error:
        print(f"Error fetching transcript or processing: {yt_error}")
        return jsonify({'error': f"Could not retrieve transcript: {str(yt_error)}"}), 500

    except openai.error.OpenAIError as openai_error:
        print(f"OpenAI API error: {openai_error}")
        return jsonify({'error': f"OpenAI API error: {str(openai_error)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999, debug=True)
