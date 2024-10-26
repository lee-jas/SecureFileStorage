from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

"""Route that accepts a file upload"""
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": 'No file part'}), 
        
    # Get the file from the request
    file = request.files['file']

    # Check if a file was selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file securely
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Save or process the file
    return jsonify({"message": "File uploaded successfully", "file": filename}), 201


"""Route that downloads a file"""
@app.route('/download', methods=['GET'])
def download_file():
    # Get the filename from the request
    filename = request.args.get('filename')

    if not filename:
        return jsonify({"error": "No filename provided"}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # Serve the file
    return send_file(file_path, as_attachment=True)


"""Check if the API is running"""
@app.route('/', methods=['GET'])
# Define a route that checks if the API is running
def health_check():
    return jsonify({"status": "API is running"}), 200


if __name__ == '__main__':
    app.run(debug=True)