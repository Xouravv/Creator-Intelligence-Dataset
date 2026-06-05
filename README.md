# Creator Intelligence Pipeline

A scalable data pipeline that crawls YouTube review videos for products, validates product relevance using rule-based matching logic, and stores both raw and filtered datasets for analysis.

---

## Features

- MongoDB-driven product queue system  
- YouTube video crawling using Selenium  
- Product-level review validation logic  
- Confidence scoring for match quality  
- Raw and filtered dataset generation  
- Duplicate handling at video URL level  

---

## Project Structure

```
project/
├── main_crawling.py
├── product_matcher.py
├── db/
├── extracted_data/
├── requirements.txt
└── README.md
```

---

## Setup

### Clone Repo
```bash
git clone <repo-url>
cd project
```

### Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## MongoDB (Docker)

```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest
```

```bash
run db/config.py    ------------> create db
run db/create_product.py  ------> add demo products
run fetch_products.py ----------> to check if product added sucessfully

```





Connection:
```
mongodb://localhost:27017
```

---

## Run Pipeline

```bash
python3 main_crawling.py
```

---

## Output

### Raw Data
- extracted_data/creator_reviews_raw_data.xlsx

### Filtered Data
- extracted_data/creator_reviews_filtered_data.xlsx

---

## Validation Logic

Each video is evaluated using:
- Product name matching
- Review intent detection
- Brand + product relevance
- Confidence scoring

Outputs:
- is_match
- confidence_score
- validation_logic
- assumptions

---

## Requirements

pandas  
pymongo  
selenium  
openpyxl  

---

## Notes

- Ensure ChromeDriver is installed
- Selenium runs in headless mode
- MongoDB must be running before execution




## 🌐 Platform Coverage

### Implemented: YouTube (Fully Functional)

The current system fully supports:
- YouTube video search crawling
- Creator extraction
- Video metadata extraction
- Product-level validation
- Structured dataset generation

YouTube was chosen due to:
- Stable DOM structure for scraping
- High availability of review content
- Rich metadata (views, date, channel info)

---

## 🚀 Extension to Other Platforms

The architecture is designed to be **platform-agnostic**, where each platform implements a common interface:



---

### 📸 Instagram Extension (Planned)

Instagram integration would require:
- Hashtag-based search (#productname, #review)
- Creator reel/post extraction
- GraphQL or scraping-based data access
- Authentication handling (optional via cookies/session)

Key challenges:
- Heavy anti-scraping protection
- Login requirement for full data access

---

### 🎵 TikTok Extension (Planned)

TikTok integration would include:
- Keyword-based video search
- Creator video feed extraction
- Caption-based product matching

Key challenges:
- Dynamic rendering (JS-heavy)
- Rate limiting and bot detection
- API restrictions

---

## 🧱 Scalable Architecture Design

To support multiple platforms, the system can be refactored into:

```

Platform Interface Layer
↓
Platform Adapters (YouTube / Instagram / TikTok)
↓
Unified Data Schema Layer
↓
Validation & Scoring Engine
↓
Storage Layer (MongoDB / Data Lake)
