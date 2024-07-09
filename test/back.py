from flask import Flask, jsonify, request, send_file, render_template
from tone_generator import generate_tone_file

app = Flask(__name__)

@app.route("/")
def home():
    ear= 'both'
    return render_template('front.html', ear=ear)

@app.route('/generate_tone', methods=['POST'])
def generate_tone():
    data = request.json
    byte_io = generate_tone_file(data)
    return send_file(byte_io, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True)