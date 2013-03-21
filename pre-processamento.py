import math

__author__ = 'Igor Medeiros'

import random
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

    # Load adjacences
    try:
        liFile = open(file_links, "r")
        for index, line in enumerate(liFile):
            line = line.split()
            target = line[0]
            source = line[1]

            if source not in data:
                data[source] = {"adjacence": [target], "label": ""}
                mapping.append(source)
            else:
                data[source]["adjacence"].append(target)
    finally:
        liFile.close()

    # Load labels
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
    """
    Chunck a list of elements (seq) into a number (num) of sublists
    """
    assert num > 0
    avg = math.ceil(len(seq) / float(num))
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def createSubDict(set):
    """
    Input: subset (set) of item from original set that will still labeled
    Output: New dictionary with empty labels in positions that are not in the subset
    """

    newdata = data.copy()
    all_keys = newdata.keys()

    # remove the labels of every key that is not in set
    for key in all_keys:
        if key not in set:
            newdata[key] = {"adjacence" : newdata[key]["adjacence"], "label": ""}

    return newdata

def buildMatrix(newdata):
    """
    Input: Dictionary with info about adjacences and labels
    Output: Matrix, in the form of a list(columns) of lists(rows).
    """
    matrix = []

    for key in mapping:
        # row with all zeros
        row = [0.0]*(len(mapping))

        label = newdata[key]["label"]
        adjacences = newdata[key]["adjacence"]

        # Node is not labeled case
        if label is "":
            # same probability among adjancents nodes
            value = 1/float(len(adjacences))
            # update value only for adjacents nodes
            for elementIndex in range(len(row)):
                if mapping[elementIndex] in adjacences:
                    row[elementIndex] = value

        # Node is labeled case
        else:
            index = mapping.index(key)
            row[index] = 1.0

        matrix.append(row)

    return matrix


def saveFile(matrix, filename):

    try:
        sFile = open(filename, "wb")

        for line in matrix:
            print>>sFile, line

    finally:
        sFile.close()


def generateCrossvalidation():
    mapping_copy = list(mapping) # leave mapping to be read-only

    # Shuffle the list
    random.shuffle(mapping_copy)
    # Generate indepents subsets
    subsets = chunkIt(mapping_copy, 10)

    # Create crossValidation files
    for index, set in enumerate(subsets):
        newdata = createSubDict(set)
        matrix = buildMatrix(newdata)
        saveFile(matrix, "validationSet" + str(index) + ".txt")


def main():
    loadData()
    generateCrossvalidation()


if __name__ == '__main__':
    main()

