import pickle


def most_common():
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

    return_dict = {'Colour': result_content[0][0][1], 'Shape': result_content[0][0][0]}
    return return_dict
