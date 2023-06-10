from selenium import webdriver
from selenium.webdriver.common.by import By
import message, time, os

class Oj(object):

    def __init__(self):
        self.start_url = "https://acm.zcmu.edu.cn/JudgeOnline/status.php?user_id=202023211401018&jresult=4"
        self.driver = webdriver.Chrome(executable_path=r"webdriver/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.num = 0

    def get_message(self, cookie):
        self.driver.execute_script(rf"""window.open("{self.start_url}", )""")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        try:
            while True:
                href_ele = self.driver.find_elements(By.XPATH, """//*[text()='C++']""")[1:]
                url_list = []
                for a in href_ele:
                    url = a.get_attribute("href")
                    url_list.append(url)
                for url in url_list:
                    print(url)
                    self.get_code(url)


                self.driver.switch_to.window(self.driver.window_handles[0])
                next_ele = self.driver.find_element(By.XPATH, """//*[@id="center"]/a[3]""")
                next_ele.click()
                time.sleep(1)
                if len(href_ele)<20:
                    return 0
        except:
            return 0




    def get_code(self, url):

        js = f"""window.open("{url}")"""
        self.driver.execute_script(js)
        self.driver.switch_to.window(self.driver.window_handles[1])
        text_ele = self.driver.find_element(By.CLASS_NAME, "container")
        text = text_ele.get_attribute("innerText")
        if not os.path.exists("code"):
            os.mkdir("code")
        with open(f"code/{str(self.num)}.txt", "w", encoding="utf8")as f:
            f.write(text.replace(" ", " "))
        self.num += 1
        if len(self.driver.window_handles)>1:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(2)

    def run(self):
        cookie = self.get_cookie()
        self.get_message(cookie)



    def get_cookie(self):
        url = "https://acm.zcmu.edu.cn/JudgeOnline/loginpage.php"
        self.driver.get(url)
        name = self.driver.find_element(By.NAME, "user_id")
        pwd = self.driver.find_element(By.NAME, "password")
        name.send_keys(message.name)
        pwd.send_keys(message.pwd)
        button = self.driver.find_element(By.NAME, "submit")
        button.click()
        time.sleep(1)
        self.driver.execute_script(rf"""window.open("https://acm.zcmu.edu.cn/JudgeOnline/userinfo.php?user=202023211401018")""")
        time.sleep(1)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        cookie = self.driver.get_cookies()
        print(cookie)
        return cookie

if __name__ == '__main__':
    o = Oj()
    o.run()
    time.sleep(4)
    o.driver.quit()



