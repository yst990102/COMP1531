from flask import Flask, app, request
from number_fun import multiply_by_two, print_message, sum_list_of_numbers, sum_iterable_of_numbers, is_in, index_of_number

APP = Flask(__name__)

port = 12345


@APP.route("/multiply_by_two", methods=['GET'])
def http_multiply_by_two():
    number = request.args.get('number')
    result = multiply_by_two(int(number))
    return str(result)


@APP.route("/print_message", methods=['GET'])
def http_print_message():
    message = request.args.get('message')
    return message


@APP.route("/sum_list_of_numbers", methods=['GET'])
def http_sum_list_of_numbers():
    numbers = request.args.get('numbers')
    result = sum_list_of_numbers(eval(numbers))
    return str(result)


@APP.route("/sum_iterable_of_numbers", methods=['GET'])
def http_sum_iterable_of_numbers():
    numbers = request.args.get('numbers')
    result = sum_iterable_of_numbers(eval(numbers))
    return str(result)


@ APP.route("/is_in", methods=['GET'])
def http_is_in():
    needle = request.args.get('needle')
    haystack = request.args.get('haystack')
    result = is_in(needle, haystack)
    return str(result)


@ APP.route("/index_of_number", methods=['GET'])
def http_index_of_number():
    item = request.args.get('item')
    numbers = request.args.get('numbers')
    result = index_of_number(int(item), eval(numbers))
    return str(result)


if __name__ == "__main__":
    APP.run(port=port)
