__author__ = 'Igor Medeiros'

from random import random
import os

PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT_PATH)

file_links = "texas.cites"
file_labels = "texas.content"


# Guarda a lista de adjacencia e o label
data = {}
# Guarda o id dos registros. Id e a posicao na listaw
mapping = []

def loadData():
    """
    load the data
    """

    try:
        liFile = open(file_links, "r")
        for index, line in enumerate(liFile):
            line = line.split()
            target = line[1]
            source = line[0]

            if source not in data:
                data[source] = {"adjacence": [target], "label": ""}
                mapping.append(source)
            else:
                data[source]["adjacence"].append(target)
    finally:
        liFile.close()

    try:
        laFile = open(file_labels, "r")
        for line in laFile:
            line = line.split()
            target = line[0]
            label = line[-1]

            if target in data:
                data[target]["label"] = label
    finally:
        laFile.close()


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def createSubDict(set):
    """Deixa a estrutura pronta para salvar em arquivo"""
    newdata = {}


    # TODO code

    return newdata


def saveFile(newdata, filename):

    try:
        sFile = open(filename, "ab")
        for line in newdata:
            sFile.write(line)

    finally:
        sFile.close()


def generateCrossvalidation():
    mapping_copy = mapping[:] # leave mapping to be read-only

    # Shuffle the list
    random.shuffle(mapping_copy)
    # Generate indepents subsets
    subsets = chunkIt(mapping_copy, 10)

    #
    for index, set in enumerate(subsets):
        newdata = createSubDict(set)
        saveFile(newdata, "validationSet" + str(index))


def main():
    loadData()
    generateCrossvalidation()


if __name__ == '__main__':
    main()

