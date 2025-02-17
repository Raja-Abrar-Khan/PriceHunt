# # import libraries
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from selenium.webdriver.chrome.options import Options

# from bs4 import BeautifulSoup 

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# #Define the URL
# url = "https://www.amazon.in/Samsung-Galaxy-Smartphone-Yellow-Storage/dp/B0CS5ZZMN8"

# #load the web page
# driver.get(url)

# #set the maximum time to load the web page in seconds
# driver.implicitly_wait(10)
# # collect data that are within the ID of contents
# # title_element = driver.find_element(By.ID, "productTitle")
# title = driver.find_element(By.ID, "productTitle").text.strip()
# # price = driver.find_element(By.CSS_SELECTOR, "a-price-whole").text.strip()
# # html='''
# # <div class="a-section a-spacing-none aok-align-center aok-relative"> <span class="aok-offscreen">   ₹57,999.00 with 23 percent savings    </span>          <span aria-hidden="true" class="a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage">-23%</span>         <span class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay" data-a-size="xl" data-a-color="base"><span class="a-offscreen"> </span><span aria-hidden="true"><span class="a-price-symbol">₹</span><span class="a-price-whole">57,999</span></span></span>               <span id="taxInclusiveMessage" class="a-size-mini a-color-base aok-align-center aok-nowrap">  </span>                </div>'''
# # soup = BeautifulSoup(html, 'html.parser')
# # pr=soup.select_('[aria-hidden="true"]').get_text(strip=True)
# # print(pr)
# # print(price)

# # image = driver.find_element(By.CSS_SELECTOR, "#landingImage").get_attribute("src")
# # print(image)
# # extract the title
# # title = title_element.text
# price_element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//span[@aria-hidden='true']//span[@class='a-price-whole']"))
# )

# price = price_element.text.strip()
# print(price) 
# # show the title of the product
# print(title)
# # print(price)



# Import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from bs4 import BeautifulSoup  

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("start-maximized")  # Open browser in maximized mode
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Start the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Define the URL
url = "https://www.amazon.in/Samsung-Galaxy-Smartphone-Yellow-Storage/dp/B0CS5ZZMN8"

# Load the web page
driver.get(url)

# Wait for a random time to avoid bot detection
time.sleep(random.uniform(2, 5))

# Get page source and parse it with BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Extract product title
try:
    title = soup.find("span", {"id": "productTitle"}).text.strip()
except AttributeError:
    title = "Title not found"

# Extract product price
try:
    price_element = soup.select_one("span.a-price-whole")
    price = price_element.text.strip() if price_element else "Price not found"
except AttributeError:
    price = "Price not found"

# Extract product image
try:
    image = driver.find_element(By.CSS_SELECTOR, "#landingImage").get_attribute("src")
except:
    image = "Image not found"

# Print results
print("Title:", title)
print("Price:", price)
print("Image URL:", image)

# Close the browser
driver.quit()
