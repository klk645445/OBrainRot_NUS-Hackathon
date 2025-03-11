from flask import Flask, request, jsonify, render_template, send_from_directory
from main import main
from search import find
import re
import os
app = Flask(__name__)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('web.html')

@app.route('/fetch', methods=['POST'])
def search_keywords():
    print("Received request at /fetch")
    data = request.get_json()
    papers = find(data['keywords'])
    print(f'Found {len(papers)} papers')

    return jsonify({'papers': list(papers)})


@app.route('/generate', methods=['POST'])
def generate():
    print("Received request at /generate")  # Debugging statement
    data = request.get_json()['paper']
    title = data['title']

    print(f"Title: {title}")  # Debugging statement

    main(data)

    # Assuming the video is saved as 'subway.mp4' in the 'assets' directory
    video_filename = 'final.mp4'
    video_path = os.path.join('final', video_filename)
    if os.path.exists(video_path):
        print("Video generation successful")  # Debugging statement

        with open(f'downloads/{title}/related.txt', 'r', encoding='utf-8') as file:
            text = file.read().split('\n')

        return jsonify({'video_url': f'/final/{video_filename}', 'related': text})
    else:
        print("Video generation failed")  # Debugging statement
        return jsonify({'error': 'Video generation failed'}), 500

@app.route('/final/<path:filename>')
def serve_video(filename):
    return send_from_directory('final', filename)

if __name__ == "__main__":
    app.run(debug=True)