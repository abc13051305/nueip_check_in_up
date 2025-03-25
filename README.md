# NUEiP 自動打卡機器人

自動登入 NUEiP 打卡系統、模擬 GPS 定位、依時間自動選擇上班／下班打卡，並透過 Discord 通知你打卡成功。搭配 GitHub Actions，每天自動執行。

---

## 📦 功能特色

- ✅ 自動登入 NUEiP 打卡頁面
- 📍 模擬指定位置進行打卡
- 🕐 自動判斷時間：早上 08:30 打上班卡，晚上 18:00 打下班卡
- 🎌 依據政府公曆 API 判斷是否為休假日（自動略過）
- 💬 打卡完成後透過 Discord Webhook 發送通知
- ☁️ 支援 GitHub Actions，實現每日自動打卡

---

## 🔧 環境需求

- Python 3.10+
- Google Chrome（建議安裝最新版）

---

## 🧪 本機執行方式

### 1️⃣ 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2️⃣ 建立 `.env` 檔案（請勿上傳 GitHub）

```
NUEIP_COMPANY_CODE=你的公司代碼
NUEIP_ACCOUNT=你的帳號
NUEIP_PASSWORD=你的密碼
DISCORD_WEBHOOK=https://discord.com/api/webhooks/xxx/yyy
```

### 3️⃣ 執行打卡

```bash
python login.py
```

如遇假日會自動跳過。

---

## ☁️ GitHub Actions 自動打卡

### 1️⃣ 建立 GitHub Secrets

到你的 repo ➜ `Settings` ➜ `Secrets and variables` ➜ `Actions` ➜ `New repository secret`：

| Name               | Value                     |
|--------------------|---------------------------|
| NUEIP_COMPANY_CODE | 公司代碼                  |
| NUEIP_ACCOUNT      | 使用者帳號                |
| NUEIP_PASSWORD     | 密碼                      |
| DISCORD_WEBHOOK    | Discord Webhook URL       |

### 2️⃣ 自動排程

```yaml
# .github/workflows/auto-punch.yml

on:
  schedule:
    - cron: '30 0 * * *'   # 台灣時間 08:30
    - cron: '0 10 * * *'   # 台灣時間 18:00
  workflow_dispatch:
```

每天早晚各執行一次，自動打卡 ✅

‼️記得替換掉login.py裡面的經緯度，經緯度可以從google map上查到

---

## 📎 政府公曆來源

資料來源：[ruyut/TaiwanCalendar](https://github.com/ruyut/TaiwanCalendar)

API 範例：
```
https://cdn.jsdelivr.net/gh/ruyut/TaiwanCalendar/data/2025.json
```

---

## 🐾 特別感謝

- ruYu 提供台灣假期 API

---

> Maintained by 小津 (Nancy) ✨
> 若有需要協助請私訊我或留言討論區 🙌
