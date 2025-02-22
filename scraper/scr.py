from flask import Flask, request, jsonify
from googlesearch import search
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
from bs4 import BeautifulSoup 
import re 

app = Flask(__name__)
CORS(app, supports_credentials=True)

def scrape_product(url):
    """Scrape product title and price from Amazon or Flipkart"""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        time.sleep(random.uniform(2, 5))

        driver.implicitly_wait(10)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title, price, image = None, None, None

        if "amazon" in url:
            title = soup.find("span", {"id": "productTitle"}).text.strip()
            print(title)
            try:
                price_element = soup.select_one("span.a-price-whole")
                price = price_element.text.strip() if price_element else "Price not found"
            except AttributeError:
                price = "Price not found"
            image = driver.find_element(By.CSS_SELECTOR, "#landingImage").get_attribute("src")
            # price = driver.execute_script("return document.querySelector('.a-price-whole')?.innerText;")
            print(price)
            print(image)
        elif "flipkart" in url:
            title = driver.find_element(By.CSS_SELECTOR, "h1._6EBuvT span.VU-ZEz").text.strip()
            price = driver.find_element(By.CSS_SELECTOR, "div.Nx9bqj").text.strip()
            clean_price = re.sub(r"[^\d]", "", price)
            print(clean_price)
            image = driver.find_element(By.CSS_SELECTOR, "img.DByuf4").get_attribute("src")
        
        if title :
            return {"title": title, "image":image , "price":clean_price, "link": url}
    except Exception as e:
        return None
    finally:
        driver.quit()

@app.route("/search", methods=["POST"])
def google_search():
    print("Received request to /search")  # Log to confirm the route is hit
    print("Request method:", request.method)  # Log the HTTP method
    print("Request headers:", request.headers)  # Log the headers
    print("Request data:", request.get_json())  # Log the request payload

    data = request.get_json()
    query = data.get("query")
    print("Received query:", query)  # Log the query

    if not query:
        return jsonify({"error": "No query provided"}), 400

    top_results = list(search(query, num_results=3))
    print("Top results:", top_results)  # Log the top results
    products = []

    for link in top_results:
        if "amazon" in link or "flipkart" in link:
            print("Scraping link:", link)  # Log the link being scraped
            product = scrape_product(link)
            if product:
                products.append(product)

    return jsonify({"products": products})
if __name__ == "__main__":
    app.run(debug=True)
