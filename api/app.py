from flask import Flask, request, jsonify, send_from_directory
import logging
import subprocess
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Path for the stop signal file
STOP_SIGNAL_FILE = "stop_signal.txt"

@app.route('/')
def index():
    return send_from_directory('.', 'frontend.html')  # Ensure it serves from the current directory

@app.route('/paste', methods=['POST'])
def paste_text():
    logging.debug("Received request at /paste")

    if 'file' not in request.files:
        logging.debug("No file uploaded!")
        return jsonify({"message": "No file uploaded!"}), 400

    file = request.files['file']
    logging.debug(f"File received: {file.filename}")

    try:
        text = file.read().decode('utf-8')
        logging.debug(f"Text received: {text[:50]}...")  # Log first 50 characters

        # Clear stop signal file before starting
        with open(STOP_SIGNAL_FILE, 'w') as f:
            f.write("")

        # Call the typing script with the text as an argument
        subprocess.Popen(['python', os.path.join('.', 'type_script.py'), text])  # Ensure the correct path
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return jsonify({"message": f"Error processing file: {str(e)}"}), 500

    return jsonify({"message": "Typing started! You have 5 seconds to click where you want to paste."})

# New route to stop typing
@app.route('/stop', methods=['POST'])
def stop_typing():
    logging.debug("Stop request received. Writing to stop signal file.")
    with open(STOP_SIGNAL_FILE, 'w') as f:
        f.write("stop")  # Write "stop" to signal the typing script to stop
    return jsonify({"message": "Typing process stopped."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

