# **Real-Time Disaster Information System**  

🌍 **A Python-based system for monitoring and analyzing real-time disaster data from multiple sources**  

---

## **📌 Overview**  
This project collects, processes, and stores real-time disaster-related information from **Reddit, NewsAPI, and weather sources** to provide timely alerts and analysis. The system filters relevant disaster reports, performs sentiment analysis, and stores structured data in **MongoDB**.  

🔗 **GitHub Repository:** [https://github.com/krishrathi1/REAL-TIME-DISEASTER-INFORMATION-](https://github.com/krishrathi1/REAL-TIME-DISEASTER-INFORMATION-)  

---

## **⚙️ Features**  

✅ **Real-time data collection** from:  
   - **Reddit** (disaster-related posts)  
   - **NewsAPI** (news articles)  
   - **Weather API** (extreme weather alerts)  

✅ **Spam detection** using **Logistic Regression** (NLP-based filtering)  
✅ **Sentiment analysis** using **VADER Sentiment**  
✅ **Geolocation tagging** (if available)  
✅ **MongoDB storage** for structured disaster reports  
✅ **Continuous monitoring** (updates every 5 minutes)  

---

## **🚀 Installation & Setup**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/krishrathi1/REAL-TIME-DISEASTER-INFORMATION-.git
cd REAL-TIME-DISEASTER-INFORMATION-
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### **3. Configure API Keys**  
Replace placeholders in `disaster_monitor.py` with your own API keys:  
- **Reddit API** (`REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`)  
- **NewsAPI** (`NEWSAPI_KEY`)  
- **MongoDB** (`MONGO_URI`)  

### **4. Run the Script**  
```bash
python disaster_monitor.py
```

---

## **📂 Project Structure**  
```
REAL-TIME-DISEASTER-INFORMATION-/
├── disaster_monitor.py       # Main script
├── README.md                # Documentation
├── requirements.txt         # Python dependencies
└── data/                    # (Optional) Sample datasets
```

---

## **🔍 How It Works**  

1. **Data Collection**  
   - **Reddit:** Scans `/r/india` and `/r/indianews` for disaster keywords (floods, earthquakes, etc.)  
   - **NewsAPI:** Fetches disaster-related news articles mentioning "India"  
   - **Weather API:** (Optional) Checks for extreme weather alerts  

2. **Spam Filtering**  
   - Uses **Logistic Regression** to classify relevant vs. irrelevant posts  

3. **Sentiment Analysis**  
   - **VADER Sentiment** detects emotional tone (positive/negative/neutral)  

4. **Data Storage**  
   - Structured data is stored in **MongoDB**  

5. **Continuous Monitoring**  
   - Runs every **5 minutes** for real-time updates  

---

## **📊 Sample Output**  
```json
{
  "title": "Flood alert in Assam",
  "description": "Heavy rains cause flooding in multiple districts...",
  "source": "NewsAPI",
  "timestamp": "2023-10-25T14:30:00Z",
  "sentiment": "negative",
  "location": "Assam, India"
}
```

---

## **📜 License**  
This project is open-source under the **MIT License**.  

---

## **📬 Contact**  
- **Author:** Krishna Rathi  
- **GitHub:** [@krishrathi1](https://github.com/krishrathi1)  
- **Email:** (Add your email if applicable)  

---

🚨 **Stay informed, stay safe!** 🚨
