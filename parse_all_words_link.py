import string

from tqdm import tqdm
from urllib.parse import urljoin

from parser import get_soup


BASE_URL = "https://dictionary.cambridge.org/"
HOME_URL = urljoin(BASE_URL, "browse/english/")
HEADERS = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}


def parse_links_to_word_group():
    for letter in tqdm(string.ascii_lowercase):

        soup = get_soup(urljoin(HOME_URL, letter), headers=HEADERS)
        links = [link.get("href") for link in soup.select("a.hlh32")]

        with open(f"letters/{letter}.txt", "w", encoding="utf-8") as file:
            for link in links:
                file.write(link + "\n")
    print("Word group was created")
    print("Done!")


def parse_links_to_word():

    for letter in tqdm(string.ascii_lowercase):
        with open(f"letters/{letter}.txt", "r", encoding="utf-8") as file:
            links = [link.strip() for link in file.readlines()]
            print(links)

        for link in tqdm(links):
            soup = get_soup(link, headers=HEADERS)
            links_to_words = [
                link.get("href") + "\n" for link in soup.select(".hlh32 > a")
            ]

            with open(f"Words_links/{letter}_links.txt", "a", encoding="utf-8") as file:
                file.writelines(links_to_words)
        print(f"{letter.capitalize()} was added")

    print("Done!")


def main():
    parse_links_to_word_group()
    parse_links_to_word()


if __name__ == "__main__":
    main()
