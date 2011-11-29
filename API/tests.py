import unittest, sys
from models import *
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class GameObjectTest(unittest.TestCase):
    def setUp(self):
	self.testbed = testbed.Testbed()
	self.testbed.activate()
	self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
	self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
	
    def tearDown(self):
	self.testbed.deactivate()

    def test_create(self):
        go = GameObject()
	go.title = "Test title"
	go.description = "Test description"
	key = go.put()
	go2 = GameObject.get(key)
	self.assertEquals(go2.title, "Test title")
