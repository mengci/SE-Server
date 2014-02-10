from flask import Blueprint
from flask import request
from flask import render_template
from google.appengine.ext import ndb

from flask import json

import logging

from flask_wtf import Form
from wtforms.ext.appengine.db import model_form
from main import app,db,security

from models.models import TestModel, MongoTestModel

test_api = Blueprint('test_api', __name__)

@test_api.route("/api/tests/<test_id>", methods=['GET', 'POST'])
def test_creat(test_id=None):
  """ Test """
  if request.method == 'GET':
    tm = TestModel(parent=ndb.Key("TestModel","yo"),
        content = "dummy content %s " % (test_id))
    tm.put()
    return "{test_id = %s}" % (test_id,)
  else:
    return str(request.data)

@test_api.route("/api/tests", methods=['GET'])
def test_list():
    """ Test """
    ancestor_key = ndb.Key("TestModel","yo")
    tests = TestModel.query_testmodel(ancestor_key).fetch(20)
    tests = TestModel.query().fetch(20)
    return json.dumps([p.to_dict() for p in list(tests)])
    #return render_template('dump_dict_list.html', model_only=True ,dict_list=[i.__dict__ for i in tests])

@test_api.route("/api/tests/random", methods=['GET','DELETE'])
def test_random():
    """ Test """
    import random
    x = random.randint(0,1000)
    y = random.randint(0,1000)
    return '{"a":%s, "b":%s}' % (x,y)

@test_api.route("/api/tests/mongo_demo", methods=['GET'])
def test_mongo_demo():
    return render_template('mongo_test.html',models=[])

@test_api.route("/api/tests/mongo", methods=['GET','POST'])
def test_mongo():
    
    from bson import json_util
    
    if request.method == 'GET':
        doc = MongoTestModel.objects.all()
        app.logger.info(doc)
        return json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
        #return render_template('mongo_test.html', model_only=True ,models=doc)

    elif request.method == 'POST':
        k1 = request.form['k1']
        k2 = request.form['k2']
        model = MongoTestModel(k1=k1,k2=k2)
        doc = model.save()
        print doc.k1
        print doc.k2
        print doc.id
        app.logger.info(doc)
        return json_util.dumps(doc.to_mongo())

@test_api.route("/api/tests/sec", methods=['GET'])
def test_sec():
    """ Test """
    return '{"a":%s, "b":%s}' % (x,y)
