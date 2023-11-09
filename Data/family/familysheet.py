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
    ! Family Moves
        ? Class
    ! Family Questions
"""


class FamilySheet:
    # Basic info
    id: int
    name: str

    # Stats
    reach: int
    grasp: int
    sleight: int

    # Alliance Treaties
    alliance_move: str
    treaties: list[dict]

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

    def __init__(self, name: str, owner: int, reach: int, grasp: int, sleight: int):
        self.id = uuid.uuid4().int
        self.owner = int
        self.name = name
        self.reach = reach
        self.grasp = grasp
        self.sleight = sleight
        self.treaties = []
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

        # Set the stats
        def setStats(self, reach: int, grasp: int, sleight: int):
            self.reach = reach
            self.grasp = grasp
            self.sleight = sleight

        # Get the stats
        def getStats(self):
            return self.reach, self.grasp, self.sleight

        # Set the alliance move
        def setAllianceMove(self, move: str):
            self.alliance_move = move

        # Get the alliance move
        def getAllianceMove(self):
            return self.alliance_move

        # Add a family to the treaty list
        def addfamily(self, family: str, treaty: dict):
            treaty = {"family": family, "points": {"to": 0, "from": 0}}

        # Get a list of all treaties
        def getTreatiesList(self):
            return self.treaties

        # Get a treaty by family name
        def getTreaty(self, family: str):
            for treaty in self.treaties:
                if treaty["family"] == family:
                    return treaty
            return None

        # add a treaty point to a family
        def addTreatypoint(self, family: str, direction: str, amount: int):
            treaty = self.getTreaty(family)
            if direction is not "to" or direction is not "from":
                raise ValueError("direction must be 'to' or 'from'")
            if treaty is not None:
                treaty["points"][direction] += amount
                return True
            else:
                return False

        # Remove a Treaty point from a family
        def removeTreatypoint(self, family: str, direction: str, amount: int):
            treaty = self.getTreaty(family)
            if direction is not "to" or direction is not "from":
                raise ValueError("direction must be 'to' or 'from'")
            if treaty is not None:
                treaty["points"][direction] -= amount
                # Can't be less that 0
                if treaty["points"][direction] < 0:
                    treaty["points"][direction] = 0
                return True
            else:
                return False
