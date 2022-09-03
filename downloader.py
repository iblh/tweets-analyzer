import os
import json
import requests
import argparse
from tqdm import tqdm
from datetime import datetime, timedelta

# credentials
import config
API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
BEARER_TOKEN = config.BEARER_TOKEN


def get_end_time(start_time):
    """
    param: start_time: string, format: YYYY-MM-DDTHH:MM:SSZ
    return: end_time: string, format: YYYY-MM-DDTHH:MM:SSZ
    """
    start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.000Z')
    end_time = start_time + timedelta(hours=1)
    return end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')


def get_tweets_v2(start_time, end_time, max_results, query_type):
    """
    param: 
        start_time: string, format: YYYY-MM-DDTHH:MM:SSZ
        end_time: string, format: YYYY-MM-DDTHH:MM:SSZ
        max_results: int, max number of tweets to return
        query_type: string, 'user' or 'keyword'
    return:
        tweets: list of tweets
    """
    headers = {'Authorization': 'Bearer {}'.format(BEARER_TOKEN)}

    if query_type == 'user':
        userlist = input('Enter a list of username, separated by commas:')
        userlist = userlist.split(',')
        results = []
        for user in userlist:
            # find tweets by user
            url = 'https://api.twitter.com/2/tweets/search/recent?query=from%3A{}&start_time={}&end_time={}&max_results={}&tweet.fields=author_id,created_at,text'.format(
                user, start_time, end_time, max_results)
            response = requests.request('GET', url, headers=headers)

            if response.json()['meta']['result_count'] > 0:
                results.extend(response.json()['data'])
        return results
    elif query_type == 'keyword':
        keyword = input('Enter a keyword:')
        if max_results <= 100:
            url = 'https://api.twitter.com/2/tweets/search/recent?query={}&start_time={}&end_time={}&max_results={}&tweet.fields=author_id,created_at,text'.format(
                keyword, start_time, end_time, max_results)
            response = requests.request('GET', url, headers=headers)

            if 'data' in response.json():
                return response.json()['data']
            else:
                return []
        else:
            # if max_results > 100, we need to loop through the pages
            results = []
            url = 'https://api.twitter.com/2/tweets/search/recent?query={}&start_time={}&end_time={}&max_results=100&tweet.fields=author_id,created_at,text'.format(
                keyword, start_time, end_time)
            response = requests.request('GET', url, headers=headers)
            if 'data' in response.json():
                results.extend(response.json()['data'])

            # check if there are more pages
            if 'next_token' in response.json()['meta']:
                next_token = response.json()['meta']['next_token']
            else:
                next_token = None

            # pagination
            with tqdm(total=max_results) as pbar:
                while next_token and len(results) < max_results:
                    url = 'https://api.twitter.com/2/tweets/search/recent?query={}&start_time={}&end_time={}&max_results=100&tweet.fields=author_id,created_at,text&next_token={}'.format(
                        keyword, start_time, end_time, next_token)
                    response = requests.request('GET', url, headers=headers)

                    if 'data' in response.json():
                        results.extend(response.json()['data'])

                    # check if there are more pages
                    if 'meta' in response.json() and 'next_token' in response.json()['meta']:
                        next_token = response.json()['meta']['next_token']
                    else:
                        print('No more tweets')
                        next_token = None
                    pbar.update(100)

            return results


def export2file(tweets, folder):
    """
    param:
        tweets: list of tweets
        folder: string, folder to save the tweets
    """
    if not os.path.exists(folder):
        # create folder if not exist
        os.makedirs(folder)
        # save tweets to a file
        with open('{}/tweets.txt'.format(folder), 'w') as f:
            json.dump(tweets, f)
    else:
        if os.path.exists('{}/tweets.txt'.format(folder)):
            # append to existing file
            with open('{}/tweets.txt'.format(folder), 'r') as f:
                old_tweets = json.load(f)
            old_tweets.extend(tweets)
            with open('{}/tweets.txt'.format(folder), 'w') as f:
                json.dump(old_tweets, f)
        else:
            # save tweets to a file
            with open('{}/tweets.txt'.format(folder), 'w') as f:
                json.dump(tweets, f)


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--query-type', help='query type',
                        choices=['keyword', 'user'], required=True)
    parser.add_argument(
        '--date', help='start date, format: YYYY-MM-DD', required=True, type=str)
    parser.add_argument(
        '--hour', help='start hour, format: HH', type=int, required=True)
    parser.add_argument('--max-results', help='max results',
                        required=True, type=int)

    # initialize variables
    args = parser.parse_args()
    start_time = '{}T{:02d}:00:00.000Z'.format(args.date, args.hour)
    end_time = get_end_time(start_time)

    # get tweets from start date to end date
    tweets = get_tweets_v2(start_time, end_time,
                           args.max_results, args.query_type)

    folder = 'tweets/date={}/hour={}'.format(args.date, args.hour)
    export2file(tweets, folder)
