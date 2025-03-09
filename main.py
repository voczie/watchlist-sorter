import os
import random
import json
from scraper import get_watchlist_csv

welcoming_msg = '''===========================================
Welcome to the Letteboxd Watchlist Sorter!!'''

def load_list(username):
    with open(f"watchlists/{username}.json", mode='r', encoding='utf-8') as fp:
        movies_list = json.load(fp)
    return movies_list

def sort_movie(username):
    movies_list = load_list(username)

    max = movies_list["size_of_list"]
    index = str(random.randrange(0, max))

    title = movies_list[index].get("title")
    second_part_link = movies_list[index].get("link")

    return title, second_part_link

def menu():
    print(welcoming_msg)
    username = input("Please insert your username in Letterboxd: ")

    if f"{username}.json" in os.listdir("watchlists"):
        print("\nList for this user already generated. Let's sort some movie for you to see!")
    else:
        print("\nThere's no list for this user, yet. Generating list...")
        try:
            get_watchlist_csv(username)
        except:
            print("Error, check log")

        print("List generated for this user! Let's sort some movie for you to see!")
    
    title, second_part_link = sort_movie(username)

    print(f"\nThe selected movie was {title}!")
    print(f"Here it's Letterboxd URL: https://letterboxd.com{second_part_link}")



if __name__ == '__main__':
    menu()