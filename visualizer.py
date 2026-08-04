import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_charts(input_path="market_signals.parquet"):
    if not os.path.exists(input_path):
        print(f"[!] Error: {input_path} missing. Run analyzer.py first.")
        return

    print("[*] Loading data for memory-efficient visualization...")
    df = pd.read_parquet(input_path)

    # Low-memory sampling technique for large-scale charts
    if len(df) > 1000:
        plot_df = df.sample(n=1000, random_state=42)
    else:
        plot_df = df

    os.makedirs("plots", exist_ok=True)

    # Chart 1: Sentiment Distribution by Market Hashtag
    fig, ax = plt.subplots(figsize=(8, 5))
    sentiment_counts = pd.crosstab(plot_df["query_tag"], plot_df["sentiment"])
    sentiment_counts.plot(kind="bar", stacked=True, ax=ax, color=['#e74c3c', '#95a5a6', '#2ecc71'])
    ax.set_title("Real-Time Market Sentiment Distribution by Index", fontsize=12, fontweight='bold')
    ax.set_xlabel("Market Hashtag")
    ax.set_ylabel("Sampled Tweet Volume")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("plots/sentiment_distribution.png", dpi=300)
    plt.close()

    print("[SUCCESS] Low-memory chart successfully generated and saved to plots/sentiment_distribution.png")

if __name__ == "__main__":
    generate_charts()