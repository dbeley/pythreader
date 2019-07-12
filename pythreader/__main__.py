import logging
import configparser
import datetime
import argparse
import tweepy
import os
import urllib.request
from .imgviewer import show_image


logger = logging.getLogger()
config = configparser.ConfigParser()
config.read("config.ini")
BEGIN_TIME = datetime.datetime.now()
ROWS, COLUMNS = os.popen("stty size", "r").read().split()


def get_thread(twitter, url):
    status = twitter.get_status(url.split("/")[-1], tweet_mode="extended")
    userid = status.author.id
    yield status

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
                yield status
                found = True
        if not found:
            break


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

    if not args.url:
        logger.error("Use the -u flag to specify an url. Exiting.")
        exit()
    else:
        url = args.url

    for status in get_thread(twitter, url):
        print(f"{'-' * int(COLUMNS)}")
        # Display images if available
        if hasattr(status, "extended_entities"):
            if "media" in status.extended_entities:
                for media in status.extended_entities["media"]:
                    urllib.request.urlretrieve(
                        media["media_url"], "/tmp/image.png"
                    )
                    show_image("/tmp/image.png")

        print(status.full_text)


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
