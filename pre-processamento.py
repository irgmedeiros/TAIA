__author__ = 'Igor Medeiros'

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

    # Load adjacencies
    try:
        liFile = open(file_links, "r")
        for index, line in enumerate(liFile):
            line = line.split()
            target = line[0]
            source = line[1]

            if source not in data:
                data[source] = {"adjacence": [target], "label": ""}
            else:
                data[source]["adjacence"].append(target)
    finally:
        liFile.close()

    # Load labels
    try:
        laFile = open(file_labels, "r")
        for line in laFile:
            line = line.split()
            site = line[0]
            label = line[-1]
            mapping.append(site)

            if site in data:
                # Adding labels to existing sites in data
                data[site]["label"] = label
            else:
                # Adding sites that don't cite anyone. They are only cited
                data[site] = {"adjacence": [], "label": label}
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

def buildProbMatrix(newdata):
    """
    Input: Dictionary with info about adjacencies and labels
    Output: Matrix, in the form of a list(columns) of lists(rows).
    """
    matrix = []

    for key in mapping:
        # row with all zeros
        row = [0.0]*(len(mapping))

        label = newdata[key]["label"]
        adjacencies = newdata[key]["adjacence"]

        # Case: Node is not labeled case
        if label is "" and adjacencies != []:
            # same probability among adjacents nodes
            value = 1/float(len(adjacencies))
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
        row = [0.0]*(len(LABELS))
        label = newdata[key]["label"]

        if label is not "":
            row[LABELS.index(label)] = 1.0
        matrix.append(row)

    return matrix

def saveMatrixFile(matrix, filename):
    try:
        sFile = open(filename, "wb")
        for row in matrix:
            string = " ".join(map(str, row))
            print>>sFile, string

    finally:
        sFile.close()


def generateCrossvalidation():
    """
    Generates the cross-validation sets
    """
    mapping_copy = list(mapping) # leave mapping to be read-only

    # Shuffle the list
    random.shuffle(mapping_copy)
    # Generate Independents subsets
    subsets = chunkIt(mapping_copy, 10)

    # Create crossValidation files
    for index, set in enumerate(subsets):
        newdata = createSubDict(set)
        p_matrix = buildProbMatrix(newdata)
        l_matrix = buildLabelMatrix(newdata)
        saveMatrixFile(p_matrix, "cvProbability" + str(index+1) + ".txt")
        saveMatrixFile(l_matrix, "cvLabel" + str(index+1) + ".txt")


def main():
    loadData()
    generateCrossvalidation()


if __name__ == '__main__':
    main()

