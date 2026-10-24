from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Python Multi-Stage Docker Build!",
        "status": "success"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "message": "Application is healthy"
    })

@app.route("/about")
def about():
    return jsonify({
        "app": "Python Flask Application",
        "version": "1.0",
        "docker": "Multi-Stage Build"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
