__author__ = 'Igor Medeiros'

import numpy as np
import math
import random
import os

PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT_PATH)

file_links = "texas.cites"
file_labels = "texas.content"


# Hold the adjacence's lists and the label
data = {}
# Hold the ID of registries. ID is the position in the list
mapping = []


def loadData():
    """
    load the data
    """

    global mapping

    # Load adjacencies
    try:
        liFile = open(file_links, "r")
        for index, line in enumerate(liFile):
            line = line.split()
            target = line[0]
            source = line[1]

            if source not in data:
                data[source] = {"adjacence": [target], "label": ""}
            if target not in data:
                data[target] = {"adjacence": [source], "label": ""}
            else:
                data[source]["adjacence"].append(target)
                data[target]["adjacence"].append(source)

    finally:
        liFile.close()

    # Load labels
    try:
        laFile = open(file_labels, "r")
        for line in laFile:
            line = line.split()
            site = line[0]

            # Vetor de features de cada site
            features = line[1:-1]
            label = line[-1]
            mapping.append(site)

            if site in data:
                # Adding labels to existing sites in data
                data[site]["label"] = label
            else:
                # Adding sites that don't cite anyone. They are only cited
                data[site] = {"adjacence": [], "label": label}
            data[site]["features"] = features

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
            newdata[key] = {"adjacence": newdata[key]["adjacence"], "label": ""}

    return newdata


def buildProbMatrix(newdata):
    """
    Input: Dictionary with info about adjacencies and labels
    Output: Matrix, in the form of a list(columns) of lists(rows).
    """
    matrix = []

    for key in mapping:
        # row with all zeros
        row = [0.0] * (len(mapping))

        label = newdata[key]["label"]
        adjacencies = newdata[key]["adjacence"]

        # Case: Node is not labeled case
        if label is "" and adjacencies != []:
            # same probability among adjacents nodes
            value = 1 / float(len(adjacencies))
            # update value only for adjacents nodes
            for elementIndex in range(len(row)):
                if mapping[elementIndex] in adjacencies:
                    row[elementIndex] = value

        # Case: Node is labeled or don't cite anyone
        else:
            index = mapping.index(key)
            row[index] = 1.0

        matrix.append(row)

    return matrix


def buildLabelMatrix(newdata):
    LABELS = ("course", "faculty", "student", "project", "staff")

    matrix = []

    for key in mapping:
        # row with all zeros
        row = [0.0] * (len(LABELS))
        label = newdata[key]["label"]

        if label is not "":
            row[LABELS.index(label)] = 1.0
        matrix.append(row)

    return matrix


def saveMatrixFile(matrix, filename):
    filename = os.path.join(PROJECT_ROOT_PATH, 'data', filename)
    sFile = open(filename, "wb")
    try:

        for row in matrix:
            string = " ".join(map(str, row))
            print>> sFile, string

    finally:
        sFile.close()


def generateCrossvalidation(split=0.1, max_quantity=3):
    """
    Generates the cross-validation sets
    """
    assert 0.01 < split < 0.99

    mapping_copy = list(mapping)  # leave mapping to be read-only
    # Shuffle the list
    random.shuffle(mapping_copy)

    cut = int(len(mapping_copy) * split)

    sublists = []
    while cut < len(mapping_copy):
        if len(sublists) is max_quantity:
            break
        sublists.append(mapping_copy[0:cut])
        mapping_copy = mapping_copy[cut:]

    # Create crossValidation files
    for index, lista in enumerate(sublists):
        newdata = createSubDict(lista)
        p_matrix = buildProbMatrix(newdata)
        l_matrix = buildLabelMatrix(newdata)
        saveMatrixFile(p_matrix, "crossvalidation" + str(int(split * 100)) + "/cvProbability" + str(index + 1) + ".txt")
        saveMatrixFile(l_matrix, "crossvalidation" + str(int(split * 100)) + "/cvLabel" + str(index + 1) + ".txt")


def removeAllLabels(dic):
    for key in mapping:
        dic[key]["label"] = ""

    return dic


def main():
    global mapping
    loadData()
    generateCrossvalidation(0.1)
    generateCrossvalidation(0.2)
    generateCrossvalidation(0.3)
    generateCrossvalidation(0.4)
    generateCrossvalidation(0.5)

    dic = createSubDict(mapping)
    originalP_matrix = buildProbMatrix(dic)
    originalL_matrix = buildLabelMatrix(dic)
    saveMatrixFile(originalP_matrix, "originalProbability" + ".txt")
    saveMatrixFile(originalL_matrix, "originalLabel" + ".txt")

    dicUnlabelled = removeAllLabels(dic)
    unlabelledP_matrix = buildProbMatrix(dicUnlabelled)
    unlabelledL_matrix = buildLabelMatrix(dicUnlabelled)
    saveMatrixFile(unlabelledP_matrix, "unlabelledProbability" + ".txt")
    saveMatrixFile(unlabelledL_matrix, "unlabelled" + ".txt")


if __name__ == '__main__':
    main()

