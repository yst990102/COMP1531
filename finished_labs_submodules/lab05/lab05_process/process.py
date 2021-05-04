import json
import operator
import pickle


def process():
    pickle_file = open("shapecolour.p", "rb")
    contents = pickle.load(pickle_file)

    content = []
    for i in contents:
        content.append(tuple(i.values()))

    content_count = {}
    for i in content:
        if content.count(i) >= 1:
            content_count[i] = content.count(i)

    result_content = sorted(content_count.items(), key=lambda x: x[1], reverse=True)

    return_dict = {
        "mostCommon": {
            "colour": result_content[0][0][1],
            "shape": result_content[0][0][0]
        },
        "rawData": contents
    }

    with open('processed.json', 'w') as f:
        f.write(json.dumps(return_dict))

    return return_dict
