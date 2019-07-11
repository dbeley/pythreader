import logging
import configparser
import datetime
import argparse
import tweepy
import os

logger = logging.getLogger()
config = configparser.ConfigParser()
config.read("config.ini")
BEGIN_TIME = datetime.datetime.now()
ROWS, COLUMNS = os.popen("stty size", "r").read().split()


def twitterconnect():
    consumer_key = config["twitter"]["consumer_key"]
    secret_key = config["twitter"]["secret_key"]
    access_token = config["twitter"]["access_token"]
    access_token_secret = config["twitter"]["access_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def main():
    args = parse_args()
    twitter = twitterconnect()
    list_status = []

    if not args.url:
        logger.error("Use the -u flag to specify an url. Exiting.")
        exit()
    else:
        url = args.url
    status = twitter.get_status(url.split("/")[-1], tweet_mode="extended")
    userid = status.author.id
    print(status.full_text)
    list_status.append(status)

    while True:
        found = False
        statusid = status.id
        curs = tweepy.Cursor(
            twitter.user_timeline,
            user_id=userid,
            since_id=statusid,
            tweet_mode="extended",
            count=100,
        ).items()
        for index, status in enumerate(curs, 0):
            if status.in_reply_to_status_id == statusid:
                print(f"{'-' * int(COLUMNS)}")
                print(status.full_text)
                found = True
                list_status.append(status)
        if not found:
            break


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bot posting images from lastfm_cg to twitter or mastodon."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument("-u", "--url", help="Tweet URL.", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
