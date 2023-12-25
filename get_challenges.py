import os
from parsel import Selector
import requests
import re
from markdownify import markdownify as md


def define_session_get(session, url, cookie, timeout=2):
    if bool(cookie) != False:
        return {"question_text": session.get(url, timeout=timeout), "question_input": session.get(url + '/input',
                                                                                                  cookies={'session': cookie})}
    return {"question_text": session.get(url,
                                         timeout=timeout), "question_input": None}


def fetch_content(url, cookie, timeout=2):
    try:
        session = requests.Session()
        response = define_session_get(session, url, cookie, timeout)
        response["question_text"].raise_for_status()
    except (requests.ReadTimeout, requests.HTTPError) as exc:
        print(exc)
        return False
    else:
        return response


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


def create_md(file_title, file_content, url, question_input):
    path_to_md = create_path(file_title['day'], file_title['year'])
    md_file = open(path_to_md + '/' + file_title['title'] + '.md', "w+")
    md_text = md(file_content, strong_em_symbol="**")
    md_file.write(md_text + 'Source: ' + url)
    if question_input != None:
        input_file = open(path_to_md + '/' + "input.txt", "w+")
        input_file.write(question_input.text)
    print("File ready. Now, go to " + path_to_md + " and happy coding!")


def fetch_challenge_text(url, year, cookie):
    challenge_text = fetch_content(url, cookie)
    if challenge_text != False:
        selector = Selector(challenge_text["question_text"].text)
        main_text = selector.css("article.day-desc").get()
        text_title = selector.css("h2").get()
        challenge_title = create_file_info(text_title, year)
        return create_md(challenge_title, main_text, url, challenge_text["question_input"])


def insert_cookie(chosen_day, year):
    session_cookie = input(
        "Do you want to fetch input? please insert your session cookie - go to adventofcode.com and copy your 'session' cookie value (press enter if you don't want) ")
    return fetch_challenge_text('https://adventofcode.com/' + year + '/day/' + chosen_day, year, session_cookie.strip())


def choose_day(year):
    chosen_day = "Wrong"
    while chosen_day.isdigit() == False:
        chosen_day = input("Choose a day to fetch: ")

        if chosen_day.isdigit() == False:
            print("Please write only numbers: ")
        else:
            return insert_cookie(chosen_day, year)


def choose_year():
    choice = "Wrong"

    while choice.isdigit() == False:
        choice = input("Choose an year to fetch: ")

        if choice.isdigit() == False:
            print("Please write only numbers: ")
        else:
            return choose_day(choice)


choose_year()
