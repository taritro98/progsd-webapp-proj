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

 ## Test whether status 200 OK is returned for login API
    def test_status200_login(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for login API
    def test_application_json_login(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        self.assertEqual(response.content_type, "application/json")

     ## Test whether status 200 OK is returned for Sign Up API
    def test_status200_signup(self):
        tester = app.test_client(self)
        response = tester.get("/sign-up")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for Sign up API
    def test_application_json_signup(self):
        tester = app.test_client(self)
        response = tester.get("/sign-up")
        self.assertEqual(response.content_type, "application/json")

     ## Test whether status 200 OK is returned for vehicle list API
    def test_status200_vehiclelist(self):
        tester = app.test_client(self)
        response = tester.get("/vehicle-list")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for vehicle list API
    def test_application_json_vehiclelist(self):
        tester = app.test_client(self)
        response = tester.get("/vehicle-list")
        self.assertEqual(response.content_type, "application/json")

     ## Test whether status 200 OK is returned for report vehicle API
    def test_status200_reportvehicle(self):
        tester = app.test_client(self)
        response = tester.get("/report-vehicle")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for report vehicle API
    def test_application_json_reportvehicle(self):
        tester = app.test_client(self)
        response = tester.get("/report-vehicle")
        self.assertEqual(response.content_type, "application/json")
    
     ## Test whether status 200 OK is returned for vehicle type report API
    def test_status200_vtr(self):
        tester = app.test_client(self)
        response = tester.get("/vtr/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for vehicle type report API
    def test_application_json_vtr(self):
        tester = app.test_client(self)
        response = tester.get("/vtr/")
        self.assertEqual(response.content_type, "application/json")
    
     ## Test whether status 200 OK is returned for vehicle operational cost report API
    def test_status200_vocr(self):
        tester = app.test_client(self)
        response = tester.get("/vocr/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for vehicle operational cost report  API
    def test_application_json_vocr(self):
        tester = app.test_client(self)
        response = tester.get("/vocr/")
        self.assertEqual(response.content_type, "application/json")
    
     ## Test whether status 200 OK is returned for active station report API
    def test_status200_asr(self):
        tester = app.test_client(self)
        response = tester.get("/asr")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for active station report API
    def test_application_json_asr(self):
        tester = app.test_client(self)
        response = tester.get("/asr")
        self.assertEqual(response.content_type, "application/json")
    
     ## Test whether status 200 OK is returned for station revenue report API
    def test_status200_srr(self):
        tester = app.test_client(self)
        response = tester.get("/srr")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for station revenue report  API
    def test_application_json_srr(self):
        tester = app.test_client(self)
        response = tester.get("/srr")
        self.assertEqual(response.content_type, "application/json")
    
     ## Test whether status 200 OK is returned for fetch operator list API
    def test_status200_fol(self):
        tester = app.test_client(self)
        response = tester.get("/fol/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for fetch operator list API
    def test_application_json_fol(self):
        tester = app.test_client(self)
        response = tester.get("/fol/")
        self.assertEqual(response.content_type, "application/json")
    
     ## Test whether status 200 OK is returned for fetch perf data API
    def test_status200_fpd(self):
        tester = app.test_client(self)
        response = tester.get("/fpd/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for fetch perf data  API
    def test_application_json_fpd(self):
        tester = app.test_client(self)
        response = tester.get("/fpd/")
        self.assertEqual(response.content_type, "application/json")
    
     ## Test whether status 200 OK is returned for move vehicle API
    def test_status200_mv(self):
        tester = app.test_client(self)
        response = tester.get("/mv")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for move vehicle API
    def test_application_json_mv(self):
        tester = app.test_client(self)
        response = tester.get("/mv")
        self.assertEqual(response.content_type, "application/json")

     ## Test whether status 200 OK is returned for manage operator API
    def test_status200_mo(self):
        tester = app.test_client(self)
        response = tester.get("/mo")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for manage operator API
    def test_application_json_mo(self):
        tester = app.test_client(self)
        response = tester.get("/mo")
        self.assertEqual(response.content_type, "application/json")

     ## Test whether status 200 OK is returned for insert operator API
    def test_status200_io(self):
        tester = app.test_client(self)
        response = tester.get("/io")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for insert operator API
    def test_application_json_io(self):
        tester = app.test_client(self)
        response = tester.get("/io")
        self.assertEqual(response.content_type, "application/json")
    
     ## Test whether status 200 OK is returned for renting ride API
    def test_status200_rentingride(self):
        tester = app.test_client(self)
        response = tester.get("/renting-ride")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for renting ride  API
    def test_application_json_rentingride(self):
        tester = app.test_client(self)
        response = tester.get("/renting-ride")
        self.assertEqual(response.content_type, "application/json")

     ## Test whether status 200 OK is returned for load data API
    def test_status200_loaddata(self):
        tester = app.test_client(self)
        response = tester.get("/load_data")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for load data API
    def test_application_json_loaddata(self):
        tester = app.test_client(self)
        response = tester.get("/load_data")
        self.assertEqual(response.content_type, "application/json")
    
     ## Test whether status 200 OK is returned for track ride API
    def test_status200_trackride(self):
        tester = app.test_client(self)
        response = tester.get("/track-ride")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for track ride  API
    def test_application_json_trackride(self):
        tester = app.test_client(self)
        response = tester.get("/track-ride")
        self.assertEqual(response.content_type, "application/json")

     ## Test whether status 200 OK is returned for total_time_per_customer API
    def test_status200_totaltimepercust(self):
        tester = app.test_client(self)
        response = tester.get("/total-time-per-cust")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for total_time_per_customer  API
    def test_application_json_totaltimepercust(self):
        tester = app.test_client(self)
        response = tester.get("/total-time-per-cust")
        self.assertEqual(response.content_type, "application/json")

    ## Test whether content type is application/json for cumulative time sum API
    def test_status200_cumultimesum(self):
        tester = app.test_client(self)
        response = tester.get("/cumul_timesum")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    ## Test whether content type is application/json for cumulative time sum API
    def test_application_json_cumultimesum(self):
        tester = app.test_client(self)
        response = tester.get("/cumul_timesum")
        self.assertEqual(response.content_type, "application/json")

if __name__=="__main__":
    unittest.main()