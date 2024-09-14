from flask import Flask, request, jsonify
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/summarize', methods=['POST'])
def summarize_video():
    data = request.json
    video_url = data.get('url')

    # Extract the video ID from the URL
    video_id = video_url.split('v=')[-1]
    
    # Gets the transcript using yt transcript api
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([entry['text'] for entry in transcript])

        # Summon GPT to summarize
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize this text: {full_text}",
            max_tokens=250,
            temperature = 0.7
            
        )

        summary = response.choices[0].text.strip()
        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999, debug="True")
