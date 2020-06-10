#!usr/bin/env python
#coding:utf-8

from tenk.overseaTest.XmlDao import xmlProvider


class flagProvider():
    def __init__(self,filename=None):
        self.__filename = filename
        print('filename', self.__filename)

    #获取节点属性
    def getValueByName(self,node,name):
        tree = xmlProvider.openXml(self.__filename)
        if tree is None:
            return None
        nodes = xmlProvider.find_nodes(tree, node)
        nodes = xmlProvider.get_node_by_keyvalue(nodes, {'name':name})
        if len(nodes) > 0:
            return nodes[0].text
            # return nodes[0].attrib["name"]
        return None

    #设置节点
    def setValueByName(self,node,name,value):
        tree = xmlProvider.openXml(self.__filename)
        if tree is None:
            return None
        nodes = xmlProvider.find_nodes(tree, node)
        nodes = xmlProvider.get_node_by_keyvalue(nodes, {'name':name})
        if len(nodes) > 0:
            nodes[0].text = value
            # nodes[0].attrib['value'] = value
            xmlProvider.saveAs(tree, self.__filename)

    #添加节点
    def addTag(self,node,name,content):
        tree = xmlProvider.openXml(self.__filename)
        xmlProvider.add_child_node([tree.getroot()],xmlProvider.create_node(node, {'name':name}, content))
        xmlProvider.saveAs(tree, self.__filename)

    #删除节点
    def deleteTagByName(self,name):
        tree = xmlProvider.openXml(self.__filename)
        xmlProvider.del_node_by_tagkeyvalue([tree.getroot()], 'flag', {'name':name})
        xmlProvider.saveAs(tree, self.__filename)
