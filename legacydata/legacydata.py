from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    BigInteger,
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

## Association tables
ownedfamilies_table = Table(
    "owned_families",
    base.metadata,
    Column("user_id", Integer, ForeignKey("legacy_user.id")),
    Column("family_id", Integer, ForeignKey("family.id")),
    Column("selected_stat", Integer),
    Column("selected_doctrine", Integer),
    Column("selected_lifestyle", Integer),
    Column("selected_tradition", Integer),
    Column("selected_landmark", Integer),
    Column("selected_history", Integer),
    Column("selected_moves", Integer),
)

assocfamilymoves_table = Table(
    "association_table_family_moves",
    base.metadata,
    Column("family_id", Integer, ForeignKey("family.id")),
    Column("move_id", Integer, ForeignKey("family_moves.id")),
)

assocharactermoves_table = Table(
    "association_table_character_moves",
    base.metadata,
    Column("character_id", Integer, ForeignKey("character.id")),
    Column("move_id", Integer, ForeignKey("character_moves.id")),
)


## User class
class User(base):
    __tablename__ = "legacy_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    discord_id: Mapped[int] = mapped_column(BigInteger)
    families: Mapped[List["FamilySheet"]] = relationship(
        "FamilySheet", secondary=ownedfamilies_table, back_populates="users"
    )


## Family Classes
class FamilySheet(base):
    __tablename__ = "family"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    moves: Mapped[List["FamilyMoves"]] = relationship(
        "FamilyMoves", secondary=assocfamilymoves_table, back_populates="family"
    )
    users: Mapped[List[User]] = relationship(
        "User", secondary=ownedfamilies_table, back_populates="families"
    )
    reach: Mapped[int] = mapped_column(Integer, default=0)
    grasp: Mapped[int] = mapped_column(Integer, default=0)
    sleight: Mapped[int] = mapped_column(Integer, default=0)
    mood: Mapped[int] = mapped_column(Integer, default=0)
    data: Mapped[int] = mapped_column(Integer, default=0)
    tech: Mapped[int] = mapped_column(Integer, default=0)
    needs: Mapped[list] = mapped_column(JSON, default=list)
    surpluses: Mapped[List] = mapped_column(JSON, default=list)
    doctrine: Mapped[List] = mapped_column(JSON, default=list)
    lifestyle: Mapped[List] = mapped_column(JSON, default=list)
    traditions: Mapped[List] = mapped_column(JSON, default=list)
    landmarks: Mapped[List] = mapped_column(JSON, default=list)
    history: Mapped[List] = mapped_column(JSON, default=list)

    def __str__(self):
        return f"ID: {self.id} name:{self.name}:"


class FamilyMoves(base):
    __tablename__ = "family_moves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    family: Mapped[List[FamilySheet]] = relationship(
        "FamilySheet", secondary=assocfamilymoves_table, back_populates="moves"
    )

    def __repr__(self):
        return f"FamilyMoves(name={self.name}, family={self.family}, description={self.description})"


# Character Classes


class Gear(base):
    __tablename__ = "gear"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("character.id"))
    owner: Mapped["Character"] = relationship("Character", back_populates="gear")
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    tags: Mapped[List] = mapped_column(JSON)


class Character(base):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    family: Mapped[int] = mapped_column(Integer, ForeignKey("family.id"))
    user: Mapped[int] = mapped_column(Integer, ForeignKey("legacy_user.id"))
    stat_options: Mapped[List] = mapped_column(JSON)
    role_details: Mapped[List] = mapped_column(JSON)
    harm_options: Mapped[List] = mapped_column(JSON)
    death_move: Mapped[str] = mapped_column(String)
    character_moves: Mapped[List["CharacterMove"]] = relationship(
        "CharacterMove",
        secondary=assocharactermoves_table,
        back_populates="characters_using",
    )
    gear: Mapped[List["Gear"]] = relationship("Gear", back_populates="owner")


class CharacterMove(base):
    __tablename__ = "character_moves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    characters_using: Mapped[List[Character]] = relationship(
        "Character",
        secondary=assocharactermoves_table,
        back_populates="character_moves",
    )


## Game operation Tables


class PostedMove(base):
    __tablename__ = "posted_move"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    family: Mapped[int] = mapped_column(Integer, ForeignKey("family.id"))
    details: Mapped[str] = mapped_column(String)
    cancelled: Mapped[bool] = mapped_column(Integer)


# Debugging db test code
engine = create_engine("postgresql://sqlalch:pass@localhost:5432/Legacy", echo=True)
base.metadata.create_all(engine)
session = sessionmaker(bind=engine)
session = session()
