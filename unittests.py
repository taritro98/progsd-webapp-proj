import unittest
from tapp import app

## Unit Test Class
class FlaskTest(unittest.TestCase):

    ## Test whether status 200 OK is returned for active tasks API
    def test_status200_activetaskslist(self):
        tester = app.test_client(self)
        response = tester.get("/active-tasks-list")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for active tasks API
    def test_application_json_activetaskslist(self):
        tester = app.test_client(self)
        response = tester.get("/active-tasks-list")
        self.assertEqual(response.content_type, "application/json")

if __name__=="__main__":
    unittest.main()