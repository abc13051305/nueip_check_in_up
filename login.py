from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import requests

# ========== 基本設定 ==========
load_dotenv()
COMPANY_CODE = os.getenv("NUEIP_COMPANY_CODE")
ACCOUNT = os.getenv("NUEIP_ACCOUNT")
PASSWORD = os.getenv("NUEIP_PASSWORD")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

LATITUDE = 23.008379077960313  # 新一軍食堂
LONGITUDE = 120.22051266925577

# ========== 工具方法 ==========
def get_punch_type():
    now = datetime.now().time()
    morning = datetime.strptime("08:30", "%H:%M").time()
    evening = datetime.strptime("18:00", "%H:%M").time()
    if now < morning:
        return "上班"
    elif now >= evening:
        return "下班"
    else:
        return "上班"

def notify_discord(webhook_url, message):
    try:
        payload = {"content": message}
        headers = {"Content-Type": "application/json"}
        res = requests.post(webhook_url, json=payload, headers=headers)
        if res.status_code in [200, 204]:
            print("📬 Discord 通知已發送！")
        else:
            print(f"⚠️ Discord 通知失敗：{res.status_code}")
    except Exception as e:
        print(f"❌ 發送 Discord 通知失敗：{e}")

# ========== 啟動瀏覽器 ==========
options = Options()
# options.add_argument('--headless')  # 測試時可先關閉，看到畫面
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 1
})

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("🔐 登入 NUEIP 中...")
    driver.get("https://portal.nueip.com/login")
    time.sleep(2)
    driver.find_element(By.NAME, "inputCompany").send_keys(COMPANY_CODE)
    driver.find_element(By.NAME, "inputID").send_keys(ACCOUNT)
    driver.find_element(By.NAME, "inputPassword").send_keys(PASSWORD)
    driver.find_element(By.CLASS_NAME, "login-button").click()
    time.sleep(5)

    # 模擬 GPS 位置
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "accuracy": 100
    })
    print(f"📍 已模擬定位：({LATITUDE}, {LONGITUDE})")

    # 自動選擇打卡類型
    punch_type = get_punch_type()
    driver.find_element(By.XPATH, f'//span[text()="{punch_type}"]/ancestor::button[1]').click()
    print(f"✅ 已完成 {punch_type} 打卡")

    # Discord 通知
    notify_discord(DISCORD_WEBHOOK, f"✅ 已成功完成「{punch_type}」打卡（位置：新一軍食堂）")

except Exception as e:
    print("❌ 發生錯誤：", e)
finally:
    driver.quit()