from flask import Flask, request, send_file
from rembg import remove
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/remove', methods=['POST'])
def remove_watermark():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    input_image = Image.open(file.stream).convert("RGBA")

    output = remove(input_image)

    output_io = BytesIO()
    output.save(output_io, format='PNG')
    output_io.seek(0)

    return send_file(output_io, mimetype='image/png')

if __name__ == '__main__':
    app.run()
