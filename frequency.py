# assign-01

import os
import operator
import collections

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(THIS_FOLDER, 'file.txt')


def file_to_string():
    f = open(file, "r")
    if f.mode == "r":
        return f.read()


def generateMap(text, step):
    count_map = {}
    total = 0
    length = len(text)
    for i in range(length):
        letters = text[i:i+step]
        if (len(letters) == step and checkLetter(letters)):
            total += 1
            if letters in count_map:
                count = count_map[letters] + 1
                count_map[letters] = count
            else:
                count_map[letters] = 1
    printMap(sortMap(count_map), total)


def checkLetter(string):
    for ch in string:
        if (ch < "A" or ch > 'Z'):
            return False
    return True


def printMap(count_map, total):
    for key, value in count_map.items():
        percent = str(format((value / total) * 100, '0.2f'))
        print(key + ":\t" + str(value) + "\t" + percent)


def sortMap(count_map):
    sort_list = sorted(count_map.items(),
                       key=operator.itemgetter(1), reverse=True)
    return collections.OrderedDict(sort_list)


def countSingleLetter(text):
    generateMap(text, 1)


def countDigraphs(text):
    generateMap(text, 2)


def countTrigraphs(text):
    generateMap(text, 3)


if __name__ == "__main__":
    TEXT = file_to_string()
    countSingleLetter(TEXT)
    print('--------------------------')
    print('--------------------------')
    countDigraphs(TEXT)
    print('--------------------------')
    print('--------------------------')
    countTrigraphs(TEXT)
