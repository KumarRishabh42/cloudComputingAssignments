import os
import hashlib
import math
import copy
class leaveNode:
    def __init__(self,data):
        self.info = data
        self.value = self.hashFunc(data)
        self.left = None
        self.right = None
        self.type = "leaf"
    def hashFunc(self,data):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

class internalNode:
    def __init__(self,leftEle,rightEle):
        self.left = leftEle
        self.right = rightEle
        self.value = self.mergeHash(leftEle.value,rightEle.value)
        self.info = self.value
        self.type = "internalNode"
    def mergeHash(self,leftEleVal,rightEleVal):
        m = hashlib.md5()
        m.update(leftEleVal+"+"+rightEleVal)
        return m.hexdigest()

class merkleTree:
    def __init__(self,fileList,rawData):
        self.leaves = []
        self.chunks = len(rawData)
        #print len(rawData)
        self.height = self.findHeight(len(rawData))
        self.tree = [None for i in xrange(0,(2**(self.height+1)))]
        self.fileList = fileList
        self.__MT__(rawData)
        pass
    def create(self,dataBlocks):
        for data in dataBlocks:
            self.leaves.append(leaveNode(data))
        height = self.findHeight(len(self.leaves))
    def findHeight(self,noOfBlocks):
        return int(math.ceil(math.log(noOfBlocks,2)))
    def makeTree(self):
        #print self.leaves
        nodeNorm = 2**self.height 
        for i in xrange(nodeNorm,nodeNorm*2):
            self.tree[i] = self.leaves[i-nodeNorm]
        for i in reversed(xrange(self.height)):
            nodeNorm = 2**i
            for i in xrange(nodeNorm,nodeNorm*2):
                newInternalNode = internalNode(self.tree[i*2],self.tree[i*2+1])
                self.tree[i] = newInternalNode

        #print self.tree
    def update(self,data,index):
        treeIndex = index-1 + 2**self.height
        self.tree[treeIndex] = leaveNode(data)
        #print self.tree
        #print treeIndex
        while(treeIndex>1):
            treeIndex = treeIndex/2
            print treeIndex
            print "using",treeIndex*2,treeIndex*2+1
            newInternalNode = internalNode(self.tree[treeIndex*2],self.tree[treeIndex*2+1])
            self.tree[treeIndex] = newInternalNode
        pass
        #print self.tree

        
        

    def __MT__(self,rawData):
        self.create(rawData)
        self.makeTree()
        



wrongChunkList = []

def compareMerkelTrees(merkelTree,merkelTree2,index,numBlocks):
    if merkelTree.tree[index].value==merkelTree2.tree[index].value:
        return
    elif index>=numBlocks and merkelTree.tree[index].value!=merkelTree2.tree[index].value:
        wrongChunkList.append([merkelTree.fileList[index-numBlocks],index])
        return
    else:
        result1=compareMerkelTrees(merkelTree,merkelTree2,2*index,numBlocks)
        result2=compareMerkelTrees(merkelTree,merkelTree2,2*index+1,numBlocks)
        return 

fileMain = "default"


if __name__=="__main__":
    merkleTreeList = {}
    print "Enter number of client nodes : ",
    noOfIPs = input()
    listOfIPs = []
    for i in xrange(noOfIPs):
        print "Enter IP details : ",
        listOfIPs.append(raw_input())
    print "to upload a new file put the file to uploads folder and press n"
    print "If a file is updated press u"
    ipList = []
    while(1):
        response = raw_input()
        
        if(response == "n"):
            print "Enter the name of the file",
            fileMain = raw_input()
            main = filter(None,open(fileMain,"r").read().split('\n'))
            for idx,i in enumerate(main):
                print idx
                pathRelative = os.path.join("uploads",str(idx))
                open(pathRelative,"w").write(i) 
            print os.listdir("uploads")
            listOfChunks = []
            listOfFiles = [str(i) for i in sorted([int(i) for i in os.listdir("uploads")])]
            print listOfFiles
            for i in listOfFiles:
                path = os.path.join("uploads",i)
                name = i
                print "New File "+name+" has been found" 
                print "press any key to start hashing"
                x = raw_input()
                listOfChunks.append(open(path,"r").read())

            size = int(2**math.ceil(math.log(len(listOfChunks),2)))
            sizeCurrent = len(listOfChunks)
            for i in xrange(size-sizeCurrent):
                listOfChunks.append("")

            for i in listOfIPs:
                scpString = "scp -rp uploads " + i
                scpFile ="scp "+fileMain +" "+i
                scpPython = "scp join.py "+i
                os.system(scpString) #TODO
                os.system(scpFile) #TODO
                os.system(scpPython) #TODO



            merkleTreeList["complete"] = merkleTree(listOfFiles,listOfChunks)

        if(response == 'u'):
            main = filter(None,open(fileMain,"r").read().split('\n'))
            for idx,i in enumerate(main):
                pathRelative = os.path.join("uploads",str(idx))
                open(pathRelative,"w").write(i) 
            wrongChunkList = []


            print os.listdir("uploads")
            listOfChunks = []
            listOfFiles = [str(i) for i in sorted([int(i) for i in os.listdir("uploads")])]
            print listOfFiles 
            for i in listOfFiles:
                path = os.path.join("uploads",i)
                name = i
                listOfChunks.append(open(path,"r").read())
            size = int(2**math.ceil(math.log(len(listOfChunks),2)))
            sizeCurrent = len(listOfChunks)
            for i in xrange(size-sizeCurrent):
                listOfChunks.append("")
            merkleTreeList["new"] = merkleTree(listOfFiles,listOfChunks)
            print "new merkle tree"
            for i in merkleTreeList["new"].tree:
                if i is not None:
                    print i.value

            print "old merkle tree"
            for i in merkleTreeList["complete"].tree:
                if i is not None:
                    print i.value


            print "reaching the comparision phase"
            changedEleList = []
            for i in xrange(size,2*size):
                if(merkleTreeList["new"].tree[i].value!=merkleTreeList["complete"].tree[i].value):
                    changedEleList.append([merkleTreeList["new"].fileList[i-size],i])

            compareMerkelTrees(merkleTreeList["complete"],merkleTreeList["new"],1,len(listOfFiles))
          
            merkleTreeList["complete"] = copy.deepcopy(merkleTreeList["new"])
            print len(listOfFiles)
            print wrongChunkList
            
            
            
            for i in changedEleList:
                for j in listOfIPs:
                    scpCommand = "scp uploads/"+i[0]+" "+j+"uploads/"
                    print scpCommand
                    os.system(scpCommand)

                    sshCommand = "ssh  "+ j.split(":")[0]+" "+' "python join.py '+fileMain+'"'
                    print sshCommand
                    os.system(sshCommand)
            print changedEleList 



