import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def analyze_signals_with_tfidf(input_path="cleaned_tweets.parquet", output_path="market_signals.parquet"):
    print("[*] Loading cleaned data for advanced signal generation...")
    try:
        df = pd.read_parquet(input_path)
    except FileNotFoundError:
        print(f"[!] Error: {input_path} not found.")
        return

    # 1. TF-IDF Text-to-Signal Conversion (Task 4 requirement)
    print("[*] Computing TF-IDF numerical feature vectors...")
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(df["cleaned_content"])
    
    # Compute keyword significance score from TF-IDF mean intensity per tweet
    df["tfidf_score"] = np.asarray(tfidf_matrix.mean(axis=1)).ravel()

    # 2. Custom Financial Lexicon Rules mapped to numerical vectors
    bullish_terms = ['bullish', 'call', 'calls', 'breakout', 'rally', 'moon', 'profit', 'buy', 'support', 'upside', 'growth', 'pump', 'long', 'target']
    bearish_terms = ['bearish', 'put', 'puts', 'crash', 'dump', 'slump', 'loss', 'sell', 'resistance', 'downside', 'fall', 'risk', 'short', 'panic']

    def compute_sentiment_and_confidence(text):
        t_lower = text.lower()
        bull_hits = sum(1 for w in bullish_terms if w in t_lower)
        bear_hits = sum(1 for w in bearish_terms if w in t_lower)
        
        if bull_hits > bear_hits:
            return "Bullish", 0.75 + min(0.2, bull_hits * 0.05)
        elif bear_hits > bull_hits:
            return "Bearish", 0.75 + min(0.2, bear_hits * 0.05)
        else:
            return "Neutral", 0.50

    print("[*] Generating composite signals and confidence intervals...")
    res = df["cleaned_content"].apply(compute_sentiment_and_confidence)
    df["sentiment"] = [r[0] for r in res]
    df["confidence_interval"] = [r[1] for r in res]

    # Compute composite trading score combining TF-IDF weight and engagement metrics
    df["composite_signal"] = df.apply(
        lambda row: (1 if row["sentiment"] == "Bullish" else (-1 if row["sentiment"] == "Bearish" else 0)) 
                    * (row["engagement_score"] + 1) * (1 + row["tfidf_score"]),
        axis=1
    )

    # 3. Aggregate by Query Tag for Summary Report
    summary = df.groupby("query_tag").agg(
        total_mentions=("content", "count"),
        avg_engagement=("engagement_score", "mean"),
        mean_confidence=("confidence_interval", "mean"),
        bullish_share=("sentiment", lambda x: (x == "Bullish").mean() * 100),
        bearish_share=("sentiment", lambda x: (x == "Bearish").mean() * 100)
    ).reset_index()

    summary["market_outlook"] = summary.apply(
        lambda r: "BULLISH 🟢" if r["bullish_share"] > r["bearish_share"] else "BEARISH 🔴",
        axis=1
    )

    print("\n" + "="*70)
    print("ADVANCED MARKET INTELLIGENCE & SIGNAL SUMMARY")
    print("="*70)
    print(summary.to_string(index=False))
    print("="*70 + "\n")

    df.to_parquet(output_path, index=False)
    summary.to_csv("market_signal_summary.csv", index=False)
    print(f"[SUCCESS] Advanced feature vectors and signals saved to {output_path}")

if __name__ == "__main__":
    analyze_signals_with_tfidf()