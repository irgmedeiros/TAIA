# -*- coding: utf-8 -*-
"""
Created on 04/04/2012

@author: Igor Medeiros

Lista:

0 azul
1 azul
3 azul
1 vermelho
1 azul
0 vermelho


Adjacencia
2 5
1 3 5
2 4
3 5 6
1 2 4
4

"""
__author__ = 'Igor Medeiros'
from xml.etree.ElementTree import Element, SubElement, Comment
import xml.etree.ElementTree as xml
from BeautifulSoup import BeautifulSoup

root = None

# historia da classificacao dos labels
histo = {1: (0, "azul"),
         2: (1, "azul"),
         3: (3, "azul"),
         4: (1, "vermelho"),
         5: (1, "azul"),
         6: (0, "vermelho")}

# Lista de adjacencias
adj = {1: [2, 5],
       2: [1, 3, 5],
       3: [2, 4],
       4: [3, 5, 6],
       5: [1, 2, 4],
       6: [4]}


def init_dynamic_graph():
    global root
    root = xml.Element('gexf')
    root.attrib['xmlns'] = "http://www.gexf.net/1.2draft"
    root.attrib['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
    root.attrib['xmlns:viz'] = "http://www.gexf.net/1.2draft/viz"
    root.attrib['xsi:schemaLocation'] = """http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd"""
    root.attrib['version'] = "1.2"

    #Create a child element
    graph = xml.Element('graph')
    graph.attrib['defaultedgetype'] = "undirected"
    graph.attrib['mode'] = "dynamic"
    graph.attrib['timeformat'] = "numeric"
    root.append(graph)

    #Create a child element
    attr = xml.Element('attributes')
    graph.append(attr)
    attr.attrib['class'] = "node"
    attr.attrib['mode'] = "dynamic"

    # Create a child element
    attribute = xml.Element('attribute')
    attr.append(attribute)
    attribute.attrib['id'] = "0"
    attribute.attrib['title'] = "label"
    attribute.attrib['type'] = "string"

    # #Create a child element
    # attr = xml.Element('attributes')
    # graph.append(attr)
    # attr.attrib['class'] = "edge"
    # attr.attrib['mode'] = "dynamic"

    # Create a child element
    # attribute = xml.Element('attribute')
    # attr.append(attribute)
    # attribute.attrib['id'] = "weight"
    # attribute.attrib['title'] = "weight"
    # attribute.attrib['type'] = "float"

    """
    <attributes class="node" mode="dynamic">
      <attribute id="score" title="score" type="integer"></attribute>
    </attributes>
    <attributes class="edge" mode="dynamic">
      <attribute id="weight" title="Weight" type="float"></attribute>
    </attributes>
    """

    return root


def criar_nodos(gexf, adjacencias, histo):
    graph = gexf.find("graph")

    #Create a child element
    nodes = xml.Element('nodes')
    graph.append(nodes)

    for no in adjacencias:
        id = str(no)
        label = str(histo[no][1])
        start_no = "0"
        end_no = str(max(histo.values())[0])
        start = str(histo[no][0])
        end = end_no

        #Create a child element
        node = xml.Element('node')
        nodes.append(node)

        node.attrib['id'] = id
        # node.attrib['label'] = label
        node.attrib['start'] = start_no
        node.attrib['end'] = end_no

        #Create a child element
        spells = xml.Element("spells")
        node.append(spells)

        #Create a child element
        spell = xml.Element("spell")
        spells.append(spell)
        spell.attrib['start'] = start
        spell.attrib['end'] = end
        spell.attrib['label'] = label

        # #Create a child element
        # viz_size = xml.Element(r"viz:size")
        # node.append(viz_size)
        # viz_size.attrib["value"] = "20.0"

        #Create a child element
        attvalues = xml.Element('attvalues')
        node.append(attvalues)

        # #Create a child element
        # attvalue = xml.Element('attvalue')
        # attvalues.append(attvalue)
        # # attvalue.attrib['for'] = "score"
        # # attvalue.attrib['value'] = "2"
        # attvalue.attrib['start'] = start
        # attvalue.attrib['end'] = end

        #Create a child element
        viz_size = xml.Element(r"viz:size")
        node.append(viz_size)
        viz_size.attrib["value"] = "30.0"

        # #Create a child element
        attvalue = xml.Element('attvalue')
        attvalues.append(attvalue)

        attvalue.attrib['for'] = "0"
        attvalue.attrib['value'] = label
        attvalue.attrib['start'] = start
        attvalue.attrib['end'] = end
        attvalue.attrib['label'] = label


def criar_arestas(gexf, adjacencias):
    graph = gexf.find("graph")

    #Create a child element
    edges = xml.Element('edges')
    graph.append(edges)

    for no in adjacencias:
        for target in adjacencias[no]:
            if no > target:
                source = str(no)
                target = str(target)
                start = str(0)
                end = str(3)

                #Create a child element
                edge = xml.Element('edge')
                edges.append(edge)
                edge.attrib['source'] = source
                edge.attrib['target'] = target

                #Create a child element
                attvalues = xml.Element('attvalues')
                edge.append(attvalues)

                #Create a child element
                attvalue = xml.Element('attvalue')
                attvalues.append(attvalue)
                # attvalues.attrib['for'] = "weight"
                # attvalues.attrib['value'] = "1.0"
                attvalues.attrib['start'] = start
                attvalues.attrib['end'] = end


def saveToFile(gexf):
    root = gexf
    #Now lets write it to an .xml file on the hard drive

    #Open a file
    gexf_ = r"D:\Usuarios\Igor Medeiros\Faculdade\2012.2\TAIA\Projeto\test.gexf"
    file = open(gexf_, 'w')

    #xml header
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')

    #Create an ElementTree object from the root element
    xml.ElementTree(root).write(file)
    file.close()

    # Prettify the xml from file
    fi = open(gexf_, "r")
    soup = BeautifulSoup(fi.read())
    fi.close()

    fo = open(gexf_, "w")
    fo.write(soup.prettify())
    fo.close()


def main():
    gexf = init_dynamic_graph()
    criar_nodos(gexf, adj, histo)
    criar_arestas(gexf, adj)
    saveToFile(gexf)


if __name__ == '__main__':
    main()