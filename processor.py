import pandas as pd
import re
import unicodedata
import os

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # Normalize Unicode characters (handles regional Indian text/special symbols properly)
    text = unicodedata.normalize('NFKD', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', flags=re.MULTILINE, string=text)
    
    # Remove excessive whitespaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def process_pipeline(input_path="raw_tweets.parquet", output_path="cleaned_tweets.parquet"):
    print("[*] Loading raw data from Parquet...")
    
    if not os.path.exists(input_path):
        print(f"[!] Error: {input_path} does not exist. Please run scraper.py first.")
        return

    try:
        df = pd.read_parquet(input_path)
    except Exception as e:
        print(f"[!] Error reading parquet file: {e}")
        return

    print(f"[*] Columns found in raw data: {list(df.columns)}")
    initial_count = len(df)
    print(f"[*] Initial row count: {initial_count}")

    if initial_count == 0 or "content" not in df.columns:
        print("[!] Warning: The raw data file is empty or missing the 'content' column.")
        print("[!] This usually means the scraper didn't collect any tweets. Please check your browser window or re-run scraper.py.")
        return

    # 1. Implement data deduplication mechanisms
    df.drop_duplicates(subset=["username", "content"], keep="first", inplace=True)
    
    # 2. Drop missing or empty contents
    df = df.dropna(subset=["content"])
    df = df[df["content"].str.strip() != ""]

    # 3. Clean and normalize text data
    print("[*] Cleaning text data and handling Unicode characters...")
    df["cleaned_content"] = df["content"].apply(clean_text)

    # 4. Standardize timestamps for time-series analysis
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    # 5. Compute basic quantitative engagement metrics for market trading signals
    df["engagement_score"] = df["likes"] + (df["retweets"] * 2) + (df["replies"] * 1.5)

    final_count = len(df)
    print(f"[+] Processing complete. Cleaned rows: {final_count} (Removed {initial_count - final_count} duplicates/invalid entries).")

    # Save into optimized Parquet format storage schema
    df.to_parquet(output_path, index=False)
    print(f"[SUCCESS] Cleaned data securely saved to {output_path}!")

if __name__ == "__main__":
    process_pipeline()