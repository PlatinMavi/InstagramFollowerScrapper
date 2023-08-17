from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

from bs4 import BeautifulSoup

# While using,
# checkpoint_freq meanshow frequently it should save it so beacuse of massive amounts of followers, you wont lose it. pass it an intager. Each iter returns 12 followers.
# is_visible is for if you want to see it working and opening browser, else it will just run in background. pass it a boolean
# format_preferance is for if you want followers in the format of link or just username. Possible inputs = "username", "link"

class mipodvapeScrapper():

    def __init__(self, username, password, checkpoint_freq, is_visible, format_preferance) -> None:
        self.username = username
        self.password = password
        self.freq = checkpoint_freq
        self.vis = is_visible
        self.pref = format_preferance

    def Parser(self,html):
        soup = BeautifulSoup(html, "html.parser")
        Usernames = soup.find_all("a")
        returnies = []

        for User in Usernames:
            returnies.append(User.get("href").replace("/",""))

        return returnies

    def ScrapeFollowers(self, url):

        if "followers" in url:
            pass
        else :
            if url.endswith("/"):
                url = url+"followers/"
            else:
                url = url+"/followers/"

        options = webdriver.ChromeOptions()
        if self.vis == False:
            options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.instagram.com/")

        try:
            element = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/button")
            element.click()
        except NoSuchElementException:
            print("[Info] - Instagram did not require to accept cookies this time.")

        usernameInput = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        passwordInput = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        usernameInput.clear()
        usernameInput.send_keys(self.username)
        passwordInput.clear()
        passwordInput.send_keys(self.password)

        login_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()
        time.sleep(6)

        driver.get(url)
        FollowerContainer = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")))

        ITER = 0

        while True:
            initial_height = driver.execute_script("return arguments[0].scrollHeight", FollowerContainer)
            
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", FollowerContainer)
            time.sleep(1.5)
            ITER+=1
            new_height = driver.execute_script("return arguments[0].scrollHeight", FollowerContainer)
            
            if new_height == initial_height:
                break  # Reached the bottom of the scrollable element

            if ITER%self.freq == 0:
                print("CheckPoint...")
                html = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div"))).get_attribute("innerHTML")
                followers = self.Parser(html)
                followers = list(set(followers))
                with open('followers.txt', 'w') as fp:
                    if self.pref == "username":
                        for item in followers:
                            # write each item on a new line
                            fp.write("%s\n" % item)
                    elif self.pref == "link":
                        for item in followers:
                            # write each item on a new line
                            fp.write("%s\n" % "https://www.instagram.com/"+item+"/")
                    print('CheckPoint Saved')

        html = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div"))).get_attribute("innerHTML")
        followers = self.Parser(html)
        followers = list(set(followers))
        with open('followers.txt', 'w') as fp:
            if self.pref == "username":
                for item in followers:
                    # write each item on a new line
                    fp.write("%s\n" % item)
            elif self.pref == "link":
                for item in followers:
                    # write each item on a new line
                    fp.write("%s\n" % "https://www.instagram.com/"+item+"/")
    
        driver.quit()
    
username = input("Username or Email: ")
password = input("Password: ")
print("checkpoint_freq means how frequently it should save it so beacuse of massive amounts of followers, you wont lose it. pass it an intager. \n Each iter returns 12 followers. if 3, it will save each 36 follower ")
freq = input("Checkpoint Frequency: ")
is_visible = input("1 if want to see chrome working, 0 for working at background: ")
if is_visible == "1":
    v = True
elif is_visible == "0":
    v = False
format = input("Save as 'username' or 'link'. Please type accordingly: ")

user = input("if you want to scrape other users followers type link, if mipodvape please type 1: ")
if user =="1":
    f = "https://www.instagram.com/mipodvape/"+"followers/"
else :
    f = user


mipodvapeScrapper(username,password,int(freq),v,format).ScrapeFollowers(f)
print("Done")