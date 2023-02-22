import json
import random
import string
from urllib.parse import urljoin

import requests
import dataclasses
from bs4 import BeautifulSoup


def get_soup(url: str, headers: dict, *args, **kwargs) -> BeautifulSoup:
    page = requests.get(url, headers=headers, *args, **kwargs).text
    return BeautifulSoup(page, "html.parser")


@dataclasses.dataclass
class Word:
    word: str
    description: str
    type: str or None
    transcription: str or None
    synonyms: list or None

    def __dict__(self):
        return {
            "word": self.word,
            "description": self.description,
            "type": self.type,
            "transcription": self.transcription,
            "synonyms": self.synonyms,
        }

    def __eq__(self, other):
        return self.word == other.word


class WordParser:

    BASE_URL = "https://dictionary.cambridge.org/"
    DICTIONARY_URL = urljoin(BASE_URL, "dictionary/english/")
    HEADERS = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/109.0.0.0 Safari/537.36",
    }

    def __init__(self, word: str = None):
        if word:
            url = urljoin(self.DICTIONARY_URL, word.lower())
            self._letter = word[0].lower()
            self.word = self.validate_word_instance(self.parse_word_page(url))
        else:
            self._letter = self.get_random_letter()
            self.word = self.validate_word_instance(
                self.parse_word_page(self.get_link_to_random_word())
            )

    @staticmethod
    def get_random_letter() -> str:
        """returns random letter with english alphabet"""
        print("Random letter is:")
        print(result := random.choice(string.ascii_lowercase))

        return result

    def parse_word_page(self, link_to_word_page: str) -> Word or bool:
        """takes a link to the word page, collects data from it, returns instance of  Word"""

        soup = get_soup(urljoin(self.BASE_URL, link_to_word_page), headers=self.HEADERS)

        try:
            print(f"get information about {soup.select_one('.hw.dhw').text.title()}")

            word = Word(
                word=soup.select_one(".hw.dhw").text.title(),
                description=soup.select_one(".ddef_d").text.strip()[:-1].capitalize(),
                type=soup.select_one(".dpos").text.title(),
                transcription=None,
                synonyms=None,
            )
            try:
                word.transcription = (soup.select_one(".dpron").text,)
                word.synonyms = [
                    synonym.text for synonym in soup.select(".synonyms > .lcs > .item")
                ]
            except AttributeError:
                pass

            return word

        except AttributeError as e:
            print(e)
            return False

    def get_link_to_random_word(self):
        """retrieves one random word page link from the word group page"""
        with open(f"Words_links/{self._letter}_links.txt", encoding="utf-8") as file:
            links_to_words = [link.strip() for link in file.readlines()]

        print("New link is:")
        print(result := random.choice(links_to_words))

        return result

    def add_to_json(self):
        """added instance of Word to json file
        :file - name of file
        :word
        """

        word_obj = self.word

        with open(f"library/{self._letter}_word.json", "rt", encoding="utf-8") as file:
            ls = json.load(file)

        result = ls if isinstance(ls, list) else list(ls)
        words = [word["word"] for word in result]

        if word_obj.word in words:
            print(f"{word_obj.word} is already in library")
            return

        result.append(word_obj.__dict__())

        with open(f"library/{self._letter}_word.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=2)

        print(f"{word_obj.word} was added")

    def validate_word_instance(self, word: Word or bool) -> Word:
        """returns valid instance of Word class if word page is not defined"""

        while not word:
            word = self.parse_word_page(self.get_link_to_random_word())
            print(word)
            print("*" * 20)

        return word


def get_word(word: str = None) -> dict:
    return WordParser(word).word.__dict__()
