import os, sys, codecs, yaml, ioutils, yaml
from flask import Flask, flash, request, redirect, url_for, send_from_directory, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from flask import json
import uuid

app = Flask(__name__)
CORS(app)
app.config['APP_REFS'] = {}
refFilePath = os.path.join(os.getcwd(), 'appref.yaml')

if os.path.exists(refFilePath):
    app.config['APP_REFS'] = ioutils.loadYaml(refFilePath)


DIR_COLLECTIONS = os.path.join(os.getcwd(), 'collections')
### init
if not os.path.exists(DIR_COLLECTIONS):
    os.makedirs(DIR_COLLECTIONS)


@app.route('/', methods=['GET'])
@cross_origin(origin='localhost')
def index():
    appFolder = os.getcwd()
    return 'Welcome to Sandbox Storage! Support: Collection'
#############################################
##### GET ALL DOCUMENTS
@app.route('/collection/<name>', methods=['GET'])
@cross_origin(origin='localhost')
def collection_get(name):
    print('\n collection [%s] get all\n' % name)
    fp = os.path.join(DIR_COLLECTIONS, '%s.json' % name)
    if os.path.exists(fp):
        return json.dumps(ioutils.loadJson(fp))
    return '[]'
#############################################
##### DELETE ALL DOCUMENTS
@app.route('/collection/<name>', methods=['DELETE'])
@cross_origin(origin='localhost')
def collection_delete(name):
    print('\n collection [%s] get all\n' % name)
    fp = os.path.join(DIR_COLLECTIONS, '%s.json' % name)
    ioutils.writeFile(fp, '[]')
    return 'ok'
#############################################
##### ADD A NEW DOCUMENT
@app.route('/collection/<name>', methods=['PUT'])
@cross_origin(origin='localhost')
def collection_add_document(name):
    doc = request.get_json()
    print('\ncollection [%s] add %s\n'% (name, json.dumps(doc)))
    
    fp = os.path.join(DIR_COLLECTIONS, '%s.json' % name)
    ls = []
    if os.path.exists(fp):
        ls = ioutils.loadJson(fp)
        
    doc['_id'] = uuid.uuid4().hex
    ls = ls + [doc]
    ioutils.saveText(fp, json.dumps(ls))
    return doc['_id']
#############################################
##### SAVE DOCUMENT
@app.route('/collection/<name>/<docid>', methods=['POST'])
@cross_origin(origin='localhost')
def collection_save_document_by_id(name, docid):
    doc = request.get_json()
    print('\ncollection [%s] save %s\n'% (name, docid))
    
    fp = os.path.join(DIR_COLLECTIONS, '%s.json' % name)
    ls = []
    if os.path.exists(fp):
        ls = ioutils.loadJson(fp)

    for i in range(len(ls)):
        if ls[i]['_id'] == docid:
            ls[i] = doc
            ls[i]['_id'] = docid

    ioutils.saveText(fp, json.dumps(ls))
    return 'ok'
#############################################
##### DELETE DOCUMENT
@app.route('/collection/<name>/<docid>', methods=['DELETE'])
@cross_origin(origin='localhost')
def collection_delete_document_by_id(name, docid):
    print('\ncollection [%s] DELETE %s\n'% (name, docid))
    
    fp = os.path.join(DIR_COLLECTIONS, '%s.json' % name)
    ls = []
    if os.path.exists(fp):
        ls = ioutils.loadJson(fp)

    for i in range(len(ls)):
        if ls[i]['_id'] == docid:
            del ls[i]
            break

    ioutils.saveText(fp, json.dumps(ls))
    return 'ok'
#############################################
##### GET DOCUMENT BY ID
@app.route('/collection/<name>/<docid>', methods=['GET'])
@cross_origin(origin='localhost')
def collection_get_document_by_id(name, docid):
    print('\ncollection [%s] save %s\n'% (name, docid))
    
    fp = os.path.join(DIR_COLLECTIONS, '%s.json' % name)
    ls = []
    if os.path.exists(fp):
        ls = ioutils.loadJson(fp)

    for i in range(len(ls)):
        if ls[i]['_id'] == docid:
            return json.dumps(ls[i])

    return abort(404)

if __name__ == "__main__":
    serverConfig = { 'file_root': os.getcwd(), 'port' : 5100 }
    configFile = os.path.join(os.getcwd(), 'server_config.json')
    
    if os.path.exists(configFile):
        f = open(configFile)
        content = f.read()
        f.close()
        serverConfig = json.loads(content)
    
    print(json.dumps(serverConfig))
    app.config['APP_STORE_FOLDER'] = serverConfig['file_root']
    app.run(port=serverConfig['port'])