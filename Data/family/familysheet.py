"""
This file holds the class that represents a family character sheet for Legacy: Life Among the Ruins 2nd Edition
"""


class FamilySheet:
    # Basic info
    name: str

    # Stats
    reach: int
    grasp: int
    sleight: int

    # Alliance Treaties
    alliance_move: str
    treaties: dict

    # Family Data
    doctrine: list[dict]
    lifestyle: list[dict]
    assets: list[dict]
    traditions: list[dict]
    landmarks: list[dict]
    projects: list[dict]

    # Characters & Character Inheritance
    Inheritance: dict
    Characters: list[int]

    # Resources
    surplus: list[dict]
    needs: list[dict]
    mood: int
    data: int
    tech: int
    family_moves: list[dict]
    family_questions: list[dict]

    def __init__(self, name: str, owner: int):
        self.owner = int
        self.name = name
        self.reach = 0
        self.grasp = 0
        self.sleight = 0
        self.treaties = {}
        self.doctrine = []
        self.lifestyle = []
        self.assets = []
        self.traditions = []
        self.landmarks = []
        self.projects = []
        self.Inheritance = {}
        self.surplus = []
        self.needs = []
        self.mood = 0
        self.data = 0
        self.tech = 0
