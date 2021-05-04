from flask import Flask, send_file
app = Flask(__name__)

@app.route("/img")
def img():
    return send_file('./cat.jpg', mimetype='image/jpg')

if __name__ == "__main__":
    app.run()
