from flask import Flask, request, jsonify
from googlesearch import search
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
CORS(app)

def scrape_product(url):
    """Scrape product title and price from Amazon or Flipkart"""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        driver.implicitly_wait(10)

        title, price = None, None

        if "amazon" in url:
            title = driver.find_element(By.ID, "productTitle").text.strip()
            price = driver.find_element(By.CSS_SELECTOR, ".a-price-whole").text.strip()
        elif "flipkart" in url:
            title = driver.find_element(By.CSS_SELECTOR, "h1._6EBuvT span.VU-ZEz").text.strip()
            price = driver.find_element(By.CSS_SELECTOR, "div.Nx9bqj").text.strip()
        
        if title and price:
            return {"title": title, "price": price, "link": url}
    except Exception as e:
        return None
    finally:
        driver.quit()

@app.route("/search", methods=["POST"])
def google_search():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    top_results = list(search(query, num_results=5))
    print(top_results)
    products = []
# "amazon" in link or
    for link in top_results:
        if "flipkart" in link:
            product = scrape_product(link)
            if product:
                products.append(product)

    return jsonify({"products": products})

if __name__ == "__main__":
    app.run(debug=True)
