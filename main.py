from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.color import Color
import time

# various browser options
options = webdriver.chrome.options.Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

# urls
chromedriver_path = r'C:\Users\user\path/chromedriver.exe'  # fill with the location of the driver exe.
url = 'https://www.instagram.com/accounts/login/'
prefix = 'https://www.instagram.com/'

# Credentials
user = 'user'  # fill with username
password = 'password'  # fill with password

# my target username made seperate incase i want the functionality to plug various users into the prefix template
target_user = 'target'  # fill with target users instagram name


class Bot():
    def __init__(self, email, password):
        self.browser = webdriver.Chrome(chromedriver_path, options=options)
        self.email = email
        self.password = password

    def signin(self):
        driver = self.browser
        driver.get(url)
        driver.implicitly_wait(10)

        emailInput = driver.find_element_by_xpath("//input[@name='username']")
        passwordInput = driver.find_element_by_xpath("//input[@name='password']")

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)

    def like_photo(self, username):
        driver = self.browser
        driver.get(prefix + username + '/')
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            except Exception:
                continue

        # Liking photos
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            # check if heart is red, if so skip since we've already liked it
            cssValue = driver.find_element_by_css_selector('#react-root > section > main > div > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > svg').value_of_css_property("fill")
            cssValue = Color.from_string(cssValue).hex
            if cssValue == "#262626":
                try:
                    like_button = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button')
                    like_button.click()
                except Exception:
                    continue

        # print('done')

    def closebrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closebrowser()


bot = Bot(user, password)
bot.signin()
bot.like_photo(target_user)
bot.closeBrowser()
