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
options.add_argument("--headless")  # Run without GUI for speed
options.add_argument("--no-sandbox")  # Required for some environments
options.add_argument("--disable-dev-shm-usage")  # Fix resource issues
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")

# Start the WebDriver **globally** for faster scraping
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def scrape_product_details(url):
    """Scrape product details (title, price, image) from Amazon or Flipkart."""
    driver.get(url)

    try:
        # **Wait until the title is loaded**
        title = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text

        # **Wait for price to load**
        try:
            if "amazon" in url:
                price_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "a-price"))
                )
                price = price_element.text.replace("₹", "").replace(",", "").strip()
            elif "flipkart" in url:
                price_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_30jeq3"))
                )
                price = price_element.text.replace("₹", "").replace(",", "").strip()
            else:
                price = "0"
            price = int(float(price))  # Convert to number
        except Exception:
            price = 0  # Default if not found

        # **Scrape Image**
        try:
            image_element = driver.find_element(By.TAG_NAME, "img")
            image = image_element.get_attribute("src")
            if not image:
                image = image_element.get_attribute("data-src")  # Try lazy-loaded images
        except Exception:
            image = ""

        return {"title": title, "price": price, "image": image, "url": url}

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


@app.route("/scrape", methods=["GET"])
def scrape():
    product_name = request.args.get("product")
    if not product_name:
        return jsonify({"error": "Product name is required"}), 400

    urls = [
        f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}",
        f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}",
    ]

    products = []
    for url in urls:
        product = scrape_product_details(url)
        if product:
            products.append(product)

    if not products:
        return jsonify({"error": "Failed to scrape product details"}), 500

    return jsonify(products)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

