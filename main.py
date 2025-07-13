
from flask import Flask, request, send_file
from rembg import remove
from io import BytesIO
from PIL import Image
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route('/')
def home():
    return '✅ Watermark API is live.'

@app.route('/remove', methods=['POST'])
def remove_watermark():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    input_image = Image.open(file.stream).convert("RGBA")

    # Process using rembg
    output_image = remove(input_image)

    # Prepare in-memory response
    output_io = BytesIO()
    output_image.save(output_io, format='PNG')
    output_io.seek(0)

    return send_file(output_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
