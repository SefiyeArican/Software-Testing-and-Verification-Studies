from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

driver.get("http://automationexercise.com/products")

# Ürünleri rastgele seçme işlemi
products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-image-wrapper")))
secilen_urunler = []

for product in products[:3]:  # Rastgele 3 ürün seçiliyor
    name = product.find_element(By.TAG_NAME, "p").text
    price = product.find_element(By.TAG_NAME, "h2").text
    button = product.find_element(By.TAG_NAME, "a")
    
    secilen_urunler.append((name, price))
    button.click()

    cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//u[contains(text(),'View')]")))
    cart.click()

cart_items = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[@class='cart_description']/h4")))
cart_prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[@class='cart_price']/p")))

eslesiyor_mu = True
for i in range(len(secilen_urunler)):
    cart_name = cart_items[i].text
    cart_price = cart_prices[i].text
    
    if cart_name != secilen_urunler[i][0] or cart_price != secilen_urunler[i][1]:
        eslesiyor_mu = False
        break

if eslesiyor_mu:
    print("Test başarılı")
else:
    print("Test başarısız")
