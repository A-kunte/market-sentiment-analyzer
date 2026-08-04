# Real-Time Market Intelligence & Sentiment Analysis Pipeline

A production-ready data collection, processing, and sentiment analysis pipeline built for Indian stock market intelligence. This system monitors real-time discussions across major financial hashtags (`#nifty50`, `#sensex`, `#intraday`, `#banknifty`) to transform unstructured social data into quantitative trading signals without paid APIs.

---

## Project Overview & Key Results

* **Total Cleaned Records Processed:** 1,768 unique financial posts
* **Target Indices Monitored:** Nifty50, Sensex, Intraday, and BankNifty
* **Core Output:** Validated bullish market sentiment trend dominance with TF-IDF feature weighting and confidence intervals

---

## Project Architecture & Workflow

### 1. Data Collection (`scraper.py`)

* Uses Selenium via an existing authenticated Chrome remote debugging session to bypass anti-bot measures and rate limits without paid APIs.
* Extracts:

  * Username
  * Timestamp
  * Post content
  * Engagement metrics
  * Mentions
  * Hashtags

### 2. Data Processing & Storage (`processor.py`)

* Performs Unicode normalization for regional text content.
* Implements strict duplicate removal.
* Stores processed data using compressed Apache Parquet format.

### 3. NLP & Signal Generation (`analyzer.py`)

* Converts text into numerical feature vectors using TF-IDF Vectorization.
* Applies custom financial lexicon weighting for terms such as:

  * Calls
  * Puts
  * Breakout
  * Crash
  * Support
  * Resistance
* Computes composite trading signals with confidence intervals.

### 4. Memory-Efficient Visualization (`visualizer.py`)

* Uses sampling techniques for efficient visualization of large datasets.
* Generates consolidated sentiment distribution charts under the `plots/` directory.

---

## Project Structure

```text
.
├── scraper.py
├── processor.py
├── analyzer.py
├── visualizer.py
├── requirements.txt
├── TECHNICAL_DOCUMENTATION.md
├── cleaned_tweets.parquet
├── market_signals.parquet
└── plots/
    └── sentiment_distribution.png
```

| File                               | Description                                            |
| ---------------------------------- | ------------------------------------------------------ |
| `scraper.py`                       | Selenium-based web scraper                             |
| `processor.py`                     | Data cleaning, normalization, and deduplication engine |
| `analyzer.py`                      | TF-IDF vectorization and sentiment signal generation   |
| `visualizer.py`                    | Memory-efficient visualization module                  |
| `requirements.txt`                 | Python dependencies                                    |
| `TECHNICAL_DOCUMENTATION.md`       | Detailed technical documentation                       |
| `cleaned_tweets.parquet`           | Cleaned and normalized dataset                         |
| `market_signals.parquet`           | Trading signals with confidence intervals              |
| `plots/sentiment_distribution.png` | Sentiment visualization                                |

---

# Setup & Installation Instructions

## Prerequisites

* Python **3.8+**
* Google Chrome
* Git

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/A-kunte/market-sentiment-analyzer.git
cd market-sentiment-anaylzer
```

---

## Step 2: Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Complete Pipeline

Run each module sequentially.

---

## Step 1: Data Collection (`scraper.py`)

> **Note:** The scraper connects to an existing Chrome instance running in Remote Debugging mode to avoid anti-bot restrictions.

### 1. Close all Chrome windows.

### 2. Start Chrome with Remote Debugging.

#### Windows

```bash
start chrome --remote-debugging-port=9222 --user-data-dir="C:\selenium_chrome_profile"
```

#### macOS

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
--remote-debugging-port=9222 \
--user-data-dir="/tmp/chrome_profile"
```

### 3. Log into your Twitter/X account in the opened browser.

### 4. Run the scraper.

```bash
python scraper.py
```

---

## Step 2: Data Processing & Storage

Clean, normalize, deduplicate, and serialize the collected data.

```bash
python processor.py
```

---

## Step 3: NLP Analysis & Signal Generation

Generate TF-IDF feature vectors and compute trading signals.

```bash
python analyzer.py
```

---

## Step 4: Memory-Efficient Visualization

Generate sentiment distribution plots.

```bash
python visualizer.py
```

The generated visualization will automatically be saved inside the `plots/` directory.

---

# Pipeline Flow

```text
Twitter/X
    │
    ▼
scraper.py
    │
    ▼
processor.py
    │
    ▼
cleaned_tweets.parquet
    │
    ▼
analyzer.py
    │
    ▼
market_signals.parquet
    │
    ▼
visualizer.py
    │
    ▼
plots/sentiment_distribution.png
```

---

# Output Files

| Output                             | Description                          |
| ---------------------------------- | ------------------------------------ |
| `cleaned_tweets.parquet`           | Cleaned dataset after preprocessing  |
| `market_signals.parquet`           | Generated trading signals            |
| `plots/sentiment_distribution.png` | Sentiment distribution visualization |

---

# Technologies Used

* Python
* Selenium
* Pandas
* Apache Parquet
* Scikit-learn (TF-IDF)
* Matplotlib
* NumPy

---

# Notes

* Chrome must be launched in Remote Debugging mode before running the scraper.
* The scraper expects an authenticated Twitter/X session.
* Execute the modules in the order shown above for successful pipeline execution.
