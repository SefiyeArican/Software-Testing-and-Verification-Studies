from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
import time

def zaman_olcum(user):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        #Login süresi
        start_time = time.time()
        driver.get("https://www.saucedemo.com/")
        driver.find_element(By.ID, "user-name").send_keys(user)
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
        login_time = time.time() - start_time
        
        #Ürün sepete ekleme süresi
        start_time = time.time()
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        add_to_cart_time = time.time() - start_time
        
        #Sepete gitme süresi
        start_time = time.time()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "checkout")))
        go_to_cart_time = time.time() - start_time
        
        #Ödeme bilgileri doldurma süresi
        start_time = time.time()
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("Şefiye")
        driver.find_element(By.ID, "last-name").send_keys("Arıcan")
        driver.find_element(By.ID, "postal-code").send_keys("1234")
        driver.find_element(By.ID, "continue").click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "finish")))
        checkout_info_time = time.time() - start_time
        
        #Siparişi tamamlama süresi
        start_time = time.time()
        driver.find_element(By.ID, "finish").click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "checkout_complete_container")))
        finish_order_time = time.time() - start_time
        
        #Başarılı işlem kontrolü
        if "Thank you" in driver.find_element(By.ID, "checkout_complete_container").text:
            print(f"{user} için işlem başarılı.")
        else:
            print(f"{user} için ödeme sırasında hata oluştu.")
        
        driver.quit()
        
        return [login_time, add_to_cart_time, go_to_cart_time, checkout_info_time, finish_order_time]

    except Exception as e:
        print(f"Test esnasında hata oluştu: {e}")
        driver.quit()
        return None

#Kullanıcılar ve süreç adımları
users = ["standard_user", "performance_glitch_user"]
steps = ['Login', 'Add to Cart', 'Go to Cart', 'Checkout Info', 'Finish Order']

#Kullanıcıların zaman ölçümleri
times_standard_user = zaman_olcum(users[0])
times_performance_glitch_user = zaman_olcum(users[1])

#Zaman ölçümleri grafiği
plt.plot(steps, times_standard_user, label='standard_user', marker='o')
plt.plot(steps, times_performance_glitch_user, label='performance_glitch_user', marker='o')
plt.title('Page Load Time Comparison: Standard User vs Performance Glitch User')
plt.xlabel('Steps')
plt.ylabel('Load Time (seconds)')
plt.legend()
plt.show()
