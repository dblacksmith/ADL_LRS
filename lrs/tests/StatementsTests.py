from django.test import TestCase
from django.test.utils import setup_test_environment
from django.core.urlresolvers import reverse
from lrs import views, models
from os import path
from django.conf import settings
import sys
import json
import base64
import uuid
from datetime import datetime, timedelta
from django.utils.timezone import utc
from lrs.objects import Activity, Statement
import time
import urllib
from lrs.util import retrieve_statement
import pdb
import hashlib
import pprint

class StatementsTests(TestCase):
    def setUp(self):
        if not settings.HTTP_AUTH_ENABLED:
            settings.HTTP_AUTH_ENABLED = True

        self.username = "tester1"
        self.email = "test1@tester.com"
        self.password = "test"
        self.auth = "Basic %s" % base64.b64encode("%s:%s" % (self.username, self.password))
        form = {"username":self.username, "email":self.email,"password":self.password,"password2":self.password}
        response = self.client.post(reverse(views.register),form, X_Experience_API_Version="1.0")

        if settings.HTTP_AUTH_ENABLED:
            response = self.client.post(reverse(views.register),form, X_Experience_API_Version="1.0")
        
        self.firstTime = str(datetime.utcnow().replace(tzinfo=utc).isoformat())
        self.guid1 = str(uuid.uuid1())

    def bunchostmts(self):
        self.guid2 = str(uuid.uuid1())
        self.guid3 = str(uuid.uuid1())    
        self.guid4 = str(uuid.uuid1())
        self.guid5 = str(uuid.uuid1())
        self.guid6 = str(uuid.uuid1())
        self.guid7 = str(uuid.uuid1())
        self.guid8 = str(uuid.uuid1())
        self.guid9 = str(uuid.uuid1())        
        self.guid10 = str(uuid.uuid1())
        self.cguid1 = str(uuid.uuid1())
        self.cguid2 = str(uuid.uuid1())    
        self.cguid3 = str(uuid.uuid1())
        self.cguid4 = str(uuid.uuid1())
        self.cguid5 = str(uuid.uuid1())
        self.cguid6 = str(uuid.uuid1())
        self.cguid7 = str(uuid.uuid1())
        self.cguid8 = str(uuid.uuid1())

        if settings.HTTP_AUTH_ENABLED:
            self.existStmt = Statement.Statement(json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
                "display": {"en-US":"created"}}, "object": {"id":"act:activity"},
                "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"},
                "authority":{"objectType":"Agent","name":"tester1","mbox":"mailto:test1@tester.com"}}))
        else:
            self.existStmt = Statement.Statement(json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
                "display": {"en-US":"created"}}, "object": {"id":"act:activity"},
                "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"}}))            
        
        self.exist_stmt_id = self.existStmt.model_object.statement_id


        self.existStmt1 = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
            "display": {"en-US":"created"}},"actor":{"objectType":"Agent","mbox":"mailto:s@s.com"},
            "object": {"objectType": "Activity", "id":"act:foogie",
            "definition": {"name": {"en-US":"testname2", "en-GB": "altname"},
            "description": {"en-US":"testdesc2", "en-GB": "altdesc"}, "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction",
            "interactionType": "fill-in","correctResponsesPattern": ["answer"],
            "extensions": {"ext:key1": "value1", "ext:key2": "value2","ext:key3": "value3"}}}, 
            "result": {"score":{"scaled":.85}, "completion": True, "success": True, "response": "kicked",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:key1": "value1", "ext:key2":"value2"}},
            "context":{"registration": self.cguid1, "contextActivities": {"other": {"id": "act:NewActivityID2"}},
            "revision": "food", "platform":"bard","language": "en-US", "extensions":{"ext:ckey1": "cval1",
            "ext:ckey2": "cval2"}}})        

        self.existStmt2 = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
            "display": {"en-US":"created"}},"actor":{"objectType":"Agent","mbox":"mailto:s@t.com"},
            "object": {"objectType": "Activity", "id":"act:foogie",
            "definition": {"name": {"en-US":"testname3", "en-GB": "altname"},
            "description": {"en-US":"testdesc3","en-GB":"altdesc"}, "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction",
            "interactionType": "fill-in","correctResponsesPattern": ["answers"],
            "extensions": {"ext:key11": "value11", "ext:key22": "value22","ext:key33": "value33"}}}, 
            "result": {"score":{"scaled":.75}, "completion": True, "success": True, "response": "shouted",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:dkey1": "dvalue1", "ext:dkey2":"dvalue2"}},
            "context":{"registration": self.cguid2, "contextActivities": {"other": {"id": "act:NewActivityID22"}},
            "revision": "food", "platform":"bard","language": "en-US", "extensions":{"ext:ckey11": "cval11",
            "ext:ckey22": "cval22"}}})        

        self.existStmt3 = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
            "display": {"en-US":"created"}},"actor":{"objectType":"Agent","mbox":"mailto:s@s.com"},
            "object": {"objectType": "Activity", "id":"act:foogals",
            "definition": {"name": {"en-US":"testname3"},"description": {"en-US":"testdesc3"}, "type": "cmi.interaction",
            "interactionType": "fill-in","correctResponsesPattern": ["answers"],
            "extensions": {"ext:key111": "value111", "ext:key222": "value222","ext:key333": "value333"}}}, 
            "result": {"score":{"scaled":.79}, "completion": True, "success": True, "response": "shouted",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:dkey1": "dvalue1", "ext:dkey2":"dvalue2"}},
            "context":{"registration": self.cguid3, "contextActivities": {"other": {"id": "act:NewActivityID22"}},
            "revision": "food", "platform":"bard","language": "en-US",
            "instructor":{"objectType": "Agent", "name":"bob", "mbox":"mailto:bob@bob.com"}, 
            "extensions":{"ext:ckey111": "cval111","ext:ckey222": "cval222"}}})        

        self.existStmt4 = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
            "display": {"en-US":"created"}},"actor":{"objectType":"Agent","mbox":"mailto:s@s.com"},
            "object": {"objectType": "Activity", "id":"act:foogal",
            "definition": {"name": {"en-US":"testname3"},"description": {"en-US":"testdesc3"}, "type": "cmi.interaction",
            "interactionType": "fill-in","correctResponsesPattern": ["answers"],
            "extensions": {"ext:key111": "value111", "ext:key222": "value222","ext:key333": "value333"}}}, 
            "result": {"score":{"scaled":.79}, "completion": True, "success": True, "response": "shouted",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:dkey1": "dvalue1", "ext:dkey2":"dvalue2"}},
            "context":{"registration": self.cguid4, "contextActivities": {"other": {"id": "act:NewActivityID22"}},
            "revision": "food", "platform":"bard","language": "en-US","instructor":{"name":"bill", "mbox":"mailto:bill@bill.com"},
            "extensions":{"ext:ckey111": "cval111","ext:ckey222": "cval222"}}})

        self.existStmt5 = json.dumps({"object":{"objectType":"Agent","name":"jon","mbox":"mailto:jon@jon.com"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/created","display": {"en-US":"created"}},
            "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"}})

        self.existStmt6 = json.dumps({"actor": {"objectType":"Agent","name":"max","mbox":"mailto:max@max.com"}, 
                                      "object":{"id": "act:test_activity"},"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
                                      "display": {"en-US":"created"}}})

        self.existStmt7 = json.dumps({"object": {"objectType":"Agent","name":"max","mbox":"mailto:max@max.com"},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/created","display": {"en-US":"created"}},
            "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"}})

        self.existStmt8 = json.dumps({"object": {"objectType":"Agent","name":"john","mbox":"mailto:john@john.com"},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/missed","display": {"en-US":"missed"}},
            "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"}})

        self.existStmt9 = json.dumps({"actor":{"objectType":"Agent","mbox":"mailto:sub@sub.com"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/missed"},"object":{"objectType":"SubStatement",
            "actor":{"objectType":"Agent","mbox":"mailto:ss@ss.com"},"verb": {"id":"verb:verb/url/nested"},
            "object": {"objectType":"activity", "id":"act:testex.com"}, "result":{"completion": True, "success": True,
            "response": "kicked"}, "context":{"registration": self.cguid6,
            "contextActivities": {"other": {"id": "act:NewActivityID"}},"revision": "foo", "platform":"bar",
            "language": "en-US", "extensions":{"ext:k1": "v1", "ext:k2": "v2"}}}})

        self.existStmt10 = json.dumps({"actor":{"objectType":"Agent","mbox":"mailto:ref@ref.com"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/missed"},"object":{"objectType":"StatementRef",
            "id":str(self.exist_stmt_id)}})

        # Put statements
        param = {"statementId":self.guid1}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt1
        self.putresponse1 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(self.putresponse1.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=2)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid1).update(stored=time)


        param = {"statementId":self.guid3}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt3
        self.putresponse3 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(self.putresponse3.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=3)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid3).update(stored=time)

        
        param = {"statementId":self.guid4}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt4
        self.putresponse4 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(self.putresponse4.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=4)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid4).update(stored=time)

        self.secondTime = str((datetime.utcnow()+timedelta(seconds=4)).replace(tzinfo=utc).isoformat())
        
        param = {"statementId":self.guid2}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt2
        self.putresponse2 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")       
        self.assertEqual(self.putresponse2.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=6)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid2).update(stored=time)


        param = {"statementId":self.guid5}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt5
        self.putresponse5 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(self.putresponse5.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=7)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid5).update(stored=time)
        

        param = {"statementId":self.guid6}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt6
        self.putresponse6 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(self.putresponse6.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=8)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid6).update(stored=time)

        
        param = {"statementId":self.guid7}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt7        
        self.putresponse7 = self.client.put(path, stmt_payload,  content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(self.putresponse7.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=9)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid7).update(stored=time)
        

        param = {"statementId":self.guid8}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt8        
        self.putresponse8 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(self.putresponse8.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=10)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid8).update(stored=time)
        
        param = {"statementId": self.guid9}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt9        
        self.putresponse9 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(self.putresponse9.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=11)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid9).update(stored=time)

        param = {"statementId": self.guid10}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = self.existStmt10        
        self.putresponse10 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(self.putresponse10.status_code, 204)
        time = retrieve_statement.convert_to_utc(str((datetime.utcnow()+timedelta(seconds=11)).replace(tzinfo=utc).isoformat()))
        stmt = models.statement.objects.filter(statement_id=self.guid10).update(stored=time)


    def test_post_with_no_valid_params(self):
        # Error will be thrown in statements class
        resp = self.client.post(reverse(views.statements), {"feet":"yes","hands": {"id":"http://example.com/test_post"}},
            content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(resp.status_code, 400)

    def test_post(self):
        stmt = json.dumps({"actor":{"objectType": "Agent", "mbox":"mailto:t@t.com", "name":"bob"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/passed","display": {"en-US":"passed"}},
            "object": {"id":"act:test_post"}})
        response = self.client.post(reverse(views.statements), stmt, content_type="application/json",
            Authorization=self.auth, X_Experience_API_Version="1.0")
        
        self.assertEqual(response.status_code, 200)
        act = models.activity.objects.get(activity_id="act:test_post")
        self.assertEqual(act.activity_id, "act:test_post")
        agent = models.agent.objects.get(mbox="mailto:t@t.com")
        self.assertEqual(agent.name, "bob")

    def test_post_wrong_duration(self):
        stmt = json.dumps({"actor":{'objectType':'Person','name':'jon',
            'mbox':'mailto:jon@example.com'},'verb': {"id":"verb:verb/url"},"object": {'id':'act:activity13'}, 
            "result": {'completion': True, 'success': True, 'response': 'yes', 'duration': 'wrongduration',
            'extensions':{'ext:key1': 'value1', 'ext:key2':'value2'}}})

        response = self.client.post(reverse(views.statements), stmt, content_type="application/json",
            Authorization=self.auth, X_Experience_API_Version="1.0")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, "Unable to parse duration string u'wrongduration'")


    def test_post_stmt_ref_no_existing_stmt(self):
        stmt = json.dumps({"actor":{"objectType":"Agent","mbox":"mailto:ref@ref.com"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/missed"},"object":{"objectType":"StatementRef",
            "id":"aaaaaaaaa"}})
        response = self.client.post(reverse(views.statements), stmt, content_type="application/json",
            Authorization=self.auth, X_Experience_API_Version="1.0")        

        self.assertEqual(response.status_code, 404)


    def test_post_with_actor(self):
        stmt = json.dumps({"actor":{"mbox":"mailto:mr.t@example.com"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/passed","display": {"en-US":"passed"}},
            "object": {"id":"act:i.pity.the.fool"}})
        
        response = self.client.post(reverse(views.statements), stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 200)
        agent = models.agent.objects.get(mbox="mailto:mr.t@example.com")

    def test_list_post(self):
        stmts = json.dumps([{"verb":{"id": "http://adlnet.gov/expapi/verbs/passed","display": {"en-US":"passed"}},
            "object": {"id":"act:test_list_post"}, "actor":{"objectType":"Agent", "mbox":"mailto:t@t.com"}},
            {"verb":{"id": "http://adlnet.gov/expapi/verbs/failed","display": {"en-GB":"failed"}},
            "object": {"id":"act:test_list_post1"}, "actor":{"objectType":"Agent", "mbox":"mailto:t@t.com"}}])
        
        response = self.client.post(reverse(views.statements), stmts,  content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 200)
        activity1 = models.activity.objects.get(activity_id="act:test_list_post")
        activity2 = models.activity.objects.get(activity_id="act:test_list_post1")
        stmt1 = models.statement.objects.get(stmt_object=activity1)
        stmt2 = models.statement.objects.get(stmt_object=activity2)
        verb1 = models.Verb.objects.get(id=stmt1.verb.id)
        verb2 = models.Verb.objects.get(id=stmt2.verb.id)
        lang_map1 = verb1.display.all()[0]
        lang_map2 = verb2.display.all()[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(stmt1.verb.verb_id, "http://adlnet.gov/expapi/verbs/passed")
        self.assertEqual(stmt2.verb.verb_id, "http://adlnet.gov/expapi/verbs/failed")
        
        self.assertEqual(lang_map1.key, "en-US")
        self.assertEqual(lang_map1.value, "passed")
        self.assertEqual(lang_map2.key, "en-GB")
        self.assertEqual(lang_map2.value, "failed")


    def test_put(self):
        guid = str(uuid.uuid1())

        param = {"statementId":guid}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/passed","display": {"en-US":"passed"}},
            "object": {"id":"act:test_put"},"actor":{"objectType":"Agent", "mbox":"mailto:t@t.com"}})

        putResponse = self.client.put(path, stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(putResponse.status_code, 204)
        stmt = models.statement.objects.get(statement_id=guid)

        act = models.activity.objects.get(activity_id="act:test_put")
        self.assertEqual(act.activity_id, "act:test_put")

        self.assertEqual(stmt.actor.mbox, "mailto:t@t.com")

        if settings.HTTP_AUTH_ENABLED:
            self.assertEqual(stmt.authority.name, "tester1")
            self.assertEqual(stmt.authority.mbox, "mailto:test1@tester.com")
        
        
        self.assertEqual(stmt.verb.verb_id, "http://adlnet.gov/expapi/verbs/passed")

    def test_put_with_substatement(self):
        con_guid = str(uuid.uuid1())
        st_guid = str(uuid.uuid1())

        param = {"statementId": st_guid}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt = json.dumps({"actor":{"objectType":"Agent","mbox":"mailto:sass@sass.com"},
            "verb": {"id":"verb:verb/url/tested"}, "object":{"objectType":"SubStatement",
            "actor":{"objectType":"Agent","mbox":"mailto:ss@ss.com"},"verb": {"id":"verb:verb/url/nested"},
            "object": {"objectType":"activity", "id":"act:testex.com"}, "result":{"completion": True, "success": True,
            "response": "kicked"}, "context":{"registration": con_guid,
            "contextActivities": {"other": {"id": "act:NewActivityID"}},"revision": "foo", "platform":"bar",
            "language": "en-US", "extensions":{"ext:k1": "v1", "ext:k2": "v2"}}}})
        
        response = self.client.put(path, stmt, content_type="application/json",
            Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 204)

        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        get_response = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(get_response.status_code, 200)
        rsp = get_response.content
        self.assertIn("objectType",rsp)
        self.assertIn("SubStatement", rsp)
        self.assertIn("actor",rsp)
        self.assertIn("ss@ss.com",rsp)
        self.assertIn("verb",rsp)
        self.assertIn("verb:verb/url/nested", rsp)
        self.assertIn("Activity", rsp)
        self.assertIn("act:testex.com", rsp)
        self.assertIn("result", rsp)
        self.assertIn("completion",rsp)
        self.assertIn("success", rsp)
        self.assertIn("response", rsp)
        self.assertIn("kicked", rsp)
        self.assertIn("context", rsp)
        self.assertIn(con_guid, rsp)
        self.assertIn("contextActivities", rsp)
        self.assertIn("other", rsp)
        self.assertIn("revision", rsp)
        self.assertIn("foo", rsp)
        self.assertIn("platform", rsp)
        self.assertIn("bar", rsp)
        self.assertIn("language", rsp)
        self.assertIn("en-US", rsp)
        self.assertIn("extensions", rsp)
        self.assertIn("ext:k1", rsp)
        self.assertIn("v1", rsp)
        self.assertIn("ext:k2", rsp)
        self.assertIn("v2", rsp)                                                                                                                                                                                                                

    def test_no_content_put(self):
        guid = str(uuid.uuid1())
        
        param = {"statementId":guid}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        stmt = json.dumps({})

        putResponse = self.client.put(path, stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(putResponse.status_code, 400)

    def test_existing_stmtID_put(self):
        guid = str(uuid.uuid1())

        existStmt = Statement.Statement(json.dumps({"statement_id":guid,
            "verb":{"id": "http://adlnet.gov/expapi/verbs/passed","display": {"en-US":"passed"}},
            "object": {"id":"act:activity"},"actor":{"objectType":"Agent", "mbox":"mailto:t@t.com"}}))

        param = {"statementId":guid}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        stmt = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/passed","display": {"en-US":"passed"}},
            "object":{"id":"act:test_existing_put"}, "actor":{"objectType":"Agent", "mbox":"mailto:t@t.com"}})

        putResponse = self.client.put(path, stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        
        self.assertEqual(putResponse.status_code, 409)        

    def test_missing_stmtID_put(self):        
        stmt = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/passed","display": {"en-US":"passed"}},
            "object": {"id":"act:test_put"},"actor":{"objectType":"Agent", "mbox":"mailto:t@t.com"}})
        response = self.client.put(reverse(views.statements), stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.content, "Error -- statements - method = PUT, but statementId paramater is missing")

    def test_get(self):
        self.bunchostmts()
        param = {"statementId":self.guid1}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        getResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(getResponse.status_code, 200)
        rsp = getResponse.content
        self.assertIn(self.guid1, rsp)

    def test_get_no_existing_ID(self):
        param = {"statementId":"aaaaaa"}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        getResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(getResponse.status_code, 404)

    def test_get_no_auth(self):
        # Will return 200 if HTTP_AUTH_ENABLED is enabled
        if settings.HTTP_AUTH_ENABLED:
            param = {"statementId":self.guid1}
            path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
            getResponse = self.client.get(path, X_Experience_API_Version="1.0")
            self.assertEqual(getResponse.status_code, 401)

    def test_get_no_statementid(self):
        self.bunchostmts()
        getResponse = self.client.get(reverse(views.statements), X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(getResponse.status_code, 200)
        jsn = json.loads(getResponse.content)
        # Will only return 10 since that is server limit
        self.assertEqual(len(jsn["statements"]), 10)
        
    def test_since_filter(self):
        self.bunchostmts()
        # Test since - should only get existStmt1-8 since existStmt is stored at same time as firstTime
        param = {"since": self.firstTime}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))      
        sinceGetResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)

        self.assertEqual(sinceGetResponse.status_code, 200)
        rsp = sinceGetResponse.content
        self.assertIn(self.guid1, rsp)
        self.assertIn(self.guid2, rsp)
        self.assertIn(self.guid3, rsp)
        self.assertIn(self.guid4, rsp)
        self.assertIn(self.guid5, rsp)
        self.assertIn(self.guid6, rsp)
        self.assertIn(self.guid7, rsp)
        self.assertIn(self.guid8, rsp)

    def test_until_filter(self):
        self.bunchostmts()
        # Test until
        param = {"until": self.secondTime}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        untilGetResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(untilGetResponse.status_code, 200)
        rsp = untilGetResponse.content
        self.assertIn(self.guid1, rsp)
        self.assertIn(self.guid3, rsp)
        self.assertIn(self.guid4, rsp)
        self.assertNotIn(self.guid2, rsp)
        self.assertNotIn(self.guid5, rsp)
        self.assertNotIn(self.guid6, rsp)
        self.assertNotIn(self.guid7, rsp)
        self.assertNotIn(self.guid8, rsp)

    def test_activity_object_filter(self):
        self.bunchostmts()
        # Test activity object
        param = {"object":{"objectType": "Activity", "id":"act:foogie"}}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        activityObjectGetResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth,
            Accept_Language='en-GB')
        self.assertEqual(activityObjectGetResponse.status_code, 200)
        rsp = activityObjectGetResponse.content
        self.assertIn(self.guid1, rsp)
        self.assertIn(self.guid2, rsp)
        self.assertNotIn(self.guid3, rsp)
        self.assertNotIn(self.guid4, rsp)
        self.assertNotIn(self.guid5, rsp)
        self.assertNotIn(self.guid6, rsp)
        self.assertNotIn(self.guid7, rsp)
        self.assertNotIn(self.guid8, rsp)
        # Should not be in response b/c of language header
        self.assertNotIn("testdesc3", rsp)
        self.assertNotIn("testname3", rsp)

    def test_no_actor(self):
        # Test actor object
        self.bunchostmts()
        param = {"object":{"objectType": "Agent", "mbox":"mailto:nobody@example.com"}}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        actorObjectGetResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        
        self.assertEqual(actorObjectGetResponse.status_code, 200)
        stmts = json.loads(actorObjectGetResponse.content)
        # Will return 10 since that is server limit
        self.assertEqual(len(stmts["statements"]), 0)

    def test_verb_filter(self):
        self.bunchostmts()
        param = {"verb":"http://adlnet.gov/expapi/verbs/missed"}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        verb_response = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(verb_response.status_code, 200)
        rsp = verb_response.content
        self.assertIn(self.guid8, rsp)
        self.assertIn(self.guid9, rsp)        
        self.assertNotIn(self.guid7, rsp)
        self.assertNotIn(self.guid6, rsp)
        self.assertNotIn(self.guid5, rsp)
        self.assertNotIn(self.guid4, rsp)
        self.assertNotIn(self.guid2, rsp)
        self.assertNotIn(self.guid3, rsp)
        self.assertNotIn(self.guid1, rsp)


    def test_actor_object_filter(self):
        self.bunchostmts()
        # Test actor object
        param = {"object":{"objectType": "Agent", "name":"jon","mbox":"mailto:jon@jon.com"}}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        actorObjectGetResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        
        self.assertEqual(actorObjectGetResponse.status_code, 200)
        self.assertContains(actorObjectGetResponse, self.guid5)
        self.assertNotIn(self.guid4, actorObjectGetResponse)
        self.assertNotIn(self.guid2, actorObjectGetResponse)
        self.assertNotIn(self.guid3, actorObjectGetResponse)
        self.assertNotIn(self.guid1, actorObjectGetResponse)

    
    def test_statement_ref_object_filter(self):
        self.bunchostmts()
        param = {"object":{"objectType": "StatementRef", "id":str(self.exist_stmt_id)}}
            
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        sub_object_get_response = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(sub_object_get_response.status_code, 200)
        self.assertContains(sub_object_get_response,self.guid10)
        self.assertNotIn(self.guid2, sub_object_get_response)
        self.assertNotIn(self.guid3, sub_object_get_response)
        self.assertNotIn(self.guid1, sub_object_get_response)
        self.assertNotIn(self.guid5, sub_object_get_response)
        self.assertNotIn(self.guid4, sub_object_get_response)
        self.assertNotIn(self.guid7, sub_object_get_response)
        self.assertNotIn(self.guid8, sub_object_get_response)        
        self.assertNotIn(self.guid9, sub_object_get_response)


    def test_registration_filter(self):
        self.bunchostmts()
        # Test Registration
        param = {"registration": self.cguid4}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        registrationPostResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)

        self.assertEqual(registrationPostResponse.status_code, 200)
        self.assertContains(registrationPostResponse,self.guid4)
        self.assertNotIn(self.guid2, registrationPostResponse)
        self.assertNotIn(self.guid3, registrationPostResponse)
        self.assertNotIn(self.guid1, registrationPostResponse)
        self.assertNotIn(self.guid5, registrationPostResponse)
        self.assertNotIn(self.guid6, registrationPostResponse)
        self.assertNotIn(self.guid7, registrationPostResponse)
        self.assertNotIn(self.guid8, registrationPostResponse)

    def test_ascending_filter(self):
        self.bunchostmts()
        # Test actor
        ascending_get_response = self.client.get(reverse(views.statements), 
            {"ascending": True},content_type="application/x-www-form-urlencoded", X_Experience_API_Version="1.0", Authorization=self.auth)

        self.assertEqual(ascending_get_response.status_code, 200)
        rsp = ascending_get_response.content
        self.assertIn(self.guid1, rsp)
        self.assertIn(self.guid2, rsp)
        self.assertIn(self.guid3, rsp)
        self.assertIn(self.guid4, rsp)
        self.assertIn(self.guid5, rsp)
        self.assertIn(self.guid6, rsp)
        self.assertIn(self.guid7, rsp)
        self.assertIn(self.guid8, rsp)
        self.assertIn(str(self.exist_stmt_id), rsp)

    def test_actor_filter(self):
        self.bunchostmts()
        # Test actor
        actorGetResponse = self.client.post(reverse(views.statements), 
            {"actor":{"objectType": "Agent", "mbox":"mailto:s@s.com"}},
             content_type="application/x-www-form-urlencoded", X_Experience_API_Version="1.0", Authorization=self.auth)
        
        self.assertEqual(actorGetResponse.status_code, 200)
        rsp = actorGetResponse.content
        self.assertIn(self.guid1, rsp)
        self.assertIn(self.guid3, rsp)
        self.assertIn(self.guid4, rsp)                        
        self.assertIn(self.guid5, rsp)
        self.assertIn(self.guid7, rsp)
        self.assertIn(self.guid8, rsp)
        self.assertIn(str(self.exist_stmt_id), rsp)        
        self.assertNotIn(self.guid6, rsp)
        self.assertNotIn(self.guid2, rsp)

    def test_instructor_filter(self):
        self.bunchostmts()
        # Test instructor - will only return one b/c actor in stmt supercedes instructor in context
        instructorGetResponse = self.client.post(reverse(views.statements), 
                                                {"instructor":{"name":"bill","mbox":"mailto:bill@bill.com"}},  
                                                content_type="application/x-www-form-urlencoded", X_Experience_API_Version="1.0", Authorization=self.auth)
        
        self.assertEqual(instructorGetResponse.status_code, 200)
        self.assertContains(instructorGetResponse, self.guid4)
        self.assertNotIn(self.guid2, instructorGetResponse)
        self.assertNotIn(self.guid3, instructorGetResponse)
        self.assertNotIn(self.guid1, instructorGetResponse)
        self.assertNotIn(self.guid5, instructorGetResponse)
        self.assertNotIn(self.guid4, instructorGetResponse)
        self.assertNotIn(self.guid6, instructorGetResponse)
        self.assertNotIn(self.guid7, instructorGetResponse)
        self.assertNotIn(self.guid8, instructorGetResponse)

    def test_authoritative_filter(self):
        self.bunchostmts()
        # Test authoritative
        self.username = "tester1"
        self.email = "test1@tester.com"
        self.password = "test"
        self.auth = "Basic %s" % base64.b64encode("%s:%s" % (self.username, self.password))
        form = {"username":self.username, "email":self.email,"password":self.password,"password2":self.password}
        response = self.client.post(reverse(views.register),form, X_Experience_API_Version="1.0")
        
        auth_stmt = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/passed",
            "display": {"en-US":"created"}},"actor":{"objectType":"Agent","mbox":"mailto:s@s.com"},
            "object": {"objectType": "Activity", "id":"act:foogie",
            "definition": {"name": {"en-US":"testname2", "en-GB": "altname"},
            "description": {"en-US":"testdesc2", "en-GB": "altdesc"}, "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction",
            "interactionType": "fill-in","correctResponsesPattern": ["answer"],
            "extensions": {"ext:key1": "value1", "ext:key2": "value2","ext:key3": "value3"}}}, 
            "result": {"score":{"scaled":.85}, "completion": True, "success": True, "response": "kicked",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:key1": "value1", "ext:key2":"value2"}},
            "context":{"registration": self.cguid7, "contextActivities": {"other": {"id": "act:NewActivityID2"}},
            "revision": "food", "platform":"bard","language": "en-US", "extensions":{"ext:ckey1": "cval1",
            "ext:ckey2": "cval2"}}})

        post_response = self.client.post(reverse(views.statements), auth_stmt, content_type="application/json",
            Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(post_response.status_code, 200)

        params = {"authoritative": False, "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"},
            "object":{"objectType": "Activity", "id":"act:foogie",
            "definition": {"name": {"en-US":"testname2", "en-GB": "altname"},
            "description": {"en-US":"testdesc2", "en-GB": "altdesc"}, "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction",
            "interactionType": "fill-in","correctResponsesPattern": ["answer"],
            "extensions": {"ext:key1": "value1", "ext:key2": "value2","ext:key3": "value3"}}}}

        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(params))        
        auth_get_response = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)        
        self.assertEqual(auth_get_response.status_code, 200)
        
        stmts = json.loads(auth_get_response.content)
        self.assertEqual(len(stmts["statements"]), 2)

    def test_limit_filter(self):
        self.bunchostmts()
        # Test limit
        limitGetResponse = self.client.post(reverse(views.statements),{"limit":1}, content_type="application/x-www-form-urlencoded", X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(limitGetResponse.status_code, 200)
        rsp = limitGetResponse.content
        respList = json.loads(rsp)
        stmts = respList["statements"]
        self.assertEqual(len(stmts), 1)
        self.assertIn(self.guid10, rsp)

    def test_sparse_filter(self):
        self.bunchostmts()
        # Test sparse
        sparseGetResponse = self.client.post(reverse(views.statements),{"sparse": False}, content_type="application/x-www-form-urlencoded", X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(sparseGetResponse.status_code, 200)
        rsp = sparseGetResponse.content

        self.assertIn("definition", rsp)        
        self.assertIn("en-GB", rsp)
        self.assertIn("altdesc", rsp)
        self.assertIn("altname", rsp)


        # Should display full lang map (won"t find testdesc2 since activity class will merge activities with same id together)
        self.assertIn("testdesc3", rsp)

    def test_linked_filters(self):
        self.bunchostmts()
        # Test reasonable linked query
        param = {"verb":"http://adlnet.gov/expapi/verbs/created", "object":{"objectType": "Activity", "id":"act:foogie"}, "since":self.secondTime, "authoritative":"False", "sparse": False}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        linkedGetResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(linkedGetResponse.status_code, 200)
        self.assertContains(linkedGetResponse, self.guid2)

    def test_language_header_filter(self):
        self.bunchostmts()
        param = {"limit":1, "object":{"objectType": "Activity", "id":"act:foogie"}}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        lang_get_response = self.client.get(path, Accept_Language="en-US", X_Experience_API_Version="1.0", Authorization=self.auth)

        self.assertEqual(lang_get_response.status_code, 200)
        rsp = lang_get_response.content
        resp_list = json.loads(rsp)
        stmts = resp_list["statements"]
        self.assertEqual(len(stmts), 1)
        self.assertIn("en-US", rsp)
        self.assertNotIn("en-GB", rsp)

    # Sever activities are PUT, but should be 5 since two have same ID and auth
    def test_number_of_activities(self):
        self.bunchostmts()
        acts = len(models.activity.objects.all())
        self.assertEqual(6, acts)

    def test_update_activity_wrong_auth(self):
        # Will respond with 200 if HTTP_AUTH_ENABLED is enabled
        if settings.HTTP_AUTH_ENABLED:
            existStmt1 = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
                "display": {"en-US":"created"}},"actor":{"objectType":"Agent","mbox":"mailto:s@s.com"},
                "object": {"objectType": "Activity", "id":"act:foogie",
                "definition": {"name": {"en-US":"testname2", "en-GB": "altname"},
                "description": {"en-US":"testdesc2", "en-GB": "altdesc"}, "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction",
                "interactionType": "fill-in","correctResponsesPattern": ["answer"],
                "extensions": {"ext:key1": "value1", "ext:key2": "value2","ext:key3": "value3"}}}, 
                "result": {"score":{"scaled":.85}, "completion": True, "success": True, "response": "kicked",
                "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:key1": "value1", "ext:key2":"value2"}},
                "context":{"registration": str(uuid.uuid1()), "contextActivities": {"other": {"id": "act:NewActivityID2"}},
                "revision": "food", "platform":"bard","language": "en-US", "extensions":{"ext:ckey1": "cval1",
                "ext:ckey2": "cval2"}}})
            param = {"statementId":self.guid1}
            path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
            stmt_payload = existStmt1
            putresponse1 = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
            
            wrong_username = "tester2"
            wrong_email = "test2@tester.com"
            wrong_password = "test2"
            wrong_auth = "Basic %s" % base64.b64encode("%s:%s" % (wrong_username, wrong_password))
            form = {"username":wrong_username, "email":wrong_email,"password":wrong_password,
                "password2":wrong_password}
            response = self.client.post(reverse(views.register),form, X_Experience_API_Version="1.0")

            stmt = json.dumps({"verb":{"id":"verb:verb/uri/attempted"},"actor":{"objectType":"Agent", "mbox":"mailto:r@r.com"},
                "object": {"objectType": "Activity", "id":"act:foogie",
                "definition": {"name": {"en-US":"testname3"},"description": {"en-US":"testdesc3"},
                "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction","interactionType": "fill-in","correctResponsesPattern": ["answer"],
                "extensions": {"ext:key1": "value1", "ext:key2": "value2","ext:key3": "value3"}}}, 
                "result": {"score":{"scaled":.85}, "completion": True, "success": True, "response": "kicked",
                "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:key1": "value1", "ext:key2":"value2"}},
                "context":{"registration": str(uuid.uuid1()), "contextActivities": {"other": {"id": "act:NewActivityID2"}},
                "revision": "food", "platform":"bard","language": "en-US", "extensions":{"ext:ckey1": "cval1",
                "ext:ckey2": "cval2"}}, "authority":{"objectType":"Agent","name":"auth","mbox":"mailto:auth@example.com"}})
            
            post_response = self.client.post(reverse(views.statements), stmt, content_type="application/json",
                Authorization=wrong_auth, X_Experience_API_Version="1.0")
            self.assertEqual(post_response.status_code, 403)
            self.assertEqual(post_response.content, "This ActivityID already exists, and you do not have" + 
                            " the correct authority to create or update it.")

    def test_update_activity_correct_auth(self):
        self.bunchostmts()
        stmt = json.dumps({"verb": {"id":"verb:verb/url/changed-act"},"actor":{"objectType":"Agent", "mbox":"mailto:l@l.com"},
            "object": {"objectType": "Activity", "id":"act:foogie",
            "definition": {"name": {"en-US":"testname3"},"description": {"en-US":"testdesc3"},
            "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction","interactionType": "fill-in","correctResponsesPattern": ["answer"],
            "extensions": {"ext:key1": "value1", "ext:key2": "value2","ext:key3": "value3"}}}, 
            "result": {"score":{"scaled":.85}, "completion": True, "success": True, "response": "kicked",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:key1": "value1", "ext:key2":"value2"}},
            "context":{"registration": self.cguid8, "contextActivities": {"other": {"id": "act:NewActivityID2"}},
            "revision": "food", "platform":"bard","language": "en-US", "extensions":{"ext:ckey1": "cval1",
            "ext:ckey2": "cval2"}}, "authority":{"objectType":"Agent","name":"auth","mbox":"mailto:auth@example.com"}})

        post_response = self.client.post(reverse(views.statements), stmt, content_type="application/json",
            Authorization=self.auth, X_Experience_API_Version="1.0")
        
        act = models.activity.objects.get(activity_id="act:foogie")
        act_def = models.activity_definition.objects.get(activity=act)

        name_set = act_def.name.all()
        desc_set = act_def.description.all()

        for ns in name_set:
            if ns.key == 'en-GB':
                self.assertEqual(ns.value, 'altname')
            elif ns.key == 'en-US':
                self.assertEqual(ns.value, 'testname3')

        for ds in desc_set:
            if ds.key == 'en-GB':
                self.assertEqual(ds.value, 'altdesc')
            elif ds.key == 'en-US':
                self.assertEqual(ds.value, 'testdesc3')

    def test_cors_post_put(self):
        bdy = {"statementId": "886313e1-3b8a-5372-9b90-0c9aee199e5d"}
        bdy["content"] = {"verb":{"id":"verb:verb/url"}, "actor":{"objectType":"Agent", "mbox": "mailto:r@r.com"},
            "object": {"id":"act:test_cors_post_put"}}
        bdy["Authorization"] = self.auth
        bdy["Content-Type"] = "application/json"
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode({"method":"PUT"}))
        response = self.client.post(path, bdy, content_type="application/x-www-form-urlencoded", X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 204)

        act = models.activity.objects.get(activity_id="act:test_cors_post_put")
        self.assertEqual(act.activity_id, "act:test_cors_post_put")

        # This agent is created from registering an auth user, so won't be created if no HTTP_AUTH_ENABLED
        if settings.HTTP_AUTH_ENABLED:
            agent = models.agent.objects.get(mbox="mailto:test1@tester.com")
            self.assertEqual(agent.name, "tester1")
            self.assertEqual(agent.mbox, "mailto:test1@tester.com")

    def test_issue_put(self):
        stmt_id = "33f60b35-e1b2-4ddc-9c6f-7b3f65244430" 
        stmt = json.dumps({"verb":{"id":"verb:verb/uri"},"object":{"id":"act:scorm.com/JsTetris_TCAPI","definition":{"type":"media",
            "name":{"en-US":"Js Tetris - Tin Can Prototype"},"description":{"en-US":"A game of tetris."}}},
            "context":{"contextActivities":{"grouping":{"id":"act:scorm.com/JsTetris_TCAPI"}},
            "registration":"6b1091be-2833-4886-b4a6-59e5e0b3c3f4"},
            "actor":{"mbox":"mailto:tom.creighton.ctr@adlnet.gov","name":"Tom Creighton"}})

        path = "%s?%s" % (reverse(views.statements), urllib.urlencode({"statementId":stmt_id}))
        put_stmt = self.client.put(path, stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(put_stmt.status_code, 204) 

    def test_post_with_group(self):
        ot = "Group"
        name = "the group ST"
        mbox = "mailto:the.groupST@example.com"
        members = [{"name":"agentA","mbox":"mailto:agentA@example.com"},
                    {"name":"agentB","mbox":"mailto:agentB@example.com"}]
        group = json.dumps({"objectType":ot, "name":name, "mbox":mbox,"member":members})

        stmt = json.dumps({"actor":group,"verb":{"id": "http://verb/uri/created", "display":{"en-US":"created"}},
            "object": {"id":"act:i.pity.the.fool"}})
        response = self.client.post(reverse(views.statements), stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 200)
        g = models.agent.objects.get(mbox="mailto:the.groupST@example.com")
        self.assertEquals(g.name, name)
        self.assertEquals(g.mbox, mbox)
        mems = g.member.values_list("name", flat=True)
        self.assertEquals(len(mems), 2)
        self.assertIn("agentA", mems)
        self.assertIn("agentB", mems)
        # pdb.set_trace()

    def test_issue_put_no_version_header(self):
        stmt_id = '33f60b35-e1b2-4ddc-9c6f-7b3f65244431'
        stmt = json.dumps({"verb":"verb:completed","object":{"id":"act:scorm.com/JsTetris_TCAPI/level2",
            "definition":{"type":"media","name":{"en-US":"Js Tetris Level2"},
            "description":{"en-US":"Starting at 1, the higher the level, the harder the game."}}},
            "result":{"extensions":{"ext:time":104,"ext:apm":229,"ext:lines":5},"score":{"raw":9911,"min":0}},
            "context":{"contextActivities":{"grouping":{"id":"act:scorm.com/JsTetris_TCAPI"}},
            "registration":"b7be7d9d-bfe2-4917-8ccd-41a0d18dd953"},
            "actor":{"name":"tom creighton","mbox":"mailto:tom@example.com"}})

        path = '%s?%s' % (reverse(views.statements), urllib.urlencode({"statementId":stmt_id}))
        put_stmt = self.client.put(path, stmt, content_type="application/json", Authorization=self.auth)
        self.assertEqual(put_stmt.status_code, 400)

    def test_issue_put_wrong_version_header(self):
        stmt_id = '33f60b35-e1b2-4ddc-9c6f-7b3f65244432'
        stmt = json.dumps({"verb":"verb:completed","object":{"id":"act:scorm.com/JsTetris_TCAPI/level2",
            "definition":{"type":"media","name":{"en-US":"Js Tetris Level2"},
            "description":{"en-US":"Starting at 1, the higher the level, the harder the game."}}},
            "result":{"extensions":{"ext:time":104,"ext:apm":229,"ext:lines":5},"score":{"raw":9911,"min":0}},
            "context":{"contextActivities":{"grouping":{"id":"act:scorm.com/JsTetris_TCAPI"}},
            "registration":"b7be7d9d-bfe2-4917-8ccd-41a0d18dd953"},
            "actor":{"name":"tom creighton","mbox":"mailto:tom@example.com"}})

        path = '%s?%s' % (reverse(views.statements), urllib.urlencode({"statementId":stmt_id}))
        put_stmt = self.client.put(path, stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="0.90")
        self.assertEqual(put_stmt.status_code, 400)


    # Use this test to make sure stmts are being returned correctly with all data - doesn't check timestamp and stored fields
    def test_all_fields_activity_as_object(self):
        self.bunchostmts()
        nested_st_id = str(uuid.uuid1())
        nest_param = {"statementId":nested_st_id}
        nest_path = "%s?%s" % (reverse(views.statements), urllib.urlencode(nest_param))
        nested_stmt = json.dumps({"actor":{"objectType":"Agent","mbox": "mailto:tincan@adlnet.gov"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/assess","display": {"en-US":"assessed"}},
            "object":{"id":"http://example.adlnet.gov/tincan/example/simplestatement"}})
        put_sub_stmt = self.client.put(nest_path, nested_stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(put_sub_stmt.status_code, 204)        

        stmt_id = str(uuid.uuid1())
        context_id= str(uuid.uuid1())
        param = {"statementId":stmt_id} 
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt = json.dumps({"actor":{"objectType":"Agent","name": "Lou Wolford","account":{"homePage":"http://example.com", "name":"uniqueName"}},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/created","display": {"en-US":"created", "en-GB":"made"}},
            "object": {"objectType": "Activity", "id":"http:adlnet.gov/my/Activity/URL",
            "definition": {"name": {"en-US":"actName", "en-GB": "anotherActName"},
            "description": {"en-US":"This is my activity description.", "en-GB": "This is another activity description."},
            "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction",
            "interactionType": "choice",
            "correctResponsesPattern": ["golf", "tetris"],
            "choices":[{"id": "golf", "description": {"en-US":"Golf Example", "en-GB": "GOLF"}},
            {"id": "tetris","description":{"en-US": "Tetris Example", "en-GB": "TETRIS"}},
            {"id":"facebook", "description":{"en-US":"Facebook App", "en-GB": "FACEBOOK"}},
            {"id":"scrabble", "description": {"en-US": "Scrabble Example", "en-GB": "SCRABBLE"}}],
            "extensions": {"ext:key1": "value1", "ext:key2": "value2","ext:key3": "value3"}}}, 
            "result": {"score":{"scaled":.85, "raw": 85, "min":0, "max":100}, "completion": True, "success": True, "response": "Well done",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:resultKey1": "resultValue1", "ext:resultKey2":"resultValue2"}},
            "context":{"registration": context_id, "contextActivities": {"other": {"id": "http://example.adlnet.gov/tincan/example/test"},
            "grouping":{"id":"http://groupingID"} },
            "revision": "Spelling error in choices.", "platform":"Platform is web browser.","language": "en-US",
            "statement":{"objectType":"StatementRef", "id":str(nested_st_id)},
            "extensions":{"ext:contextKey1": "contextVal1","ext:contextKey2": "contextVal2"}},
            "timestamp":self.firstTime})

        put_stmt = self.client.put(path, stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(put_stmt.status_code, 204)
        param = {"statementId":stmt_id}
        get_path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        get_response = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        
        the_returned = json.loads(get_response.content)
        self.assertEqual(the_returned['id'], stmt_id)
        self.assertEqual(the_returned['actor']['objectType'], 'Agent')
        self.assertEqual(the_returned['actor']['name'], 'Lou Wolford')
        self.assertEqual(the_returned['actor']['account']['name'], 'uniqueName')
        self.assertEqual(the_returned['actor']['account']['homePage'], 'http://example.com')

        self.assertEqual(the_returned['verb']['id'], 'http://adlnet.gov/expapi/verbs/created')
        self.assertEqual(the_returned['verb']['display']['en-GB'], 'made')
        self.assertEqual(the_returned['verb']['display']['en-US'], 'created')

        self.assertEqual(the_returned['result']['completion'], True)
        self.assertEqual(the_returned['result']['duration'], 'P3Y6M4DT12H30M5S')
        self.assertEqual(the_returned['result']['extensions']['ext:resultKey1'], 'resultValue1')
        self.assertEqual(the_returned['result']['extensions']['ext:resultKey2'], 'resultValue2')
        self.assertEqual(the_returned['result']['response'], 'Well done')
        self.assertEqual(the_returned['result']['score']['max'], 100)
        self.assertEqual(the_returned['result']['score']['min'], 0)
        self.assertEqual(the_returned['result']['score']['raw'], 85)
        self.assertEqual(the_returned['result']['score']['scaled'], 0.85)
        self.assertEqual(the_returned['result']['success'], True)

        self.assertEqual(the_returned['context']['contextActivities']['other']['id'], 'http://example.adlnet.gov/tincan/example/test')
        self.assertEqual(the_returned['context']['extensions']['ext:contextKey1'], 'contextVal1')
        self.assertEqual(the_returned['context']['extensions']['ext:contextKey2'], 'contextVal2')
        self.assertEqual(the_returned['context']['language'], 'en-US')
        self.assertEqual(the_returned['context']['platform'], 'Platform is web browser.')
        self.assertEqual(the_returned['context']['registration'], context_id)
        self.assertEqual(the_returned['context']['revision'], 'Spelling error in choices.')
        self.assertEqual(the_returned['context']['statement']['id'], str(nested_st_id))
        self.assertEqual(the_returned['context']['statement']['objectType'], 'StatementRef')

        if settings.HTTP_AUTH_ENABLED:
            self.assertEqual(the_returned['authority']['objectType'], 'Agent')
            self.assertEqual(the_returned['authority']['name'], 'tester1')
            self.assertEqual(the_returned['authority']['mbox'], 'mailto:test1@tester.com')

        self.assertEqual(the_returned['object']['id'], 'http:adlnet.gov/my/Activity/URL')
        self.assertEqual(the_returned['object']['objectType'], 'Activity')
        self.assertEqual(the_returned['object']['definition']['description']['en-US'], 'This is my activity description.')
        self.assertEqual(the_returned['object']['definition']['description']['en-GB'], 'This is another activity description.')
        self.assertEqual(the_returned['object']['definition']['interactionType'], 'choice')
        self.assertEqual(the_returned['object']['definition']['name']['en-US'], 'actName')
        self.assertEqual(the_returned['object']['definition']['name']['en-GB'], 'anotherActName')
        self.assertEqual(the_returned['object']['definition']['type'], 'http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction')
        self.assertEqual(the_returned['object']['definition']['extensions']['ext:key1'], 'value1')
        self.assertEqual(the_returned['object']['definition']['extensions']['ext:key2'], 'value2')
        self.assertEqual(the_returned['object']['definition']['extensions']['ext:key3'], 'value3')
        # arrays.. testing slightly differently
        choices_str = json.dumps(the_returned['object']['definition']['choices'])
        self.assertIn('description', choices_str)
        self.assertIn('id', choices_str)
        self.assertIn('GOLF', choices_str)
        self.assertIn('Golf Example', choices_str)
        self.assertIn('golf', choices_str)
        self.assertIn('TETRIS', choices_str)
        self.assertIn('Tetris Example', choices_str)
        self.assertIn('tetris', choices_str)
        self.assertIn('FACEBOOK', choices_str)
        self.assertIn('Facebook App', choices_str)
        self.assertIn('Facebook', choices_str)
        self.assertIn('SCRABBLE', choices_str)
        self.assertIn('Scrabble Example', choices_str)
        self.assertIn('scrabble', choices_str)

        crp_str = json.dumps(the_returned['object']['definition']['correctResponsesPattern'])
        self.assertIn('golf', crp_str)
        self.assertIn('tetris', crp_str)


    # Use this test to make sure stmts are being returned correctly with all data - doesn't check timestamp, stored fields
    def test_all_fields_agent_as_object(self):
        nested_st_id = str(uuid.uuid1())
        nest_param = {"statementId":nested_st_id}
        nest_path = "%s?%s" % (reverse(views.statements), urllib.urlencode(nest_param))
        nested_stmt = json.dumps({"actor":{"objectType":"Agent","mbox": "mailto:tincan@adlnet.gov"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/assess","display": {"en-US":"assessed"}},
            "object":{"id":"http://example.adlnet.gov/tincan/example/simplestatement"}})
        put_sub_stmt = self.client.put(nest_path, nested_stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(put_sub_stmt.status_code, 204)        


        stmt_id = str(uuid.uuid1())
        context_id= str(uuid.uuid1())
        param = {"statementId":stmt_id} 
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        msha = hashlib.sha1("mailto:tom@example.com").hexdigest()                
        stmt = json.dumps({"actor":{"objectType":"Agent","name": "Lou Wolford","account":{"homePage":"http://example.com", "name":"louUniqueName"}},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/helped","display": {"en-US":"helped", "en-GB":"assisted"}},
            "object": {"objectType":"Agent","name": "Tom Creighton","mbox_sha1sum":msha}, 
            "result": {"score":{"scaled":.85, "raw": 85, "min":0, "max":100}, "completion": True, "success": True, "response": "Well done",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:resultKey1": "resultValue1", "ext:resultKey2":"resultValue2"}},
            "context":{"registration": context_id, "contextActivities": {"other": {"id": "http://example.adlnet.gov/tincan/example/test"}},
            "revision": "Spelling error in choices.", "platform":"Platform is web browser.","language": "en-US",
            "statement":{"objectType":"StatementRef", "id":str(nested_st_id)},
            "extensions":{"ext:contextKey1": "contextVal1","ext:contextKey2": "contextVal2"}},
            "timestamp":self.firstTime})
        
        put_stmt = self.client.put(path, stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(put_stmt.status_code, 204)
        param = {"statementId":stmt_id}
        get_path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        get_response = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        
        the_returned = json.loads(get_response.content)
        self.assertEqual(the_returned['id'], stmt_id)
        self.assertEqual(the_returned['actor']['objectType'], 'Agent')
        self.assertEqual(the_returned['actor']['name'], 'Lou Wolford')
        self.assertEqual(the_returned['actor']['account']['name'], 'louUniqueName')
        self.assertEqual(the_returned['actor']['account']['homePage'], 'http://example.com')

        self.assertEqual(the_returned['verb']['id'], 'http://adlnet.gov/expapi/verbs/helped')
        self.assertEqual(the_returned['verb']['display']['en-GB'], 'assisted')
        self.assertEqual(the_returned['verb']['display']['en-US'], 'helped')

        self.assertEqual(the_returned['result']['completion'], True)
        self.assertEqual(the_returned['result']['duration'], 'P3Y6M4DT12H30M5S')
        self.assertEqual(the_returned['result']['extensions']['ext:resultKey1'], 'resultValue1')
        self.assertEqual(the_returned['result']['extensions']['ext:resultKey2'], 'resultValue2')
        self.assertEqual(the_returned['result']['response'], 'Well done')
        self.assertEqual(the_returned['result']['score']['max'], 100)
        self.assertEqual(the_returned['result']['score']['min'], 0)
        self.assertEqual(the_returned['result']['score']['raw'], 85)
        self.assertEqual(the_returned['result']['score']['scaled'], 0.85)
        self.assertEqual(the_returned['result']['success'], True)

        self.assertEqual(the_returned['context']['contextActivities']['other']['id'], 'http://example.adlnet.gov/tincan/example/test')
        self.assertEqual(the_returned['context']['extensions']['ext:contextKey1'], 'contextVal1')
        self.assertEqual(the_returned['context']['extensions']['ext:contextKey2'], 'contextVal2')
        self.assertEqual(the_returned['context']['language'], 'en-US')
        self.assertEqual(the_returned['context']['registration'], context_id)
        self.assertEqual(the_returned['context']['statement']['id'], str(nested_st_id))
        self.assertEqual(the_returned['context']['statement']['objectType'], 'StatementRef')

        if settings.HTTP_AUTH_ENABLED:
            self.assertEqual(the_returned['authority']['objectType'], 'Agent')
            self.assertEqual(the_returned['authority']['name'], 'tester1')
            self.assertEqual(the_returned['authority']['mbox'], 'mailto:test1@tester.com')


        self.assertEqual(the_returned['object']['objectType'], 'Agent')
        self.assertEqual(the_returned['object']['name'], 'Tom Creighton')
        self.assertEqual(the_returned['object']['mbox_sha1sum'], msha)


    # Use this test to make sure stmts are being returned correctly with all data - doesn't check timestamps or stored fields
    def test_all_fields_substatement_as_object(self):
        nested_st_id = str(uuid.uuid1())
        nest_param = {"statementId":nested_st_id}
        nest_path = "%s?%s" % (reverse(views.statements), urllib.urlencode(nest_param))
        nested_stmt = json.dumps({"actor":{"objectType":"Agent","mbox": "mailto:tincannest@adlnet.gov"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/assess","display": {"en-US":"assessed", "en-GB":"graded"}},
            "object":{"id":"http://example.adlnet.gov/tincan/example/simplestatement"}})
        put_sub_stmt = self.client.put(nest_path, nested_stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(put_sub_stmt.status_code, 204)        


        nested_sub_st_id = str(uuid.uuid1())
        nest_sub_param = {"statementId":nested_sub_st_id}
        nest_sub_path = "%s?%s" % (reverse(views.statements), urllib.urlencode(nest_sub_param))        
        nested_sub_stmt = json.dumps({"actor":{"objectType":"Agent","mbox": "mailto:tincannestsub@adlnet.gov"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/verb","display": {"en-US":"verb", "en-GB":"altVerb"}},
            "object":{"id":"http://example.adlnet.gov/tincan/example/simplenestedsubstatement"}})
        put_nest_sub_stmt = self.client.put(nest_sub_path, nested_sub_stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(put_nest_sub_stmt.status_code, 204)


        stmt_id = str(uuid.uuid1())
        context_id= str(uuid.uuid1())
        sub_context_id= str(uuid.uuid1())        
        param = {"statementId":stmt_id} 
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        msha = hashlib.sha1("mailto:tom@example.com").hexdigest()        
        
        stmt = json.dumps({"actor":{"objectType":"Agent","name": "Lou Wolford","account":{"homePage":"http://example.com", "name":"louUniqueName"}},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/said","display": {"en-US":"said", "en-GB":"talked"}},
            "object": {"objectType": "SubStatement", "actor":{"objectType":"Agent","name":"Tom Creighton","mbox": "mailto:tom@adlnet.gov"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/assess","display": {"en-US":"assessed", "en-GB": "Graded"}},
            "object":{"id":"http://example.adlnet.gov/tincan/example/simplestatement",
            'definition': {'name': {'en-US':'SubStatement name'},
            'description': {'en-US':'SubStatement description'},
            'type': 'http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction','interactionType': 'matching',
            'correctResponsesPattern': ['lou.3,tom.2,andy.1'],'source':[{'id': 'lou',
            'description': {'en-US':'Lou', 'it': 'Luigi'}},{'id': 'tom','description':{'en-US': 'Tom', 'it':'Tim'}},
            {'id':'andy', 'description':{'en-US':'Andy'}}],'target':[{'id':'1',
            'description':{'en-US': 'ADL LRS'}},{'id':'2','description':{'en-US': 'lrs'}},
            {'id':'3', 'description':{'en-US': 'the adl lrs', 'en-CH': 'the lrs'}}]}},
            "result": {"score":{"scaled":.50, "raw": 50, "min":1, "max":51}, "completion": True,
            "success": True, "response": "Poorly done",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:resultKey11": "resultValue11", "ext:resultKey22":"resultValue22"}},
            "context":{"registration": sub_context_id,
            "contextActivities": {"other": {"id": "http://example.adlnet.gov/tincan/example/test/nest"}},
            "revision": "Spelling error in target.", "platform":"Ipad.","language": "en-US",
            "statement":{"objectType":"StatementRef", "id":str(nested_sub_st_id)},
            "extensions":{"ext:contextKey11": "contextVal11","ext:contextKey22": "contextVal22"}}}, 
            "result": {"score":{"scaled":.85, "raw": 85, "min":0, "max":100}, "completion": True, "success": True, "response": "Well done",
            "duration": "P3Y6M4DT12H30M5S", "extensions":{"ext:resultKey1": "resultValue1", "ext:resultKey2":"resultValue2"}},
            "context":{"registration": context_id, "contextActivities": {"other": {"id": "http://example.adlnet.gov/tincan/example/test"}},
            "revision": "Spelling error in choices.", "platform":"Platform is web browser.","language": "en-US",
            "statement":{"objectType":"StatementRef", "id":str(nested_st_id)},
            "extensions":{"ext:contextKey1": "contextVal1","ext:contextKey2": "contextVal2"}},
            "timestamp":self.firstTime})
        put_stmt = self.client.put(path, stmt, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(put_stmt.status_code, 204)
        param = {"statementId":stmt_id}
        get_path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        get_response = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        
        the_returned = json.loads(get_response.content)
        self.assertEqual(the_returned['id'], stmt_id)
        self.assertEqual(the_returned['actor']['objectType'], 'Agent')
        self.assertEqual(the_returned['actor']['name'], 'Lou Wolford')
        self.assertEqual(the_returned['actor']['account']['name'], 'louUniqueName')
        self.assertEqual(the_returned['actor']['account']['homePage'], 'http://example.com')

        self.assertEqual(the_returned['verb']['id'], 'http://adlnet.gov/expapi/verbs/said')
        self.assertEqual(the_returned['verb']['display']['en-GB'], 'talked')
        self.assertEqual(the_returned['verb']['display']['en-US'], 'said')
        
        self.assertEqual(the_returned['object']['actor']['objectType'], 'Agent')
        self.assertEqual(the_returned['object']['actor']['name'], 'Tom Creighton')
        self.assertEqual(the_returned['object']['actor']['mbox'], 'mailto:tom@adlnet.gov')
        
        self.assertEqual(the_returned['object']['context']['registration'], sub_context_id)
        self.assertEqual(the_returned['object']['context']['language'], 'en-US')
        self.assertEqual(the_returned['object']['context']['platform'], 'Ipad.')
        self.assertEqual(the_returned['object']['context']['revision'], 'Spelling error in target.')
        self.assertEqual(the_returned['object']['context']['statement']['id'], str(nested_sub_st_id))
        self.assertEqual(the_returned['object']['context']['statement']['objectType'], 'StatementRef')
        self.assertEqual(the_returned['object']['context']['contextActivities']['other']['id'], 'http://example.adlnet.gov/tincan/example/test/nest')
        self.assertEqual(the_returned['object']['context']['extensions']['ext:contextKey11'], 'contextVal11')
        self.assertEqual(the_returned['object']['context']['extensions']['ext:contextKey22'], 'contextVal22')
        self.assertEqual(the_returned['object']['object']['id'], 'http://example.adlnet.gov/tincan/example/simplestatement')
        self.assertEqual(the_returned['object']['object']['definition']['type'], 'http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction')
        self.assertEqual(the_returned['object']['object']['definition']['description']['en-US'], 'SubStatement description')
        self.assertEqual(the_returned['object']['object']['definition']['interactionType'], 'matching')
        self.assertEqual(the_returned['object']['object']['definition']['name']['en-US'], 'SubStatement name')
        # arrays.. testing slightly differently
        source_str = json.dumps(the_returned['object']['object']['definition']['source'])
        self.assertIn('description', source_str)
        self.assertIn('id', source_str)
        self.assertIn('Lou', source_str)
        self.assertIn('Luigi', source_str)
        self.assertIn('lou', source_str)
        self.assertIn('Tom', source_str)
        self.assertIn('Tim', source_str)
        self.assertIn('tom', source_str)
        self.assertIn('Andy', source_str)
        self.assertIn('andy', source_str)

        target_str = json.dumps(the_returned['object']['object']['definition']['target'])
        self.assertIn('description', target_str)
        self.assertIn('id', target_str)
        self.assertIn('ADL LRS', target_str)
        self.assertIn('1', target_str)
        self.assertIn('lrs', target_str)
        self.assertIn('2', target_str)
        self.assertIn('the lrs', target_str)
        self.assertIn('the adl lrs', target_str)
        self.assertIn('3', target_str)
        
        self.assertEqual(the_returned['object']['objectType'], 'SubStatement')

        self.assertEqual(the_returned['object']['result']['completion'], True)
        self.assertEqual(the_returned['object']['result']['duration'], 'P3Y6M4DT12H30M5S')
        self.assertEqual(the_returned['object']['result']['extensions']['ext:resultKey11'], 'resultValue11')
        self.assertEqual(the_returned['object']['result']['extensions']['ext:resultKey22'], 'resultValue22')
        self.assertEqual(the_returned['object']['result']['response'], 'Poorly done')
        self.assertEqual(the_returned['object']['result']['score']['max'], 51)
        self.assertEqual(the_returned['object']['result']['score']['min'], 1)
        self.assertEqual(the_returned['object']['result']['score']['raw'], 50)
        self.assertEqual(the_returned['object']['result']['score']['scaled'], 0.5)
        self.assertEqual(the_returned['object']['result']['success'], True)
        
        self.assertEqual(the_returned['object']['verb']['id'], 'http://adlnet.gov/expapi/verbs/assess')
        self.assertEqual(the_returned['object']['verb']['display']['en-GB'], 'Graded')
        self.assertEqual(the_returned['object']['verb']['display']['en-US'], 'assessed')

        self.assertEqual(the_returned['result']['completion'], True)
        self.assertEqual(the_returned['result']['duration'], 'P3Y6M4DT12H30M5S')
        self.assertEqual(the_returned['result']['extensions']['ext:resultKey1'], 'resultValue1')
        self.assertEqual(the_returned['result']['extensions']['ext:resultKey2'], 'resultValue2')
        self.assertEqual(the_returned['result']['response'], 'Well done')
        self.assertEqual(the_returned['result']['score']['max'], 100)
        self.assertEqual(the_returned['result']['score']['min'], 0)
        self.assertEqual(the_returned['result']['score']['raw'], 85)
        self.assertEqual(the_returned['result']['score']['scaled'], 0.85)
        self.assertEqual(the_returned['result']['success'], True)

        self.assertEqual(the_returned['context']['contextActivities']['other']['id'], 'http://example.adlnet.gov/tincan/example/test')
        self.assertEqual(the_returned['context']['extensions']['ext:contextKey1'], 'contextVal1')
        self.assertEqual(the_returned['context']['extensions']['ext:contextKey2'], 'contextVal2')
        self.assertEqual(the_returned['context']['language'], 'en-US')
        self.assertEqual(the_returned['context']['platform'], 'Platform is web browser.')
        self.assertEqual(the_returned['context']['registration'], context_id)
        self.assertEqual(the_returned['context']['revision'], 'Spelling error in choices.')
        self.assertEqual(the_returned['context']['statement']['id'], str(nested_st_id))
        self.assertEqual(the_returned['context']['statement']['objectType'], 'StatementRef')

        if settings.HTTP_AUTH_ENABLED:
            self.assertEqual(the_returned['authority']['objectType'], 'Agent')
            self.assertEqual(the_returned['authority']['name'], 'tester1')
            self.assertEqual(the_returned['authority']['mbox'], 'mailto:test1@tester.com')

    # Third stmt in list is missing actor - should throw error and perform cascading delete on first three statements
    def test_post_list_rollback(self):
        self.bunchostmts()
        cguid1 = str(uuid.uuid1())
        # print cguid1
        stmts = json.dumps([{"verb":{"id": "http://adlnet.gov/expapi/verbs/wrong-failed","display": {"en-US":"wrong-failed"}},"object": {"id":"act:test_wrong_list_post2"},
            "actor":{"objectType":"Agent", "mbox":"mailto:wrong-t@t.com"},"result": {"score":{"scaled":.99}, "completion": True, "success": True, "response": "wrong",
            "extensions":{"ext:resultwrongkey1": "value1", "ext:resultwrongkey2":"value2"}}},
            {"verb":{"id": "http://adlnet.gov/expapi/verbs/wrong-kicked","display": {"en-US":"wrong-kicked"}},
            "object": {"objectType": "Activity", "id":"act:test_wrong_list_post",
            "definition": {"name": {"en-US":"wrongactName", "en-GB": "anotherActName"},
            "description": {"en-US":"This is my activity description.", "en-GB": "This is another activity description."},
            "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction",
            "interactionType": "choice",
            "correctResponsesPattern": ["wronggolf", "wrongtetris"],
            "choices":[{"id": "wronggolf", "description": {"en-US":"Golf Example", "en-GB": "GOLF"}},
            {"id": "wrongtetris","description":{"en-US": "Tetris Example", "en-GB": "TETRIS"}},
            {"id":"wrongfacebook", "description":{"en-US":"Facebook App", "en-GB": "FACEBOOK"}},
            {"id":"wrongscrabble", "description": {"en-US": "Scrabble Example", "en-GB": "SCRABBLE"}}],
            "extensions": {"ext:wrongkey1": "wrongvalue1", "ext:wrongkey2": "wrongvalue2","ext:wrongkey3": "wrongvalue3"}}},
            "actor":{"objectType":"Agent", "mbox":"mailto:wrong-t@t.com"}},
            {"verb":{"id": "http://adlnet.gov/expapi/verbs/wrong-passed","display": {"en-US":"wrong-passed"}},"object": {"id":"act:test_wrong_list_post1"},
            "actor":{"objectType":"Agent", "mbox":"mailto:wrong-t@t.com"},"context":{"registration": cguid1, "contextActivities": {"other": {"id": "act:wrongActivityID2"}},
            "revision": "wrong", "platform":"wrong","language": "en-US", "extensions":{"ext:wrongkey1": "wrongval1",
            "ext:wrongkey2": "wrongval2"}}},            
            {"verb":{"id": "http://adlnet.gov/expapi/verbs/wrong-kicked","display": {"en-US":"wrong-kicked"}},"object": {"id":"act:test_wrong_list_post2"}},            
            {"verb":{"id": "http://adlnet.gov/expapi/verbs/wrong-kicked","display": {"en-US":"wrong-kicked"}},"object": {"id":"act:test_wrong_list_post4"}, "actor":{"objectType":"Agent", "mbox":"wrong-t@t.com"}}])
        
        response = self.client.post(reverse(views.statements), stmts,  content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 400)
        self.assertIn("No actor provided, must provide 'actor' field", response.content)
        
        results = models.result.objects.filter(response='wrong')
        scores = models.score.objects.filter(scaled=.99)
        exts = models.extensions.objects.filter(key__contains='wrong')
        
        contexts = models.context.objects.filter(registration=cguid1)
        
        verbs = models.Verb.objects.filter(verb_id__contains='wrong')
        
        activities = models.activity.objects.filter(activity_id__contains='test_wrong_list_post')
        activity_definitions = models.activity_definition.objects.all()
        crp_answers = models.correctresponsespattern_answer.objects.filter(answer__contains='wrong')
        
        statements = models.statement.objects.all()

        # 11 statements from setup
        self.assertEqual(len(statements), 11)

        self.assertEqual(len(results), 0)
        self.assertEqual(len(scores), 0)
        self.assertEqual(len(exts), 0)
        self.assertEqual(len(contexts), 0)
        self.assertEqual(len(verbs), 0)
        self.assertEqual(len(activities), 0)
        # Should only be 3 from setup (4 there but 2 get merged together to make 1, equaling 3)
        self.assertEqual(len(activity_definitions), 3)
        self.assertEqual(len(crp_answers), 0)

    def test_post_list_rollback_part_2(self):
        self.bunchostmts()
        stmts = json.dumps([{"object": {"objectType":"Agent","name":"john","mbox":"mailto:john@john.com"},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/wrong","display": {"wrong-en-US":"wrong"}},
            "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"}},
            {"verb":{"id": "http://adlnet.gov/expapi/verbs/created"},
            "object": {"objectType": "Activity", "id":"act:foogie",
            "definition": {"name": {"en-US":"testname2", "en-GB": "altname"},
            "description": {"en-US":"testdesc2", "en-GB": "altdesc"}, "type": "http://www.adlnet.gov/experienceapi/activity-types/cmi.interaction",
            "interactionType": "fill-in","correctResponsesPattern": ["answer"]}},
            "actor":{"objectType":"Agent", "mbox":"mailto:wrong-t@t.com"}},
            {"verb":{"id": "http://adlnet.gov/expapi/verbs/wrong-kicked"},"object": {"id":"act:test_wrong_list_post2"}}])

        response = self.client.post(reverse(views.statements), stmts,  content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 400)
        self.assertIn("No actor provided, must provide 'actor' field", response.content)

        created_verbs = models.Verb.objects.filter(verb_id__contains='http://adlnet.gov/expapi/verbs/created')
        wrong_verbs = models.Verb.objects.filter(verb_id__contains='http://adlnet.gov/expapi/verbs/wrong')
        
        activities = models.activity.objects.filter(activity_id='act:foogie')
        
        statements = models.statement.objects.all()

        wrong_agent = models.agent.objects.filter(mbox='mailto:wrong-t@t.com')
        john_agent = models.agent.objects.filter(mbox='mailto:john@john.com')
        s_agent = models.agent.objects.filter(mbox='mailto:s@s.com')
        auth_agent = models.agent.objects.filter(mbox='mailto:test1@tester.com')
        verb_display = models.LanguageMap.objects.filter(key__contains='wrong')

        self.assertEqual(len(created_verbs), 1)
        self.assertEqual(len(wrong_verbs), 0)
        self.assertEqual(len(verb_display), 0)

        self.assertEqual(len(activities), 1)
        
        self.assertEqual(len(statements), 11)

        self.assertEqual(len(wrong_agent), 0)
        self.assertEqual(len(john_agent), 1)
        self.assertEqual(len(s_agent), 1)

        if settings.HTTP_AUTH_ENABLED:
            self.assertEqual(len(auth_agent), 1)

    def test_post_list_rollback_with_void(self):
        self.bunchostmts()
        stmts = json.dumps([{"actor":{"objectType":"Agent","mbox":"mailto:only-s@s.com"},
            "object": {"objectType":"StatementRef","id":str(self.exist_stmt_id)},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/voided","display": {"en-US":"voided"}}},
            {"verb":{"id": "http://adlnet.gov/expapi/verbs/wrong-kicked"},"object": {"id":"act:test_wrong_list_post2"}}])

        response = self.client.post(reverse(views.statements), stmts,  content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 400)
        self.assertIn("No actor provided, must provide 'actor' field", response.content)
        voided_st = models.statement.objects.get(statement_id=str(self.exist_stmt_id))
        voided_verb = models.Verb.objects.filter(verb_id__contains='voided')
        only_actor = models.agent.objects.filter(mbox="mailto:only-s@s.com")
        statements = models.statement.objects.all()

        self.assertEqual(len(statements), 11)
        self.assertEqual(voided_st.voided, False)
        self.assertEqual(len(voided_verb), 1)
        self.assertEqual(len(only_actor), 0)

    def test_post_list_rollback_with_subs(self):
        self.bunchostmts()
        sub_context_id = str(uuid.uuid1())
        stmts = json.dumps([{"actor":{"objectType":"Agent","mbox":"mailto:wrong-s@s.com"},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/wrong","display": {"wrong-en-US":"wrong"}},
            "object": {"objectType":"Agent","name":"john","mbox":"mailto:john@john.com"}},
            {"actor":{"objectType":"Agent","mbox":"mailto:s@s.com"},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/wrong-next","display": {"wrong-en-US":"wrong-next"}},
            "object":{"objectType":"SubStatement",
            "actor":{"objectType":"Agent","mbox":"mailto:wrong-ss@ss.com"},"verb": {"id":"http://adlnet.gov/expapi/verbs/wrong-sub"},
            "object": {"objectType":"activity", "id":"act:wrong-testex.com"}, "result":{"completion": True, "success": True,
            "response": "sub-wrong-kicked"}, "context":{"registration": sub_context_id,
            "contextActivities": {"other": {"id": "act:sub-wrong-ActivityID"}},"revision": "foo", "platform":"bar",
            "language": "en-US", "extensions":{"ext:wrong-k1": "v1", "ext:wrong-k2": "v2"}}}},
            {"verb":{"id": "http://adlnet.gov/expapi/verbs/wrong-kicked"},"object": {"id":"act:test_wrong_list_post2"}}])
        response = self.client.post(reverse(views.statements), stmts,  content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(response.status_code, 400)
        self.assertIn("No actor provided, must provide 'actor' field", response.content)

        s_agent = models.agent.objects.filter(mbox="mailto:wrong-s@s.com")
        ss_agent = models.agent.objects.filter(mbox="mailto:wrong-ss@ss.com")
        john_agent  = models.agent.objects.filter(mbox="mailto:john@john.com")
        subs = models.SubStatement.objects.all()
        wrong_verb = models.Verb.objects.filter(verb_id__contains="wrong")
        activities = models.activity.objects.filter(activity_id__contains="wrong")
        results = models.result.objects.filter(response__contains="wrong")
        contexts = models.context.objects.filter(registration=sub_context_id)
        con_exts = models.extensions.objects.filter(key__contains="wrong")
        con_acts = models.ContextActivity.objects.filter(context_activity__contains="wrong")
        statements = models.statement.objects.all()

        self.assertEqual(len(statements), 11)
        self.assertEqual(len(s_agent), 0)
        self.assertEqual(len(ss_agent), 0)
        self.assertEqual(len(john_agent), 1)
        # Only 1 sub from setup
        self.assertEqual(len(subs), 1)
        self.assertEqual(len(wrong_verb), 0)
        self.assertEqual(len(activities), 0)
        self.assertEqual(len(results), 0)
        self.assertEqual(len(contexts), 0)
        self.assertEqual(len(con_exts), 0)
        self.assertEqual(len(con_acts), 0)

    def test_object_filter(self):
        if settings.HTTP_AUTH_ENABLED:
            exist_stmt = Statement.Statement(json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
                "display": {"en-US":"created"}}, "object": {"id":"act:activity"},
                "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"},
                "authority":{"objectType":"Agent","name":"tester1","mbox":"mailto:test1@tester.com"}}))
        else:
            exist_stmt = Statement.Statement(json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
                "display": {"en-US":"created"}}, "object": {"id":"act:activity"},
                "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"}}))            
        
        exist_stmt_id = exist_stmt.model_object.statement_id

        stmt_agent_jon = json.dumps({"object":{"objectType":"Agent","name":"jon","mbox":"mailto:jon@jon.com"},
                                     "verb":{"id": "http://adlnet.gov/expapi/verbs/tutored","display": {"en-US":"tutored"}},
                                     "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"}})

        stmt_act_1 = json.dumps({"actor": {"objectType":"Agent","name":"max","mbox":"mailto:max@max.com"}, 
                                 "object":{"id": "test://adlnet.gov/activities/test/1"},
                                 "verb":{"id": "http://adlnet.gov/expapi/verbs/completed"}})

        stmt_act_2 = json.dumps({"actor": {"objectType":"Agent","name":"max","mbox":"mailto:max@max.com"}, 
                                 "object":{"id": "test://adlnet.gov/activities/test/2"},
                                 "verb":{"id": "http://adlnet.gov/expapi/verbs/completed"}})

        stmt_sub_stmt = json.dumps({"actor":{"objectType":"Agent","mbox":"mailto:sub@sub.com"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/missed"},"object":{"objectType":"SubStatement",
            "actor":{"objectType":"Agent","mbox":"mailto:ss@ss.com"},"verb": {"id":"verb:verb/url/nested"},
            "object": {"objectType":"activity", "id":"act:testex.com"}, "result":{"completion": True, "success": True,
            "response": "kicked"}, "context":{"registration": str(uuid.uuid1()),
            "contextActivities": {"other": {"id": "act:NewActivityID"}},"revision": "foo", "platform":"bar",
            "language": "en-US", "extensions":{"ext:k1": "v1", "ext:k2": "v2"}}}})

        stmt_stmt_ref = json.dumps({"actor":{"objectType":"Agent","mbox":"mailto:ref@ref.com"},
            "verb":{"id": "http://adlnet.gov/expapi/verbs/missed"},"object":{"objectType":"StatementRef",
            "id":str(exist_stmt_id)}})

        path = reverse(views.statements)
        stmt_payload = [stmt_agent_jon, stmt_act_1, stmt_act_2, stmt_sub_stmt, stmt_stmt_ref]
        postresponse1 = self.client.post(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(postresponse1.status_code, 200)

        getallresp = self.client.get(path, Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(getallresp.status_code, 200)

        allstmts = json.loads(getallresp.content)
        self.assertEqual(len(allstmts['statements']), 6)

        param = {"object":{"objectType": "Agent", "mbox":"mailto:jon@jon.com"}}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        agentresp = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        
        agentstmts = json.loads(agentresp.content)
        self.assertEqual(len(agentstmts['statements']), 1)

        param = {"object":{"objectType": "Activity", "id":"test://adlnet.gov/activities/test/1"}}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        acttyperesp = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)

        acttypestmts = json.loads(acttyperesp.content)
        self.assertEqual(len(acttypestmts['statements']), 1)

        param = {"object":{"id":"test://adlnet.gov/activities/test/2"}}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))        
        actresp = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)
        actstmts = json.loads(actresp.content)
        self.assertEqual(len(actstmts['statements']), 1)

        param = {"object": "test://adlnet.gov/activities/test/2"}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param)) 
        actnoobjresp = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)            
        
        self.assertEqual(actnoobjresp.status_code, 400)
        self.assertEqual(actnoobjresp.content, "Cannot evaluate data into dictionary to parse")

    def test_no_activity_filter(self):
        self.bunchostmts()
        # Test actor
        actorGetResponse = self.client.post(reverse(views.statements), 
            {"object":{"objectType": "Activity", "id":"http://notarealactivity.com"}},
             content_type="application/x-www-form-urlencoded", X_Experience_API_Version="1.0", Authorization=self.auth)
        self.assertEqual(actorGetResponse.status_code, 200)
        rsp = json.loads(actorGetResponse.content)
        stmts = rsp['statements']
        self.assertEqual(len(stmts), 0)

    def test_since_filter_tz(self):
        stmt1_guid = str(uuid.uuid1())
        stmt1 = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
                "display": {"en-US":"created"}}, "object": {"id":"act:activity"},
                "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"}, "timestamp":"2013-02-02T12:00:00-05:00"})

        param = {"statementId":stmt1_guid}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = stmt1
        resp = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(resp.status_code, 204)
        time = "2013-02-02T12:00:32-05:00"
        stmt = models.statement.objects.filter(statement_id=stmt1_guid).update(stored=time)

        stmt2_guid = str(uuid.uuid1())
        stmt2 = json.dumps({"verb":{"id": "http://adlnet.gov/expapi/verbs/created",
                "display": {"en-US":"created"}}, "object": {"id":"act:activity2"},
                "actor":{"objectType":"Agent","mbox":"mailto:s@s.com"}, "timestamp":"2013-02-02T20:00:00+05:00"})

        param = {"statementId":stmt2_guid}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))
        stmt_payload = stmt2
        resp = self.client.put(path, stmt_payload, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(resp.status_code, 204)
        time = "2013-02-02T10:00:32-05:00"
        stmt = models.statement.objects.filter(statement_id=stmt2_guid).update(stored=time)

        param = {"since": "2013-02-02T14:00Z"}
        path = "%s?%s" % (reverse(views.statements), urllib.urlencode(param))      
        sinceGetResponse = self.client.get(path, X_Experience_API_Version="1.0", Authorization=self.auth)

        self.assertEqual(sinceGetResponse.status_code, 200)
        rsp = sinceGetResponse.content
        self.assertIn(stmt1_guid, rsp)
        self.assertIn(stmt2_guid, rsp)

        param2 = {"since": "2013-02-02T16:00Z"}
        path2 = "%s?%s" % (reverse(views.statements), urllib.urlencode(param2))      
        sinceGetResponse2 = self.client.get(path2, X_Experience_API_Version="1.0", Authorization=self.auth)

        self.assertEqual(sinceGetResponse2.status_code, 200)
        rsp2 = sinceGetResponse2.content
        self.assertIn(stmt1_guid, rsp2)
        self.assertNotIn(stmt2_guid, rsp2)
        
    def test_stmts_w_same_regid(self):
        stmt1_guid = str(uuid.uuid1())
        stmt2_guid = str(uuid.uuid1())
        reg_guid = str(uuid.uuid1())
        stmt1 = json.dumps({"actor":{"mbox":"mailto:tom@example.com"},
                            "verb":{"id":"http:adlnet.gov/expapi/verbs/tested",
                                    "display":{"en-US":"tested"}},
                            "object":{"id":"test:same.regid"},
                            "context":{"registration":reg_guid}
                            })
        stmt2 = json.dumps({"actor":{"mbox":"mailto:tom@example.com"},
                            "verb":{"id":"http:adlnet.gov/expapi/verbs/tested",
                                    "display":{"en-US":"tested"}},
                            "object":{"id":"test:same.regid.again"},
                            "context":{"registration":reg_guid}
                            })

        param1 = {"statementId":stmt1_guid}
        path1 = "%s?%s" % (reverse(views.statements), urllib.urlencode(param1))
        stmt_payload1 = stmt1
        resp1 = self.client.put(path1, stmt_payload1, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(resp1.status_code, 204)

        param2 = {"statementId":stmt2_guid}
        path2 = "%s?%s" % (reverse(views.statements), urllib.urlencode(param2))
        stmt_payload2 = stmt2
        resp2 = self.client.put(path2, stmt_payload2, content_type="application/json", Authorization=self.auth, X_Experience_API_Version="1.0")
        self.assertEqual(resp2.status_code, 204)
        