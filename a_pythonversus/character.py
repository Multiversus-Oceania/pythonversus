import json
from typing import Optional


class Character:
    def __init__(self, name: str, slug: str, emote: str):
        self.name = name
        self.slug = slug
        self.emote = emote

    @classmethod
    def from_dict(cls, data: dict) -> 'Character':
        return cls(data['name'], data['slug'], data['emote'])

    def __str__(self) -> str:
        return f"{self.name} ({self.slug})"


class CharacterManager:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.characters = {
                key: Character.from_dict(value)
                for key, value in json.load(f).items()
            }

    def get_character_by_key(self, key: str) -> Optional[Character]:
        return self.characters.get(key.strip())

    def get_character_by_slug(self, slug: str) -> Optional[Character]:
        slug = slug.strip().lower()
        return next((char for char in self.characters.values() if char.slug.lower() == slug), None)

    def get_character_by_name(self, name: str) -> Optional[Character]:
        name = name.strip().lower()
        return next((char for char in self.characters.values() if char.name.lower() == name), None)

    def get_slug_from_name(self, name: str) -> Optional[str]:
        character = self.get_character_by_name(name)
        return character.slug if character else None

    def get_emote_from_slug(self, slug: str) -> Optional[str]:
        character = self.get_character_by_slug(slug)
        return character.emote if character else None

    def get_emote_from_name(self, name: str) -> Optional[str]:
        character = self.get_character_by_name(name)
        return character.emote if character else None
