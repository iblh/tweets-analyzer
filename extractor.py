import os
import re
import csv
import json
import argparse
import pandas as pd


def extract_text(df, date, hour):
    """
    Extract text from a JSON file.
    param:
        df: pandas dataframe
        date: string, date of the dataset, format: YYYY-MM-DD
        hour: string, hour of the dataset, format: HH
    """
    df['clean_text'] = df['text'].str.replace(
        '[^A-Za-z0-9:.,!\'?@#$%&*()[\]+=\-_/<>]+', ' ', regex=True)
    df['clean_text'] = df['clean_text'].str.strip()
    df['clean_text'].to_csv('tweets/date={}/hour={}/text.txt'.format(
        date, hour), index=False, header=False, quoting=csv.QUOTE_ALL)


def extract_hashtags(df, date, hour):
    """
    Extract hashtags from a JSON file.
    param:
        df: pandas dataframe
        date: string, date of the dataset, format: YYYY-MM-DD
        hour: string, hour of the dataset, format: HH
    """
    hashtags = {}
    for tweet in df['text']:
        for word in tweet.split():
            if word.startswith('#') and len(word) > 1:
                if word in hashtags:
                    hashtags[word] += 1
                else:
                    hashtags[word] = 1

    # sort hashtags by frequency
    hashtags = {k: v for k, v in sorted(
        hashtags.items(), key=lambda item: item[1], reverse=True)}

    # save hashtags to a file
    with open('tweets/date={}/hour={}/hashtags_count.txt'.format(date, hour), 'w', encoding='utf-8') as f:
        for hashtag, count in hashtags.items():
            f.write('{} {}\n'.format(hashtag, count))


def extract_username(df, date, hour):
    """
    Extract usernames from a JSON file.
    param:
        df: pandas dataframe
        date: string, date of the dataset, format: YYYY-MM-DD
        hour: string, hour of the dataset, format: HH
    """
    usernames = {}
    for tweet in df['text']:
        for word in tweet.split():
            if word.startswith('@') and len(word) > 1:
                # username can only contain alphanumeric characters and underscores
                word = re.sub(r'[^A-Za-z0-9_]+', '', word)
                word = '@' + word
                if word in usernames:
                    usernames[word] += 1
                else:
                    usernames[word] = 1

    # sort usernames by frequency
    usernames = {k: v for k, v in sorted(
        usernames.items(), key=lambda item: item[1], reverse=True)}

    # save usernames to a file
    with open('tweets/date={}/hour={}/username_count.txt'.format(date, hour), 'w', encoding='utf-8') as f:
        for username, count in usernames.items():
            f.write('{} {}\n'.format(username, count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=str, required=True,
                        help='date of input file, format: YYYY-MM-DD')
    parser.add_argument('--hour', type=str, required=True,
                        help='hour of input file, format: HH')
    args = parser.parse_args()

    # check if file exists
    file_path = 'tweets/date={}/hour={}/tweets.txt'.format(
        args.date, args.hour)
    if os.path.exists(file_path):
        df = pd.read_json(file_path)
    else:
        print('File not found')
        raise SystemExit

    extract_text(df, args.date, args.hour)
    print('Text extracted')
    extract_hashtags(df, args.date, args.hour)
    print('Hashtags extracted')
    extract_username(df, args.date, args.hour)
    print('Usernames extracted')
