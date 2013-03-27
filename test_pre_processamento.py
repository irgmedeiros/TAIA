__author__ = 'Igor Medeiros'

import pre_processamento as p
import unittest

class TestPreProcessamento(unittest.TestCase):

    def setUp(self):
        p.loadData()
        self.sub_lists = p.chunkIt(p.mapping, 10)
        data = p.createSubDict(self.sub_lists[0])
        self.p_matrix1 = p.buildProbMatrix(data)
        self.l_matrix1 = p.buildLabelMatrix(data)

    def test_subsets_are_independents(self):

        subsets = map(set, self.sub_lists)

        intersec = set.intersection(*subsets)
        self.assertFalse(intersec)

    def test_matrix_dimension(self):
        self.assertEquals(len(self.p_matrix1), len(p.mapping))


if __name__ == '__main__':
    unittest.main()

