from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    create_engine,
    select,
    Table,
    Column,
    JSON,
    MetaData,
)
from sqlalchemy.orm import (
    Session,
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from typing import List, Optional

"""
This file contains the SQLAlchemy classes used to define the database schema.
"""


## Base Class for SQLAlchemy
metadata_obj = MetaData(schema="legacy")


class base(DeclarativeBase):
    metadata = metadata_obj


## SQLAlchemy classes


## User class
class User(base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    families: Mapped[List["FamilySheet"]] = relationship(
        "FamilySheet", secondary="owned_families"
    )


## Family Classes
class FamilySheet(base):
    __tablename__ = "family"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    moves: Mapped[List["FamilyMoves"]] = relationship(
        "FamilyMoves", secondary="association_table_family_moves"
    )
    users: Mapped[List[User]] = relationship("User", secondary="owned_families")
    description: Mapped[str] = mapped_column(String)
    reach: Mapped[int] = mapped_column(Integer)
    grasp: Mapped[int] = mapped_column(Integer)
    sleight: Mapped[int] = mapped_column(Integer)
    mood: Mapped[int] = mapped_column(Integer)
    data: Mapped[int] = mapped_column(Integer)
    tech: Mapped[int] = mapped_column(Integer)
    needs: Mapped[list] = mapped_column(JSON)
    surpluses: Mapped[List] = mapped_column(JSON)
    doctrine: Mapped[List] = mapped_column(JSON)
    lifestyle: Mapped[List] = mapped_column(JSON)
    traditions: Mapped[List] = mapped_column(JSON)
    landmarks: Mapped[List] = mapped_column(JSON)
    history: Mapped[List] = mapped_column(JSON)

    def __repr__(self):
        return f"FamilySheet(name={self.name}, owner={self.owner}, reach={self.reach}, grasp={self.grasp}, sleight={self.sleight})"


class FamilyMoves(base):
    __tablename__ = "family_moves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    family: Mapped[List[FamilySheet]] = relationship(
        "FamilySheet", secondary="association_table_family_moves"
    )

    def __repr__(self):
        return f"FamilyMoves(name={self.name}, family={self.family}, description={self.description})"


# Character Classes


class Character(base):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    family: Mapped[int] = mapped_column(Integer, ForeignKey("family.id"))
    user: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    stat_options: Mapped[List] = mapped_column(JSON)
    role_details: Mapped[List] = mapped_column(JSON)
    harm_options: Mapped[List] = mapped_column(JSON)
    death_move: Mapped[str] = mapped_column(String)
    character_moves: Mapped[List["CharacterMove"]] = relationship(
        "CharacterMove", secondary="association_table_character_moves"
    )
    gear: Mapped[List["Gear"]] = relationship("gear", back_populates="owner")


class CharacterMove(base):
    __tablename__ = "character_moves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    characters_using: Mapped[List[Character]] = relationship(
        "Character", secondary="association_table_character_moves"
    )


class Gear(base):
    __tablename__ = "gear"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("character.id"))
    owner: Mapped[Character] = relationship("character", back_populates="gear")
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    tags: Mapped[List] = mapped_column(JSON)


## Game operation Tables


class PostedMove(base):
    __tablename__ = "posted_move"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    family: Mapped[int] = mapped_column(Integer, ForeignKey("family.id"))
    details: Mapped[str] = mapped_column(String)
    cancelled: Mapped[bool] = mapped_column(Integer)


## Association tables
OwnedFamilies_table = Table(
    "owned_families",
    base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("family_id", Integer, ForeignKey("family.id")),
    Column("selected_stat", Integer),
    Column("selected_doctrine", Integer),
    Column("selected_lifestyle", Integer),
    Column("selected_tradition", Integer),
    Column("selected_landmark", Integer),
    Column("selected_history", Integer),
    Column("selected_moves", Integer),
)

AssocFamilyMoves_table = Table(
    "association_table_family_moves",
    base.metadata,
    Column("family_id", Integer, ForeignKey("family.id")),
    Column("move_id", Integer, ForeignKey("family_moves.id")),
)

AssocCharacterMoves_table = Table(
    "association_table_character_moves",
    base.metadata,
    Column("character_id", Integer, ForeignKey("character.id")),
    Column("move_id", Integer, ForeignKey("character_moves.id")),
)


# Debugging db test code
engine = create_engine("postgresql://sqlalch:pass@localhost:5432/Legacy", echo=True)
base.metadata.create_all(engine)
session = sessionmaker(bind=engine)
session = session()
