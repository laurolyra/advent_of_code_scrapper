## Scrapper for Advent of code's challenges

### What's been done here
This project consists in a interactive scrapper to [advent of code's](https://adventofcode.com/) daily challenges, taking its text and saving into an .md file.

### Setup
1. Clone this repo
2. Create an virtual enviroment with `python3 -m venv .venv && source .venv/bin/activate`
3. Install packages with `pip install -r requirements.txt`
4. Run `python get_challenges.py`

### TL;DR
1. Setup as above;
2. Type the desired year and hit enter;
3. Type the desired day and hit enter.


### How does it work?
After setuping, you will be asked to type the corresponding year and day that you'd like to fetch - please note that these setup accepts only integers as input.

Then, this script will try to fetch the challenge for that day using `requests` library. If there aren't challenges for that day or that year or any other HTTP exception, or either a timeout, this script will print the error and return `False` (I think that was a better option than trying to validate every input).

If the response is successfull, the script, using `Selector` from `parsel` library, will obtain the main text and the title of the challenge, wich will be useful to create some file info and path to create the Markdown file.

By default, MDs are generated on the following directory: `./[year]/day[day]/[challenge-title].md`, like the one included on this repo - which is created when it is executed without overwritting existing files/direcrories if any.

### Possible improvements
- Test coverage;
- A third option that allows user to select a programming language and, after fetching and creating the directories, create an empty file like `solution.js` or `solution.py`;
- Different file name or directory structure.