from PyQt4.QtGui import QMainWindow, QFileDialog, QDialog, QMessageBox, qApp, QGraphicsScene, QColor, QBrush, QPen, QPixmap
from PyQt4.QtCore import Qt, QRectF
from GUI.Windows.ui_ShowLinks import Ui_ShowLinks
from Common.SysConfig import SysConfig
from Common.System import System
from Common.Module import Module
from Common.Algorithm import Algorithm
from Common.StopCondition import StopCondition 
from copy import deepcopy

import time, os, math, sys
    
def addParam(object, name, value):
    object[name] = value
    
class Node():
    
    def __init__(self, label):
        self.label = label
        self.parameters = {}
    
class Edge():
    
    def __init__(self, label, headNode, tailNode):
        self.headNode = headNode
        self.tailNode = tailNode
        self.parameters = {}
        addParam(self.parameters, "label", label)
    
class Field():
    
    def __init__(self, filename, graphName = "G", rankDir = "LR"):
        self.filename = filename
        self.graphName = graphName
        self.rankDir = rankDir
        self.nodes = {}
        self.edges = []
        self.generalNodeParams = {}
        self.generalEdgeParams = {}
        self.config = None
    
    def setGeneralNodeParams(self):
        addParam(self.generalNodeParams,"fontsize","12")
        addParam(self.generalNodeParams,"shape","component")
        addParam(self.generalNodeParams,"style","filled, bold")
        addParam(self.generalNodeParams,"fillcolor","lightgrey")
        addParam(self.generalNodeParams,"color","black")
        addParam(self.generalNodeParams,"fontcolor","black")
    
    def setGeneralEdgeParams(self):
        addParam(self.generalEdgeParams,"fontsize","9")
        addParam(self.generalEdgeParams,"color","red")
        addParam(self.generalEdgeParams,"fontcolor","blue")
    
    def addNode(self, nodeName):
        if nodeName not in list(self.nodes.keys()):
            self.nodes[nodeName.num] = Node("Module %d" % (nodeName.num + 1))
    
    def addInvisibleNodes(self, modnum):
        self.nodes[-1] = Node("Module 0")
        addParam(self.nodes[-1].parameters,"style","invisible")
        self.nodes[modnum] = Node("Module %d" % (modnum + 1))
        addParam(self.nodes[modnum].parameters,"style","invisible")
    
    def addDashedEdges(self, modnum):
        #print len(self.nodes)
        temp = Edge("", self.nodes[modnum - 1], self.nodes[modnum])
        addParam(temp.parameters,"style","dashed")
        self.edges.append(temp)
        
        temp = Edge("", self.nodes[-1], self.nodes[0])
        addParam(temp.parameters,"style","dashed")
        self.edges.append(temp)
    
    def addEdge(self, link):
        temp = Edge(str(link.vol), self.nodes[link.src.num], self.nodes[link.dst.num])
        self.edges.append(temp)
    
    def makeFieldFromConfig(self, config):
        self.setGeneralNodeParams()
        self.setGeneralEdgeParams()
        for l in config.links:
            self.addNode(l.src)
            self.addNode(l.dst)
            self.addEdge(l)
        self.addInvisibleNodes(config.modNum)
        self.addDashedEdges(config.modNum)
    
    def printHead(self):
        self.filename.write("digraph %s\n" % (self.graphName))
        self.filename.write("{\n")
        self.filename.write('\t rankdir = "%s"\n' % (self.rankDir))
    
    def printParams(self, Params):
        num = 0
        for key in list(Params.keys()):
            self.filename.write(' %s = "%s"' % (key, Params[key]))
            num += 1
            if num != len(list(Params.keys())):
                self.filename.write(" ,")
    
    def printGeneralNodeParams(self):
        self.filename.write("\t node ")
        if len(self.generalNodeParams) != 0:
            self.filename.write("[")
            self.printParams(self.generalNodeParams)
            self.filename.write(" ];\n")
    
    def printGeneralEdgeParams(self):
        self.filename.write("\t edge ")
        if len(self.generalEdgeParams) != 0:
            self.filename.write("[")
            self.printParams(self.generalEdgeParams)
            self.filename.write(" ];\n")
    
    def printNode(self, node):
        self.filename.write('\t "%s" ' % (node.label))
        if len(node.parameters) != 0:
            self.filename.write('[')
            self.printParams(node.parameters)
            self.filename.write(' ]')
        self.filename.write(';\n')
    
    def printEdge(self, edge):
        self.filename.write('\t "%s"  ->  "%s" ' % (edge.headNode.label, edge.tailNode.label))
        if len(edge.parameters) != 0:
            self.filename.write('[')
            self.printParams(edge.parameters)
            self.filename.write(' ]')
        self.filename.write(';\n')
    
    def printTail(self):
        self.filename.write("}\n")
    
    def printField(self, file):
        self.printHead()
        self.printGeneralNodeParams()
        self.printGeneralEdgeParams()
        for key in list(self.nodes.keys()):
            self.printNode(self.nodes[key])
        for e in self.edges:
            self.printEdge(e)
        self.printTail()
    
class ShowLinks(QDialog):
    
    def __init__(self, config, filename):
        self.pix = None
        self.filename = (((filename.split('/'))[-1]).split('.'))[0]
        self.makeLinksField(config)
        self.FieldToPNG()
        QDialog.__init__(self)
        self.ui = Ui_ShowLinks()
        self.ui.setupUi(self) 
        self.Paint()   
    
    def __del__(self):
        try:
            os.remove(self.filename + ".gv")
            os.remove(self.filename + ".png")
        except:
            pass      
            
    def makeLinksField(self, config):
        name = self.filename + '.gv'
        f = open(name, "w")
        self.field = Field(f)
        self.field.makeFieldFromConfig(config)
        self.field.printField(f)
        f.close()      
            
    def FieldToPNG(self):
        GVname = self.filename + '.gv'
        PNGname = self.filename + '.png'
        if sys.platform.startswith("win"):
            os.system(u"dot.exe -Tpng -o %s %s" % (unicode(PNGname), unicode(GVname)))
        else:
            os.system("dot -Tpng -o %s %s" % (PNGname, GVname))

    def SaveImageAs(self):
        name = unicode(QFileDialog.getSaveFileName(directory = "SystemGraphs/PNG/%s" % (self.filename),filter=self.tr("Images (*.png)")))
        if name == None or name == '':
            return
        self.pix.save(name)

    def SaveDigraphAs(self):
        name = unicode(QFileDialog.getSaveFileName(directory = "SystemGraphs/GV/%s" % (self.filename),filter=self.tr("Graphviz files (*.gv)")))
        if name == None or name == '':
            return
        f1 = open(name, "w")
        n = self.filename + '.gv'
        f2 = open(n, "r")
        f1.write(f2.read())
        f2.close()      
        f1.close()      
            
    def Paint(self):
        PNGname = self.filename + '.png'
        scene = QGraphicsScene()
        scene.setBackgroundBrush(Qt.transparent)
        self.pix = QPixmap(PNGname)
        scene.addPixmap(self.pix)
        self.ui.graph.setScene(scene)
        self.ui.graph.show()
