import string
import re
import decimal

def similarities(texts, target):
    final_list = []
    for text in texts:
        final_list.append(sim(text, target))
    return sorted(final_list, reverse=True)

def word_length_list(text):
    fp = open(text, 'r', encoding="utf-8")
    dict_collect = {}
    word_length_list = []
    for line in fp.read().splitlines():
        words = re.split('[ \n\t]', line)
        for word in words:
            word = word.strip(string.punctuation)
            if len(word) not in dict_collect.keys():
                dict_collect[len(word)] = 1
            else:
                dict_collect[len(word)] += 1

    # make up with 0 if there is gapped word_length
    for i in range(1, max(dict_collect.keys()) + 1):
        try:
            word_length_list.append(dict_collect[i])
        except KeyError:
            word_length_list.append(0)
    return word_length_list

def sim(text,target):
    listA = word_length_list(text)
    listB = word_length_list(target)

    len_max  = max(len(listA), len(listB))
    len_diff = abs(len(listA) - len(listB))

    # make up with 0 if there is length difference
    if len(listA) > len(listB):
        for i in range(0,len_diff):
            listB.append(0)
    elif len(listA) < len(listB):
        for i in range(0,len_diff):
            listA.append(0)

    denominator = 0
    numerator = 0
    # numerator calculation
    for i in range(0,len_max):
        numerator += (listA[i] * listB[i])

    # denominator calculation
    part1 = 0
    part2 = 0
    for i in range(0,len_max):
        part1 += (listA[i] ** 2)
        part2 += (listB[i] ** 2)
    denominator = (part1 ** 0.5) * (part2 ** 0.5)


    # All numbers should be rounded to three decimal places.
    result = round(numerator / denominator, 3)
    # result = numerator / denominator
    # result = decimal.Decimal(str(result)).quantize(decimal.Decimal("0.000"))

    tup_return = (result, text)
    return tup_return