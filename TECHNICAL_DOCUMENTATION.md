# Technical Documentation: Real-Time Market Intelligence Pipeline

## 1. System Architecture & Approach
The system is built as a modular, four-stage data pipeline designed to ingest, clean, analyze, and visualize Indian stock market discussions from social media without relying on paid APIs.

## 2. Technical Component Breakdown
* **Data Extraction (`scraper.py`)**: Utilizes Selenium via an active Chrome remote debugging session. This bypasses anti-bot firewalls and rate limits natively while extracting metadata (timestamps, engagement counts, hashtags).
* **Data Cleansing & Storage (`processor.py`)**: Handles Unicode normalization for multi-lingual and special characters typical in regional social content. Implements strict composite deduplication (username + content hash checks) and serializes data into **Apache Parquet format** for columnar compression and high-speed I/O.
* **NLP & Signal Generation (`analyzer.py`)**: Transforms raw text into quantitative features using **TF-IDF Vectorization** (`scikit-learn`)[cite: 1]. Integrates a custom financial lexicon to score directional bias (*bullish/bearish*) and computes confidence intervals.
* **Memory-Efficient Visualization (`visualizer.py`)**: Implements data-sampling techniques to restrict in-memory footprint during heavy dataframe processing, rendering clean categorical distribution plots using Matplotlib[cite: 1].