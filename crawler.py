import requests, lxml.html, json
from datetime import datetime

path_json = 'C:\\Users\\'

#login & export_file (json)
def export_file(sDate, eDate, email, psw, path_download):
    s = requests.session()
	login_url = 'https://xxxxxx.com/login'
    login = s.get(login_url)
    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    form['email'] = email
    form['password'] = psw
    login = s.post(login_url, data=form)
    #end login
    json_obj = None
    fileNam = 'export_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.json'
    if login.ok:
        #Get .json file
        form['start_date'] = sDate 
        form['end_date'] = eDate 
        response = s.post('https://xxxxxx/analyses/export', data=form)
        #response.url
        if response.ok:
            response_decode = response.content.decode('utf-8')
            json_obj = [True, json.loads(response_decode)]
            #write the content to file
            with open(path_download + fileNam, "wb") as code:
                code.write(response.content)
        else:
            json_obj = [False, "err02: could not access file"]
        # end .json file
    else:
        json_obj = [False, "err01: failed login"]

    return json_obj
#end func export_file