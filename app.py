from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>Personal Wallet Warning Signal</h2><p>🚀 Flask app deployed successfully!</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
