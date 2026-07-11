from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message" : "the server is on"})

@app.route("/greeting")
def greeting():
    return jsonify({"message" : "hello from Indonesia !!!"})


if __name__ == "__main__":
    app.run()

    # to execute : python ./"Backend AI Track"/"Week 1"/"Build your first API endpoint"/server.py
    # to see with curl : curl http://127.0.0.1:5000 (for {"message" : "the server is on"}) 
    #                    curl http://127.0.0.1:5000/greeting (for {"message" : "hello from Indonesia !!!"})

