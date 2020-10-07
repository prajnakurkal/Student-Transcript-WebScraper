import requests
import lxml.html
import bs4
from bs4 import BeautifulSoup
import re

service_url = 'https://sis.rutgers.edu/tags/student.htm'

def scanUser():
	user = input("enter netid username ")
	return user
def scanPass():
	pwd = input("enter netid password ")
	return pwd
def cas_login(service, username, password):
    # GET parameters - URL we'd like to log into.
    params = {'service': service}
    LOGIN_URL = 'https://cas.rutgers.edu/login'

    # Start session and get login form.
    session = requests.session()
    login = session.get(LOGIN_URL, params=params)

    # Get the hidden elements and put them in our form.
    login_html = lxml.html.fromstring(login.text)
    hidden_elements = login_html.xpath('//form//input[@type="hidden"]')
    form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

    # "Fill out" the form.
    form['username'] = username
    form['password'] = password

    # Finally, login and return the session.
    qq = session.post(LOGIN_URL, data=form, params=params)
    return qq;
def checkLogin(webPage):
	if(webPage.title.get_text() == "Rutgers  Central  Authentication  Service (CAS)"):
		return False
	elif(webPage.title.get_text() == "Student Unofficial Transcript and Grades | Home"):
		return True
	else:
		return False
def scanSemester(): #can also be used to check semester validity
	sem = input("what semester would you like to check your grades for ")
	semester = sem.upper()
	if("FALL" in semester or "SPRING" in semester or "SUMMER" in semester or "WINTER" in semester):
		return semester
	else:
		return None
def getSemesterID(semester):
	ID = 'RU'
	if('FALL' in semester):
		ID += '9'
	elif('SPRING' in semester):
		ID += '1'
	elif('SUMMER' in semester):
		ID += '7'
	elif('WINTER' in semester):
		ID += '12'
	else:
		return None #not a semester
	for c in semester:
		if(c.isdigit()):
			ID += c
	return ID
def scrape():
	page = cas_login(service_url, scanUser(), scanPass())
	soup = BeautifulSoup(page.content, 'html.parser')
	if(checkLogin(soup) == False):
		print("login error")
		return
	semID = getSemesterID(scanSemester())
	if(semID == None):
		print("sorry there was an error we cannot find this semester")
		return
	semesterName = soup.find(id=re.compile(semID)) #semester = none if not found
	if(semesterName == None):
		print('sorry there was an error we cannot find this semester')
		return
	semester = semesterName.parent
	body = semester.find('tbody')
	name = body.find_all(class_="name")
	grade = body.find_all(class_="grade")
	for n, g in zip(name, grade):
		if not g.get_text():
			print("so far there's no grade for: " + n.get_text())
		else:
			print("in the course " + n.get_text() + " your grade is " + g.get_text()) 


