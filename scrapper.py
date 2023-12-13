import os
from parsel import Selector
import requests
import re
from markdownify import markdownify as md


def fetch_content(url, timeout=2):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except (requests.ReadTimeout, requests.HTTPError) as exc:
        print(exc)
        return False
    else:
        return response.text


def create_file_info(text_title, year):
    raw_title = re.match(r"<h2>(.*?)<\/h2>",
                         text_title).group(1).strip('-').strip()
    day = raw_title.split(':')[0].lower()
    return {'day': day.replace(" ", ""), 'title': raw_title, 'year': year}


def create_path(day, year):
    path = './' + year + '/' + day
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def create_md(file_title, file_content, url):
    path_to_md = create_path(file_title['day'], file_title['year'])
    md_file = open(path_to_md + '/' + file_title['title'] + '.md', "w+")
    md_text = md(file_content, strong_em_symbol="**")
    md_file.write(md_text + 'Source: ' + url)
    print("File ready. Check the question in " + file_title['title'] + ".md and happy coding!")


def fetch_challenge_text(url, year):
    challenge_text = fetch_content(url)
    if challenge_text != False:
        selector = Selector(challenge_text)
        main_text = selector.css("article.day-desc").get()
        text_title = selector.css("h2").get()
        challenge_title = create_file_info(text_title, year)
        return create_md(challenge_title, main_text, url)


def choose_day(year):
    choice = "Wrong"

    while choice.isdigit() == False:
        choice = input("Choose a day to fetch: ")

        if choice.isdigit() == False:
            print("Please write only numbers")
        else:
            return fetch_challenge_text('https://adventofcode.com/' + year + '/day/' + choice, year)


def choose_year():
    choice = "Wrong"

    while choice.isdigit() == False:
        choice = input("Choose an year to fetch: ")

        if choice.isdigit() == False:
            print("Please write only numbers: ")
        else:
            return choose_day(choice)


choose_year()
