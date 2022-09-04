# Tweets-Analyzer

## Tweets Dataset

This repository include three datasets under `tweets` folder, each of them is a txt file.

- `date=2022-08-29/hour=20/tweets.txt`: contains 51,676 tweets
- `date=2022-09-01/hour=10/tweets.txt`: contains 50,033 tweets
- `date=2022-09-02/hour=10/tweets.txt`: contains 889 tweets

### Sample format of tweets.txt

```json
[
    {
        "id": "1565655773933457408",
        "author_id": "1510724946657517580",
        "text": "RT @dos_xyz: Hello Solana, We are pleased to announce our Hackathon Submission: DreamOS \ud83d\udcab\n\nA new user experience for crypto - it is the fir\u2026",
        "created_at": "2022-09-02T10:59:59.000Z"
    },
    {
        "id": "1565655773488812033",
        "author_id": "70647170",
        "text": "RT @joshtokitaaaaa: HELLO P-POP KINGS!! \ud83d\udc51\n\n@SB19Official #SB19\n#WYAT #WhereYouAtSB19 https://t.co/ZoXd2Ihhgi",
        "created_at": "2022-09-02T10:59:59.000Z"
    }
]
```

## Usage

### downloader.py

Download tweets from Twitter API and save them to local files (`tweets/date=YYYY-MM-DD/hour=HH/tweets.txt`).

```bash
python downloader.py -h
usage: downloader.py [-h] --query-type {keyword,user} --date DATE --hour HOUR --max-results MAX_RESULTS

## Example
# Download tweets use 'keyword' query type
python downloader.py --query-type keyword  --date 2022-08-30 --hour 10 --max-results 200
> keyword: hello

# Download tweets use 'user' query type
python downloader.py --query-type user  --date 2022-08-29 --hour 20 --max-results 200
> username: nasa
```

### extractor.py

- Extract and clean text from `tweets.txt` and save them to `text.txt` files.
- Extract and count hashtags from `tweets.txt` and save them to `hashtags_count.txt` files.
- Extract and count mentioned username from `tweets.txt` and save them to `username_count.txt` files.

```bash
python extractor.py -h
usage: extractor.py [-h] --date DATE --hour HOUR

python extractor.py --date 2022-09-01 --hour 10
```
