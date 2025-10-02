# HR Tracker

**HR Tracker** is a desktop application built with **Python, Tkinter, and SQLite** that helps the HR team at **ICPC Zagazig Community** track and analyze group activities.

The app connects to the **Telegram API** to fetch group messages, organize them by **mentor and group**, and then generate both **Excel sheets** and **PDF summary reports** for easy review.

---

## 🚀 Features
- **Group & Mentor Selection**: Choose which group and mentor you want to analyze from a simple UI.
- **Telegram API Integration**: Fetch messages directly from Telegram channels or groups.
- **Data Storage**: Store metadata in **SQLite database** 
- **Excel Export**: Save all fetched messages into a structured **Excel sheet**.
- **PDF Reports**: Automatically generate **summary reports with charts**
- **User-Friendly UI**: Built with **Tkinter** for easy navigation.

---

## 🛠️ Tech Stack
- **Python 3**
- **Tkinter** (GUI framework)
- **SQLite** (local database)
- **Pandas** (data processing)
- **Matplotlib** (charts & visualizations)
- **Telethon** (Telegram API client for fetching messages)

### 3️⃣ Configure Telegram API (Telethon)
1. Go to [my.telegram.org](https://my.telegram.org).
2. Get your `API_ID` and `API_HASH`.
3. Create a `.env` file in the api folder:

   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash

## 👨‍💻 Contributors

- [Abdelrahman Elaraby](https://github.com/aelaraby6)
- [Basmala Saeed](https://github.com/basmalaeltabakh)
- [Aya Hamdy](https://github.com/ayahamdy44) 
