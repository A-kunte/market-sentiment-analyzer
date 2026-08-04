# Real-Time Market Intelligence & Sentiment Analysis Pipeline

A production-ready data collection, processing, and sentiment analysis pipeline built for Indian stock market intelligence. This system monitors real-time discussions across major financial hashtags (`#nifty50`, `#sensex`, `#intraday`, `#banknifty`) to transform unstructured social data into quantitative trading signals without paid APIs.

---

## Project Overview & Key Results
* **Total Cleaned Records Processed**: 1,768 unique financial posts.
* **Target Indices Monitored**: Nifty50, Sensex, Intraday, and BankNifty.
* **Core Output**: Validated bullish market sentiment trend dominance with TF-IDF feature weighting and confidence intervals.

---

## Project Architecture & Workflow

1. **Data Collection (`scraper.py`)**: 
   - Uses Selenium via an existing authenticated Chrome remote debugging session to bypass anti-bot measures and rate limits without paid APIs.
   - Extracts metadata: username, timestamp, content, engagement metrics (likes, retweets, replies), mentions, and hashtags.

2. **Data Processing & Storage (`processor.py`)**:
   - Handles Unicode normalization for regional text content.
   - Implements strict deduplication mechanisms.
   - Stores data using compressed **Apache Parquet** storage schemas.

3. **NLP & Signal Generation (`analyzer.py`)**:
   - Converts textual data into numerical feature vectors using **TF-IDF Vectorization** (scikit-learn).
   - Implements custom financial lexicon weightings (*calls, puts, breakout, crash, support, resistance*).
   - Computes composite trading signals with confidence intervals.

4. **Memory-Efficient Visualization (`visualizer.py`)**:
   - Implements data-sampling techniques to handle large datasets efficiently.
   - Generates distribution charts saved under `/plots`.

---

## Project Structure

```text
market-intelligence-assignment/
│
├── scraper.py             # Selenium-based web scraper
├── processor.py           # Data cleaning, normalization, and deduplication engine
├── analyzer.py            # TF-IDF vectorization & sentiment trading signal generator
├── visualizer.py          # Low-memory data sampling and plotting script
├── requirements.txt       # Project dependencies
├── raw_tweets.parquet     # Raw collected dataset storage
├── cleaned_tweets.parquet # Cleaned & normalized dataset
├── market_signals.parquet # Processed signals with confidence intervals
└── plots/
    └── sentiment_distribution.png  # Visual intelligence summary chart