import os
import time
import pandas as pd
from pymongo import MongoClient

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from product_matcher import validate_video




# ---------------------------
# MongoDB
# ---------------------------

client = MongoClient("mongodb://localhost:27017")
db = client["creator_intelligence"]



def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=options)


# ---------------------------
# RAW RECORD STRUCTURE
# ---------------------------

def build_record(brand, product_name, title, url,
                 publish_date, view_count,
                 creator_name, creator_url):

    return {
        "Creator Name": creator_name,
        "Creator Profile URL": creator_url,
        "Platform": "YouTube",
        "Video Title": title,
        "Video URL": url,
        "Publish Date": publish_date,
        "View Count": view_count,
        "Product Mentioned": product_name,
        "Brand Mentioned": brand,
        "Evidence Snippet": title
    }


# ---------------------------
# CRAWLER
# ---------------------------

def crawl_youtube(driver, brand, product_name, limit=50):

    query = f"{brand} {product_name} review"
    url = f"https://www.youtube.com/results?search_query={query.replace(' ','+')}"

    try:
        driver.get(url)
    except WebDriverException as e:
        print("❌ Driver crashed on initial load:", e)
        return []

    time.sleep(5)

    videos = []
    seen_urls = set()

    while len(videos) < limit:

        try:
            driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);"
            )
            time.sleep(2)

            cards = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")

        except WebDriverException as e:
            print("❌ Driver lost during scroll:", e)
            break

        for card in cards:

            try:
                title_el = card.find_element(By.CSS_SELECTOR, "a#video-title")

                title = title_el.get_attribute("title") or ""
                video_url = title_el.get_attribute("href")

                if not video_url or video_url in seen_urls:
                    continue

                # basic product filter (fast pre-filter)
                if product_name.lower() not in title.lower():
                    continue

                view_count = ""
                publish_date = ""

                meta = card.find_elements(By.CSS_SELECTOR, "#metadata-line span")

                if len(meta) >= 1:
                    view_count = meta[0].text
                if len(meta) >= 2:
                    publish_date = meta[1].text

                try:
                    creator_el = card.find_element(
                        By.XPATH,
                        ".//div[@id='channel-info']//a"
                    )
                    creator_name = creator_el.text.strip()
                    creator_url = creator_el.get_attribute("href")

                except:
                    creator_name = ""
                    creator_url = ""

                videos.append(
                    build_record(
                        brand,
                        product_name,
                        title,
                        video_url,
                        publish_date,
                        view_count,
                        creator_name,
                        creator_url
                    )
                )

                seen_urls.add(video_url)

            except Exception:
                continue

        print(f"{product_name}: {len(videos)} videos collected")

        if len(cards) > 200:
            break

    return videos[:limit]


# ---------------------------
# MAIN PIPELINE
# ---------------------------

products = list(db.products.find({"status": 1}))

base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "extracted_data")
os.makedirs(output_dir, exist_ok=True)


writer = pd.ExcelWriter("extracted_data/creator_reviews_raw_data.xlsx", engine="openpyxl")
validated_writer = pd.ExcelWriter("extracted_data/creator_reviews_filtered_data.xlsx", engine="openpyxl")

driver = get_driver()

for product in products:

    brand = product["brand"]
    product_name = product["product"]

    print(f"\n🚀 Processing {brand} {product_name}")

    try:
        data = crawl_youtube(driver, brand, product_name, limit=50)

        if not data:
            print("⚠️ No data found")
            continue

        raw_df = pd.DataFrame(data)
        raw_df.to_excel(writer, sheet_name=product_name[:31], index=False)

        # ---------------------------
        # VALIDATION LAYER
        # ---------------------------

        validation_results = raw_df["Video Title"].apply(
            lambda x: validate_video(x, product_name)
        ).apply(pd.Series)

        filtered_df = pd.concat([raw_df, validation_results], axis=1)

        filtered_df = filtered_df[filtered_df["is_match"] == True]

        filtered_df.drop(columns=["is_match"], inplace=True)

        filtered_df.to_excel(
            validated_writer,
            sheet_name=product_name[:31],
            index=False
        )

    except Exception as e:
        print(f"❌ Error processing {product_name}: {e}")
        continue

# ---------------------------
# CLEAN EXIT
# ---------------------------

writer.close()
validated_writer.close()

try:
    driver.quit()
except:
    pass

print("\n✅ Pipeline completed")