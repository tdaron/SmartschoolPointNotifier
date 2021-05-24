import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import unquote
from loaders import TextLoader, SpinningLoader

class SmartschoolApi:
    def __init__(self, base_url):
        self.base_url = base_url
    def authenticate(self, username, password):
        loader = SpinningLoader(text="Authentification", complete_text="Authenticated", speed=0.15, animation="bounce")
        loader.start()
        self.s = requests.session()
        #print("Getting login page...")
        body = self.s.get(self.base_url+"/login")
        soup = BeautifulSoup(body.text, 'html.parser')
        #print("Extracting tokens...")
        formToken = soup.find("input", {"id":"login_form__token"}).attrs["value"]
        generationTime = soup.find("input", {"id":"login_form__generationTime"}).attrs["value"]


        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'content-type': 'application/x-www-form-urlencoded',
        }

        data = {
        'login_form[_username]': username,
        'login_form[_password]': password,
        'login_form[_generationTime]': generationTime,
        'login_form[_token]': formToken
        }
        #print("Loggin in..")

        response = self.s.post(self.base_url+'/login', headers=headers, data=data)
        if response.url.endswith("login"):
            print("Bad Credentials")
            sys.exit(0)
        loader.stop()


        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'x-requested-with': 'XMLHttpRequest',
        }
        userInfo = self.s.post(self.base_url+"/Studentcard/Student/getStudents", headers=headers).json()[0]

    def getGrade(self, location):
        loader = SpinningLoader(text="Searching grade", complete_text="Grade found", speed=0.15, animation="bounce", colour="yellow")
        loader.start()
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        response = self.s.post(self.base_url+'/Grades/Config/getConfig', headers=headers)
        data = response.json()

        classId = data["skoreClassID"]
        report = data["currentReport"]
        #Hello message
        classroom = data["reports"][0]["className"]
        

        data = {
        'reportID': report,
        'skoreClassID': classId,
        'pupilID': '0'
        }
        #print("Getting Grade URL for "+ classroom)
        response = self.s.post(self.base_url+'/Grades/Report/getReport', headers=headers, data=data)
        info = response.json()
        url = "http:"+unquote(info["reportData"]["url"])
        loader.stop()

        loader = SpinningLoader(text="Downloading", complete_text="Downloaded", speed=0.15, animation="bounce", colour="blue")
        loader.start()
        data = self.s.get(url)
        pdf = open(location,"wb")
        pdf.write(data.content)
        pdf.close()
        loader.stop()
