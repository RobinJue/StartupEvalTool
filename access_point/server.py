from flask import Flask, request, jsonify, send_from_directory, Response
from api import process_startup
from pathlib import Path
import subprocess
import sys

app = Flask(__name__)

# Define the path to the directory containing gui.html
html_dir = Path(__file__).parent

@app.route('/')
def serve_gui():
    """
    Serve the gui.html file when accessing the root URL.
    """
    return send_from_directory(html_dir, 'gui.html')

@app.route('/process', methods=['GET'])
def process():
    """
    Streams logs live back to the client using Server-Sent Events (SSE).
    """
    startup_name = request.args.get('startup_name')
    if not startup_name:
        return Response("Startup name is required.", status=400)

    def generate_logs():
        """
        Generator function to stream logs from main.py.
        """
        try:
            process = subprocess.Popen(
                [sys.executable, str(Path(__file__).parent.parent / "main.py"), startup_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            for line in process.stdout:
                yield f"data: {line.strip()}\n\n"
            for line in process.stderr:
                yield f"data: {line.strip()}\n\n"

            process.wait()

            if process.returncode == 0:
                yield "data: Main script completed successfully.\n\n"
            else:
                yield f"data: Main script failed with return code {process.returncode}.\n\n"

        except Exception as e:
            yield f"data: An error occurred: {e}\n\n"

    return Response(generate_logs(), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(port=5000)