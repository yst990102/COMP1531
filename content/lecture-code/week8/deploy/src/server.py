from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/test')
def test():
    return "Testing World!"

if __name__ == '__main__':
    app.run(port=8080)

