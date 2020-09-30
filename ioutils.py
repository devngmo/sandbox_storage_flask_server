import os, sys, json, yaml
import codecs

def saveText(filePath,text):
    f = codecs.open(filePath, 'w', encoding='utf-8')
    f.write(text)
    f.close()

def saveBytes(filePath, data):
    f = open(filePath, 'wb')
    f.write(data)
    f.close()

def loadText(filePath):    
    f = codecs.open(filePath, encoding='utf-8')
    #for line in f:
    #    print repr(line)
    text = f.read()
    f.close()
    return text

def writeFile(filePath, content):
    f = codecs.open(filePath, 'w', encoding='utf-8')
    f.write(content)
    f.close()
    
def loadJson(filePath):
    f = codecs.open(filePath, 'r', encoding='utf-8')
    jsonstr = f.read()
    f.close()
    return json.loads( jsonstr )

def loadYaml(filePath):
    return yaml.load( loadText(filePath) )

def saveYaml(filePath, data):
    saveText(filePath, yaml.dump(data))
        
def listDirs(src):
    ls = []
    srcDeep = src.count(os.path.sep)
    for root, dirs, files in os.walk(src):
        rootDeep = root.count(os.path.sep)
        if rootDeep == srcDeep + 1:
            ls = ls + [os.path.basename(root)]
    return ls
    
def listDirsFiles(src):
    lsDirs = []
    lsFiles = []
    srcDeep = src.count(os.path.sep)
    for root, dirs, files in os.walk(src):
        rootDeep = root.count(os.path.sep)
        if rootDeep == srcDeep + 1:
            lsDirs = lsDirs + [os.path.basename(root)]
        
        elif rootDeep == srcDeep:
            for f in files:
                lsFiles = lsFiles + [f]
    return lsDirs, lsFiles
