# ⚽ SportyBet Auto Trading Bot

> An intelligent Python-powered football betting automation system that aggregates predictions from multiple trusted football prediction platforms, applies weighted probability analysis, identifies value betting opportunities, and automatically places bets on SportyBet using browser automation.

---

## 📖 Overview

The **SportyBet Auto Trading Bot** is an end-to-end football betting automation platform designed to eliminate manual analysis and execute value bets based on data-driven decision making.

Instead of relying on a single prediction website, this system gathers predictions from multiple football prediction providers, standardizes the data into a unified format, calculates weighted consensus probabilities, evaluates betting edge, and automatically places qualifying bets on SportyBet.

The entire workflow is fully automated, allowing users to move from data collection to bet execution with minimal manual intervention.

---

# 🚀 Features

* ✅ Fully automated football prediction scraping
* ✅ Multi-source prediction aggregation
* ✅ Weighted probability consensus engine
* ✅ Kelly Criterion bankroll optimization
* ✅ Value betting (Edge) calculation
* ✅ Automatic SportyBet bet placement
* ✅ Playwright browser automation
* ✅ Intelligent fixture matching
* ✅ CSV data pipeline
* ✅ Duplicate match detection
* ✅ Automated login and navigation
* ✅ Supports multiple betting markets
* ✅ Modular and scalable architecture

---

# 🌍 Supported Prediction Sources

The system currently aggregates predictions from:

* Accumulator Generator
* Forebet
* BetClan
* FootballSuperTips
* Prematips
* Statarea

Each prediction source contributes to the final probability using a configurable weighting system.

---

# ⚙️ System Workflow

```text
             START
               │
               ▼
    Scrape Multiple Prediction Websites
               │
               ▼
      Normalize Prediction Data
               │
               ▼
        Store Standardized CSV Files
               │
               ▼
     Merge Predictions From All Sources
               │
               ▼
    Apply Weighted Probability Analysis
               │
               ▼
      Calculate Betting Edge (Value)
               │
               ▼
     Match Fixtures With SportyBet
               │
               ▼
      Evaluate Betting Conditions
               │
               ▼
      Automatically Place Qualified Bets
               │
               ▼
              END
```

---

# 🧠 Prediction Aggregation

Rather than trusting a single prediction provider, this project combines multiple independent prediction sources into a single weighted consensus.

Each provider has an adjustable confidence weight, allowing more reliable sources to contribute more strongly to the final prediction.

Example:

```text
Prediction Source
        │
        ▼
Acca Generator
BetClan
Forebet
Prematips
FootballSuperTips
Statarea
        │
        ▼
Weighted Probability Engine
        │
        ▼
Final Consensus Probability
```

---

# 📊 Betting Markets

The bot currently supports:

### 1X2 Market

* Home Win
* Draw
* Away Win

---

### Over / Under

* Over 2.5 Goals
* Under 2.5 Goals

---

### Both Teams To Score

* BTTS (Yes)
* BTTS (No)

---

# 💹 Value Betting Engine

The system does not place bets solely because a prediction has a high probability.

Instead, it compares:

* Model probability
* Bookmaker odds

to calculate the betting edge.

Only bets that satisfy configurable value thresholds are executed automatically.

This reduces low-value trades and focuses on mathematically favorable opportunities.

---

# 🛠 Technologies Used

### Programming

* Python

### Data Processing

* Pandas

### Web Scraping

* Requests
* BeautifulSoup
* lxml

### Browser Automation

* Playwright

### Data Storage

* CSV

### Backend Utilities

* Custom Python Modules

---

# 📂 Project Structure

```text
SportyBet-Auto-Trading-Bot/

│
├── accumulator.py
├── forebet.py
├── betclan.py
├── footballsupertips.py
├── prematips.py
├── statarea.py
│
├── SportyBet_Bot.py
├── func.py
├── Main.py
│
├── CSV FILES/
│
└── README.md
```

---

# 🔄 Data Pipeline

Every prediction website is converted into the exact same standardized dataset.

```text
DATE
TIME

HOME TEAM
AWAY TEAM

HOME PER
DRAW PER
AWAY PER

1X PER
12 PER
X2 PER

OVER 1.5
UNDER 2.5
OVER 2.5

BTS
OTS
```

This standardized format allows the betting engine to process every prediction source identically, making the system highly modular and easy to extend.

---

# 📈 Why This Project?

This project demonstrates practical experience in:

* Software Engineering
* Automation
* Data Engineering
* Web Scraping
* Probability Analysis
* Browser Automation
* Algorithm Design
* Python Development

It showcases the ability to build scalable automation systems that combine multiple data sources into intelligent decision-making pipelines.

---

# 🔮 Future Improvements

* Machine Learning prediction integration
* Expected Value (EV) analysis
* Live odds monitoring
* Multi-bookmaker support
* Arbitrage detection
* Cloud deployment
* Dashboard analytics
* Telegram notifications
* Performance tracking
* Historical ROI analysis

---

# ⚠️ Disclaimer

This project was developed for educational, research, and software engineering purposes.

Users are responsible for complying with the terms of service and applicable laws of any platform they choose to interact with. No guarantee of profit or betting success is implied.

---

# 👨‍💻 Author

**Chikwendu Emmanuel Onyedika (Ezee Kits )**

Electrical & Electronic Engineer | Python Developer | Automation Engineer | Machine Learning Enthusiast

---

# 🌐 Connect With Me

💼 **Portfolio:** https://ezee-kits-portfolio.onrender.com/

💻 **GitHub:** https://github.com/Ezee-Kits/

🔗 **LinkedIn:** https://www.linkedin.com/in/onyedika-emmanuel-chikwendu-987922280/

📺 **YouTube:** https://www.youtube.com/@EzeeKits

---

## ⭐ Support

If you found this project interesting, consider giving it a **Star ⭐** on GitHub.

It helps support the project and encourages future development.
