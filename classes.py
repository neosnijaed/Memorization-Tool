from enum import Enum

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Flashcard(Base):
    """
    ORM class with related functionality and initializer for Flashcard.

    Arguments:
    __tablename__ -- a string representing the table of the database.
    id -- an integer representing the id of the Flashcard.
    question -- a string representing the question of the Flashcard.
    answer -- a string representing the answer of the Flashcard.
    box_number -- an integer representing the box number of the Flashcard.
    """
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer)

    def create_flashcard(self):
        """Add the Flashcard instance to the table and commit the changes."""
        session.add(self)
        session.commit()

    @staticmethod
    def read_all_boxes():
        """Return a list of all Flashcard instances in the table."""
        return session.query(Flashcard).all()

    @staticmethod
    def read_first_box():
        """Return Flashcard instances with box number of 1."""
        return session.query(Flashcard).filter(Flashcard.box_number == 1)

    @staticmethod
    def read_first_second_box():
        """Return Flashcard instances with box number of 1 and 2."""
        return session.query(Flashcard).filter(Flashcard.box_number < 3)

    def update_flashcard(self, new_question: str, new_answer: str):
        """
        Update new question and answer of the Flashcard in the table and commit the changes.
        :param new_question: String representing the new question of the Flashcard.
        :param new_answer: String representing the new answer of the Flashcard.
        """
        session.query(Flashcard).filter(Flashcard.id == self.id).update(
            {'question': new_question or self.question, 'answer': new_answer or self.answer}
        )
        session.commit()

    def increment_box_number(self):
        """Increment the box number of the filtered Flashcard in the table and commit the changes."""
        session.query(Flashcard).filter(Flashcard.id == self.id).update(
            {'box_number': self.box_number + 1}
        )
        session.commit()

    def set_box_number_one(self):
        """Set the box number of the filtered Flashcard to 1 in the table and commit the changes."""
        session.query(Flashcard).filter(Flashcard.id == self.id).update(
            {'box_number': 1}
        )
        session.commit()

    def delete_flashcard(self):
        """Delete the filtered Flashcard in the table and commit the changes."""
        session.query(Flashcard).filter(Flashcard.id == self.id).delete()
        session.commit()

    @staticmethod
    def delete_flashcards_box_number_four():
        """Delete the Flashcards with the box number of 4 in the table and commit the changes."""
        session.query(Flashcard).filter(Flashcard.box_number == 4).delete()
        session.commit()


Base.metadata.create_all(engine)


class Menu(Enum):
    """Enums for the Menu."""
    MAIN = 1
    SUB = 2
    GET = 3
    ADD = 4
    EXIT = 5


class Session(Enum):
    """Enums for the Session."""
    FIRST = 1
    SECOND = 2
    THIRD = 3
    EXIT = 4
