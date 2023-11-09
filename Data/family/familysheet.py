import uuid

"""
This file holds the class that represents a family character sheet for Legacy: Life Among the Ruins 2nd Edition
"""

"""
! SETUP TODO:
    ! Family Data
    ! Inheritance
    ! Characters
    ! Resources
    ! Family Questions
"""


class FamilySheet:
    # Basic info
    __id: int
    name: str

    # Stats
    reach: int
    grasp: int
    sleight: int

    # Alliance Move/Treaties
    alliance_move: str
    # treaties:
    treaties: list[dict]
    # Family Data
    doctrine: list[dict]
    lifestyle: list[dict]
    traditions: list[dict]

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

    def __init__(self, name: str, owner: int, reach: int, grasp: int, sleight: int):
        self._id = uuid.uuid4().int
        self.owner = int
        self.name = name
        self.reach = reach
        self.grasp = grasp
        self.sleight = sleight
        self.treaties = []
        self.doctrine = []
        self.lifestyle = []
        self.traditions = []
        self.Inheritance = {"stat": {"choice_1": "", "choice_2": ""}, "moves": []}
        self.surplus = []
        self.needs = []
        self.mood = 0
        self.data = 0
        self.tech = 0

    def __str__(self):
        return f"FamilySheet: {self.name}, ID: {self._id}"

    def __eq__(self, other):
        return self._id == other._id

    @property
    def id(self):
        return self._id


if __name__ == "__main__":
    print("This file is not meant to be run directly")
    exit(1)
