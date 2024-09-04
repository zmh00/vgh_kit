import requests
import re
# from bs4 import BeautifulSoup


class Client:
    def __init__(self, login_id=None, login_psw=None, TEST_MODE=False):
        # 建立request session
        s = requests.session()
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari',
            'referer': 'https://eip.vghtpe.gov.tw/login.php'
        }
        s.headers.update(headers)
        self.session = s  # 將建立的物件存在instance屬性中
        self.headers = headers
        self.TEST_MODE = TEST_MODE
        self.login_id = login_id
        self.login_psw = login_psw
        self.webmode = None
        self.webbrowser = None


    def acquire_id_psw(self):    
        while(1):
            login_id = input("Enter your ID: ").upper().strip()
            if len(login_id) != 0:
                break
        while(1):
            login_psw = input("Enter your PASSWORD: ")
            if len(login_psw) != 0:
                break
        return login_id, login_psw


    def eip_login_requests(self, login_id=None, login_psw=None): # TODO目前需要測試
        '''
        使用requests連線EIP 
        '''
        if login_id is None or login_psw is None:
            if self.login_id is None or self.login_psw is None:
                login_id, login_psw = self.acquire_id_psw()
            else:
                login_id = self.login_id
                login_psw = self.login_psw

        baseURL = 'https://eip.vghtpe.gov.tw'

        r = self.session.get(url="https://eip.vghtpe.gov.tw/login.php") # 必須先到啟始頁
        url = 'https://eip.vghtpe.gov.tw/login_action.php'
        data = {
            'loginCheck': 0,
            'login_name': login_id,
            'password': login_psw,
            'fromAjax': 0, # 設定0會直接回傳auth_token
        }
        r1 = self.session.post(url, data=data)
        # r2 = self.session.get(url="https://eip.vghtpe.gov.tw/login_check.php")

        match = re.search(r'window\.location\s*=\s*["\'](.*?)["\']', r1.text)

        if match:
            redirect_url = match.group(1)
            print(f"Auth_token URL found: {redirect_url}")
        else:
            print("Auth_token URL Not found!")
            return False

        url = baseURL+redirect_url
        r3 = self.session.get(url=url)

        # 顯示個人EIP內功能清單
        # https://eip.vghtpe.gov.tw/app_menu/app_menu.php?action=personal_appmenu_view&_=1724795599436

        # DRWEB系統
        # r4 = self.session.get(url="https://web9.vghtpe.gov.tw/emr/qemr/qemr.cfm?action=findPatient&srnId=DRWEBAPP&seqno=009")

    
    def scheduler_login(self, login_id=None, login_psw=None):
        '''
        登入排程系統
        '''
        if login_id is None or login_psw is None:
            if self.login_id is None or self.login_psw is None:
                login_id, login_psw = self.acquire_id_psw()
            else:
                login_id = self.login_id
                login_psw = self.login_psw
        
        tURL = "https://cks.vghtpe.gov.tw/Exm/HISLogin/CheckUserByID"
        login_payload = {
            'signOnID': login_id,
            'signOnPassword': login_psw
        }
        r = self.session.post(tURL, data=login_payload)
        if r.status_code == 200:
            print("SCHEDULER: Login succeeded!")
            self.login_id = login_id
            self.login_psw = login_psw
            return True
        else:
            print("SCHEDULER: Login failed!")
            self.login_id = None
            self.login_psw = None
            return False


    def login_drweb(self):
        self.eip_login_requests()
        r4 = self.session.get(url="https://web9.vghtpe.gov.tw/emr/qemr/qemr.cfm?action=findPatient&srnId=DRWEBAPP&seqno=009")


if __name__=='__main__':
    c=Client()
    c.TEST_MODE = True

### TEST ###

# import requests
# from bs4 import BeautifulSoup
# import re

# login_id = ''
# login_psw = ''
# headers = {
#     'user-agent': 'Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari',
#     'referer': 'https://eip.vghtpe.gov.tw/login.php'
# }


# s = requests.session()
# s.headers.update(headers)
# baseURL = 'https://eip.vghtpe.gov.tw'

# r = s.get(url="https://eip.vghtpe.gov.tw/login.php") # 必須先到啟始頁
# url = 'https://eip.vghtpe.gov.tw/login_action.php'
# data = {
#     'loginCheck': 0,
#     'login_name': login_id,
#     'password': login_psw,
#     'fromAjax': 0, # 設定0會直接回傳auth_token
# }
# r1 = s.post(url, data=data)
# # r2 = s.get(url="https://eip.vghtpe.gov.tw/login_check.php")

# match = re.search(r'window\.location\s*=\s*["\'](.*?)["\']', r1.text)

# if match:
#     redirect_url = match.group(1)
#     print(f"Auth_token URL found: {redirect_url}")
# else:
#     print("Auth_token URL Not found!")

# url = baseURL+redirect_url
# r3 = s.get(url=url)

# r4 = s.get(url="https://web9.vghtpe.gov.tw/emr/qemr/qemr.cfm?action=findPatient&srnId=DRWEBAPP&seqno=009")

# soup = BeautifulSoup(r.text)
# print(soup.prettify())

