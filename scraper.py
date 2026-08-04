import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

class TwitterScraper:
    def __init__(self):
        options = Options()
        # Connect to the already-open Chrome browser session where you are logged in
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        
        self.driver = webdriver.Chrome(options=options)
        self.tweets_data = []

    def scroll_and_extract(self, hashtag, target_count=500):
        search_url = f"https://twitter.com/search?q=%23{hashtag}&f=live"
        print(f"[*] Navigating to search: {search_url}")
        self.driver.get(search_url)
        time.sleep(5)  # Initial load wait

        collected_ids = set()
        scroll_attempts = 0
        max_scroll_attempts = 400  # Allow enough attempts to reach target

        while len(collected_ids) < target_count and scroll_attempts < max_scroll_attempts:
            articles = self.driver.find_elements(By.TAG_NAME, "article")
            
            for article in articles:
                try:
                    user_elem = article.find_element(By.XPATH, './/div[@data-testid="User-Name"]')
                    username = user_elem.text.split("\n")[1] if len(user_elem.text.split("\n")) > 1 else "Unknown"
                    
                    time_elem = article.find_element(By.XPATH, './/time')
                    timestamp = time_elem.get_attribute("datetime")
                    
                    content_elem = article.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                    content = content_elem.text
                    
                    tweet_id = f"{username}_{timestamp}"
                    if tweet_id in collected_ids:
                        continue
                    collected_ids.add(tweet_id)

                    metrics = {"reply": 0, "retweet": 0, "like": 0}
                    for metric_type in ["reply", "retweet", "like"]:
                        try:
                            elem = article.find_element(By.XPATH, f'.//div[@data-testid="{metric_type}"]')
                            val_text = elem.get_attribute("aria-label") or "0"
                            numbers = re.findall(r'\d+', val_text)
                            if numbers:
                                metrics[metric_type] = int(numbers[0])
                        except:
                            pass

                    mentions = re.findall(r'@\w+', content)
                    hashtags = re.findall(r'#\w+', content)

                    self.tweets_data.append({
                        "username": username,
                        "timestamp": timestamp,
                        "content": content,
                        "replies": metrics["reply"],
                        "retweets": metrics["retweet"],
                        "likes": metrics["like"],
                        "mentions": mentions,
                        "hashtags": hashtags,
                        "query_tag": hashtag
                    })
                except Exception:
                    continue

            # Smooth incremental scrolling to trigger Twitter's lazy loader
            self.driver.execute_script("window.scrollBy(0, 1200);")
            time.sleep(random.uniform(2.0, 3.5))
            
            scroll_attempts += 1
            print(f"[+] Progress: Collected {len(collected_ids)}/{target_count} unique tweets for #{hashtag}...")

            if len(collected_ids) >= target_count:
                print(f"[+] Target reached for #{hashtag}!")
                break

    def close(self):
        pass

if __name__ == "__main__":
    hashtags = ["nifty50", "sensex", "intraday", "banknifty"]
    scraper = TwitterScraper()
    try:
        for tag in hashtags:
            scraper.scroll_and_extract(tag, target_count=500)  # 500 per tag = 2,000 total
        
        if len(scraper.tweets_data) > 0:
            df = pd.DataFrame(scraper.tweets_data)
            df.to_parquet("raw_tweets.parquet", index=False)
            print(f"[SUCCESS] Saved {len(df)} total tweets to raw_tweets.parquet!")
        else:
            print("[!] Warning: 0 tweets were collected.")
    finally:
        pass