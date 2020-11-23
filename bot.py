import tweepy
import random
import logging
import os
import time
from tmdbv3api import TMDb


API_KEY = "mP1ZhioSbyqbH2OVbklTeYgMU"
API_SECRET_KEY = "nRGSVhkJB3354j7keYWIXwxHkzUuXClcyryoFiUjgMRqG8VQbv"
ACESS_TOKEN = "1329462339335286791-NJy91VEAWF1KA1jFGzCl9e5jr8Kmqo"
ACESS_SECRET = "0PPyFuN1W658NV5aBrusNnrGtN5NoYMCMviaIFsl0r093"
TMDB_API = 'e05c25740e933e2f20eb86f8d923157f'


def autent():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACESS_TOKEN, ACESS_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    tmdb = TMDb()
    tmdb.api_key = TMDB_API

    return api


def check_mentions(api, since_id):
    print("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue

        search_movie_title = tweet.text.split(' ', 1)[1]
        print(search_movie_title)
        movie_title, movie_rating = search_movie(search_movie_title)

        print(f"Answering to {tweet.user.name}")
        status = "@" + tweet.user.name + " Pesquisa: " + search_movie_title + "\n" + \
            "Encontrado: " + movie_title + "\n" + \
            "Score: " + str(movie_rating) + "/10 \n"
        api.update_status(status, in_reply_to_status_id=tweet.id,
                          auto_populate_reply_metadata=True)

    return new_since_id


def search_movie(movie_title):
    from tmdbv3api import Movie
    movie = Movie()
    search = movie.search(movie_title)
    first_result = search[0]

    print(first_result.title)
    print(first_result.vote_average)

    return first_result.title, first_result.vote_average


def main():
    api_m = autent()
    since_id = 1
    while True:
        since_id = check_mentions(api_m, since_id)
        print("Waiting...")
        time.sleep(30)


if __name__ == "__main__":
    main()
