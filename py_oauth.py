# -*- coding: utf-8 -*-
import ast
#from selenium.webdriver import Edge
#from selenium.webdriver import DesiredCapabilities
import re
from selenium import webdriver
import time
import tkinter
import requests
#from tkinter.messagebox import showinfo

#clientid for testing: 4c55fa54-0d2d-41d6-a140-69cd0ed098d1
class Login():
    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.title('OAuth')
        self.tk.geometry('400x400')
        self.id = tkinter.StringVar()

        tkinter.Label(self.tk, text='ClientID:').place(x=30,y=10)

        self.t1 = tkinter.Entry(self.tk, textvariable=self.id)

        self.t1.place(width=150, height=20,x=150,y=10)

        self.bt_login = tkinter.Button(self.tk, text='Run', command=self.start)
        self.bt_re = tkinter.Button(self.tk, text='Cancel', command=self.stop)
        self.bt_login.place(x=40,y=40)
        self.bt_re.place(x=200,y=40)
        self.txt = tkinter.Text(self.tk)
        self.txt.place(x=90, y=100, width=300, height=150)
        #
        self.access_token_title_label = tkinter.Label(self.tk, text="access token:")
        self.access_token_title_label.place(x=0, y=100)
        self.access_token_text = tkinter.Text(self.tk)
        self.access_token_text.place(x=90, y=100, width=300, height=150)
        # self.access_token_text = tkinter.Text(self.tk)
        # self.access_token_text.grid(row=2, column=1)
        #
        self.refresh_token_title_label = tkinter.Label(self.tk, text="refresh token:")
        self.refresh_token_title_label.place(x=0, y=250)
        self.refresh_token_text = tkinter.Text(self.tk)
        self.refresh_token_text.place(x=90, y=230, width=300, height=150)

        # self.expires_in_title_label = tkinter.Label(self.tk, text="expires_in:")
        # self.expires_in_title_label.grid(row=4, column=0)
        # self.expires_in_text = tkinter.Text(self.tk)
        # self.expires_in_text.grid(row=4, column=1)

        #self.capabilities = DesiredCapabilities.CHROME
        #self.driver = Edge(capabilities=self.capabilities)
        self.driver = webdriver.Chrome (r'C:\chromedriver.exe')
        #self.driver = webdriver.Chrome ()

    def start(self):
        clientid = self.id.get()
        # capabilities['ms:inPrivate'] = True

        self.driver.get(
            "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=" + clientid + "&scope=openid%20profile%20https://ads.microsoft.com/ads.manage%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient&state=ClientStateGoesHere&prompt=login")
        time.sleep(5)
        url = self.driver.current_url

        while True:
            b = url[-4:-1]
            # c = url[-15]
            d = ''
            print('auto capture url from user login page: ', url)
            if b == 'Her':
                #d = url[-63:-26]
                s = url
                a = r'code=(.*?)&state'
                d = re.findall(a, s)


                print('auto retrieve Authentication Code from final url: ', d)
                break
            else:
                time.sleep(5)
                url = self.driver.current_url
                print(url)
                url = url

        # grantedcode = d

        url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

        a = {'ContentType': 'application/x-www-form-urlencoded',
             'client_id': clientid,
             'scope': 'https://ads.microsoft.com/ads.manage offline_access',
             'code': d,
             'grant_type': 'authorization_code',
             'redirect_uri': 'https://login.microsoftonline.com/common/oauth2/nativeclient'}

        r = requests.post(url, data=a, allow_redirects=True)  # << Note data is used here
        dict = ast.literal_eval(r.text)
        access_token = dict['access_token']
        refresh_token = dict['refresh_token']
        expires_in = dict['expires_in']
        self.access_token_text.insert(tkinter.END,access_token)
        self.refresh_token_text.insert(tkinter.END,refresh_token)
        # self.expires_in_text.insert(tkinter.END,expires_in)
        print('This is your access token: ', access_token)
        print('This is your refresh token: ', refresh_token)
        print('Your access token will be expires in: ', expires_in)

    def stop(self):
        self.driver.quit()

def main():
    tk = Login()
    tk.tk.mainloop()

if __name__ == '__main__':
    main()

