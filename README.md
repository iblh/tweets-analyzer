# Tweets-Analyzer

## Usage

### downloader.py

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
