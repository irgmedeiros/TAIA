__author__ = 'Igor Medeiros'

import xml.etree.ElementTree as xml

root = xml.Element('gexf')
root.attrib['xmlns'] = "http://www.gexf.net/1.1draft"
root.attrib['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
root.attrib['xsi:schemaLocation'] = """http://www.gexf.net/1.1draft http://www.gexf.net/1.1draft/gexf.xsd"""
root.attrib['version'] ="1.1"

#Create a child element
graph = xml.Element('graph')
root.append(graph)

graph.attrib['defaultedgetype'] = "directed"
graph.attrib['mode'] = "dynamic"


#Create a child element
attr = xml.Element('attributes')
graph.append(attr)

attr.attrib['class']="node"
attr.attrib['mode']="dynamic"

#Create a child element
nodes = xml.Element('nodes')
graph.append(nodes)

#Create a child element
node = xml.Element('node')
nodes.append(node)

node.attrib['id']="n1"
node.attrib['label']="Node 1"
node.attrib['start']="2007"
node.attrib['end']="2009"

#Create a child element
attvalues = xml.Element('attvalues')
node.append(attvalues)

#Create a child element
attvalue = xml.Element('attvalue')
attvalues.append(attvalue)

#Now lets write it to an .xml file on the hard drive

#Open a file
file = open(r"C:\Users\Igor Medeiros\Desktop\test.gexf", 'w')

#xml header
file.write('<?xml version="1.0" encoding="UTF-8"?>\n')

#Create an ElementTree object from the root element
xml.ElementTree(root).write(file)

#Close the file like a good programmer
file.close()
