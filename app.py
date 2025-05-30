from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "✅ Flask 서버가 정상적으로 동작 중입니다!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

