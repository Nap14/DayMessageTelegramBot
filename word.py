import dataclasses


@dataclasses.dataclass
class Word:
    word: str
    description: str
    type: str or None
    pronounce: str or None
    synonyms: list or None

    def dict(self):
        return {
            "word": self.word,
            "description": self.description,
            "type": self.type,
            "pronounce": self.pronounce,
            "synonyms": self.synonyms
        }

    def __eq__(self, other):
        return self.word == other.word
