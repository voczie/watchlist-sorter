import bs4
import requests
import json

def transform_page_to_soup(username, second_part_link = ""):
    page = requests.get(f"https://letterboxd.com/{username}/watchlist/{second_part_link}/")
    soup = bs4.BeautifulSoup(page.text, "html5lib")
    return soup

def get_total_number_of_pages(username):
    soup = transform_page_to_soup(username)
    paginas = soup.find_all("li", class_="paginate-page")

    if len(paginas) == 0:
        return 1
    else:
        return paginas[-1].text
    
def get_movies_from_soup(soup):
    names = []
    links = []

    movies = soup.find_all("li", attrs={"class": "poster-container"})

    for movie in movies:
        names.append(movie.find("img").attrs["alt"])
        links.append(movie.find("div").attrs["data-target-link"])

    return names, links
        

def get_watchlist_csv(username):
    number_pages = int(get_total_number_of_pages(username))
    movies_dict = {}
    movie_index = 0

    for i in range(1, number_pages + 1):
        soup = transform_page_to_soup(username, f"/page/{i}")
        names, links = get_movies_from_soup(soup)
        for j in range(0, len(names)):
            movies_dict.update({movie_index:{"title": names[j], "link" : links[j]}})
            movie_index += 1
    
    movies_dict.update({"size_of_list":(movie_index - 1)})

    save_list(username, movies_dict)

def save_list(username, movies_dict):
    movies_json = json.dumps(movies_dict, indent=4, ensure_ascii=False)

    with open(f"watchlists/{username}.json", 'w', encoding='utf-8') as fp:
        fp.write(movies_json)