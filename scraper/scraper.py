from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# **Setup Selenium with Headless Chrome**
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")

# Start WebDriver globally
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def scrape_amazon(product_name):
    """Scrape Amazon search results for multiple products."""
    url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    driver.get(url)

    products = []
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']"))
        )
        product_elements = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")[:5]

        for item in product_elements:
            try:
                title = item.find_element(By.CSS_SELECTOR, "h2 a span").text
                price_element = item.find_elements(By.CSS_SELECTOR, ".a-price span.a-offscreen")
                price = price_element[0].text.replace("₹", "").replace(",", "").strip() if price_element else "N/A"
                image = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                link = "https://www.amazon.in" + item.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")

                products.append({"title": title, "price": price, "image": image, "url": link})
            except Exception as e:
                print(f"Skipping Amazon product due to error: {e}")

    except Exception as e:
        print(f"Amazon scraping failed: {e}")

    return products


def scrape_flipkart(product_name):
    """Scrape Flipkart search results for multiple products."""
    url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"
    driver.get(url)

    products = []
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div._1AtVbE"))
        )
        product_elements = driver.find_elements(By.CSS_SELECTOR, "div._1AtVbE")[:5]

        for item in product_elements:
            try:
                title = item.find_element(By.CSS_SELECTOR, "a.IRpwTa").text
                price_element = item.find_elements(By.CSS_SELECTOR, "div._30jeq3")
                price = price_element[0].text.replace("₹", "").replace(",", "").strip() if price_element else "N/A"
                image = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                link = "https://www.flipkart.com" + item.find_element(By.CSS_SELECTOR, "a.IRpwTa").get_attribute("href")

                products.append({"title": title, "price": price, "image": image, "url": link})
            except Exception as e:
                print(f"Skipping Flipkart product due to error: {e}")

    except Exception as e:
        print(f"Flipkart scraping failed: {e}")

    return products


@app.route("/scrape", methods=["GET"])
def scrape():
    product_name = request.args.get("product")
    if not product_name:
        return jsonify({"error": "Product name is required"}), 400

    amazon_products = scrape_amazon(product_name)
    flipkart_products = scrape_flipkart(product_name)

    return jsonify({"amazon": amazon_products, "flipkart": flipkart_products})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
