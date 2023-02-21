import json

from parser import WordParser


class Chat:

    chats = set()

    def __init__(
        self, message=None, *, chat_id: int = None, word: str = None, spam: bool = None
    ):
        if message:
            self.id = message.chat.id
            self.word = WordParser()
            self.spam = True
            for chat in self.get_chats():
                self.chats.add(chat)
        else:
            self.id = chat_id
            self.word = WordParser(word)
            self.spam = spam

        self.chats.add(self)
        self.save_chats()

    def __dict__(self):
        return {"chat_id": self.id, "word": self.word.word.word, "spam": self.spam}

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

    def __repr__(self):
        return f"Chat(chat id: {self.id})"

    def save_chats(self):
        with open("chats/chats.json", "wt") as file:
            json.dump([chat.__dict__() for chat in self.chats], file, indent=2)

    @staticmethod
    def get_chats():
        with open("chats/chats.json") as file:
            return [Chat(**chat) for chat in json.load(file)]

    @classmethod
    def get_chat(cls, message):
        for chat in cls.chats:
            if chat.id == int(message.chat.id):
                return chat
