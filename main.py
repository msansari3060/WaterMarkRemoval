from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Watermark Remover API is Live", 200

@app.route('/remove', methods=['POST'])
def remove_watermark():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    try:
        image = request.files['image']
        input_image = Image.open(image.stream).convert("RGBA")
        output_image = remove(input_image)

        buf = io.BytesIO()
        output_image.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Important: Use port from environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
