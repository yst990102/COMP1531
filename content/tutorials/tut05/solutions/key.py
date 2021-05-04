import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/getcount', methods=['GET'])
def addname():
    tag = request.args.get('tag')
    
    c = requests.get(f"https://www.unsw.edu.au/").text
    allcontent = c.split('<')
    count = 0
    for f in allcontent:
        if f[0] != '/':
            condensed = f.split(' ')[0].split('>')[0]
            if condensed == tag:
                count += 1

    return jsonify({
        'tag_count': count,
    })

if __name__ == '__main__':
    app.run()

