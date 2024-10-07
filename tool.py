from classes import Flashcard, Menu, Session


def get_valid_input(question_answer: str) -> str:
    """Return user's input or recursively call this function if input is None."""
    return input(f'{question_answer}:\n').strip() or get_valid_input(question_answer)


def edit_flashcard(flashcard: Flashcard) -> None:
    """
    Show and edit flashcard given as parameter.
    :param flashcard: instance of class Flashcard.
    """
    print(f'\ncurrent question: {flashcard.question}')
    new_question = input('please write a new question:\n').strip()
    print(f'\ncurrent answer: {flashcard.answer}')
    new_answer = input('please write a new answer:\n').strip()
    flashcard.update_flashcard(new_question, new_answer)


def show_flashcards(flashcards: list) -> None:
    """
    For each flashcard in given parameter 'flashcards' show the question and show practice menu.
    :param flashcards: List of flashcard instances of class Flashcard.
    """
    generate_flashcard = (flashcard for flashcard in flashcards)
    for flashcard in generate_flashcard:
        print(f'\nQuestion: {flashcard.question}')
        show_prac_menu(flashcard)
    print()


def get_flashcards(session_status: Session) -> (Menu, Session):
    """
    Depending on which session filter and get flashcards accordingly.

    Collect right flashcards and show them to user.
    Return to main-menu and return the next session.
    :param session_status: Seesion.{name} where 'Session' is a class derived from Enum and 'name' a class attribute.
    :return: Menu.{name} where 'Menu' is a class derived from Enum and 'name' a class attribute and session status.
    """
    box_flashcards = None
    if len(flashcards := Flashcard.read_all_boxes()) == 0:
        print('\nThere is no flashcard to practice!\n')
        return Menu.MAIN, Session.FIRST
    elif session_status is Session.FIRST:
        box_flashcards = Flashcard.read_first_box()
        session_status = Session.SECOND
    elif session_status is Session.SECOND:
        box_flashcards = Flashcard.read_first_second_box()
        session_status = Session.THIRD
    elif session_status is Session.THIRD:
        box_flashcards = flashcards
        session_status = Session.FIRST
    if box_flashcards:
        show_flashcards(flashcards)
        return Menu.MAIN, session_status
    else:
        return get_flashcards(session_status)


def add_flashcard() -> Menu:
    """
    Add new flashcard and return to Sub-Menu.
    :return: Menu.{name} where 'Menu' is a class derived from Enum and 'name' a class attribute.
    """
    new_flashcard = Flashcard(question=get_valid_input('Question'), answer=get_valid_input('Answer'), box_number=1)
    new_flashcard.create_flashcard()
    return Menu.SUB


def show_learning_menu(flashcard: Flashcard) -> None:
    """
    Show learning menu options user can choose.

    Depending on user's choice increment the box number of this given flashcard or
    set the box number to 1.
    Delete flashcards with box number 4.
    :param flashcard: Instance of class Flashcard.
    """
    print(f'press "y" if your answer is correct:\n'
          'press "n" if your answer is wrong:')
    chosen_opt = input().strip()
    if chosen_opt == 'y':
        flashcard.increment_box_number()
    elif chosen_opt == 'n':
        flashcard.set_box_number_one()
    else:
        print(f'{chosen_opt} is not an option\n')
        show_learning_menu(flashcard)
    Flashcard.delete_flashcards_box_number_four()


def show_update_menu(flashcard: Flashcard) -> None:
    """
    Show update menu options user can choose.

    Depending on user's choice delete/edit the given flashcard or go to the update menu.
    :param flashcard: Instance of class Flashcard.
    """
    print('\npress "d" to delete the flashcard:\n'
          'press "e" to edit the flashcard:')
    chosen_opt = input().strip()
    if chosen_opt == 'd':
        flashcard.delete_flashcard()
    elif chosen_opt == 'e':
        edit_flashcard(flashcard)
    else:
        print(f'\n{chosen_opt} is not an option')
        show_update_menu(flashcard)


def show_prac_menu(flashcard: Flashcard) -> None:
    """
    Show practice menu options user can choose.

    Depending on user's choice show answer of the given flashcard or go to next menu.
    :param flashcard: Instance of class Flashcard.
    """
    print('press "y" to see the answer:\n'
          'press "n" to skip:\n'
          'press "u" to update:')
    chosen_opt = input().strip()
    if chosen_opt == 'y':
        print(f'\nAnswer: {flashcard.answer}')
        show_learning_menu(flashcard)
    elif chosen_opt == 'n':
        pass
    elif chosen_opt == 'u':
        show_update_menu(flashcard)
    else:
        print(f'{chosen_opt} is not an option\n')
        show_prac_menu(flashcard)


def show_sub_menu() -> Menu:
    """
    Show sub menu options user can choose and return to next menu.
    :return: Menu.{name} where 'Menu' is a class derived from Enum and 'name' a class attribute.
    """
    print()
    user_choices = list()
    for index, option in enumerate(('Add a new flashcard', 'Exit'), start=1):
        user_choices.append(str(index))
        print(f'{index}. {option}')
    chosen_opt = input().strip()
    if chosen_opt == '1':
        print()
        return Menu.ADD
    elif chosen_opt == '2':
        print()
        return Menu.MAIN
    else:
        print(f'\n{chosen_opt} is not an option')
        return show_sub_menu()


def show_main_menu() -> Menu:
    """
    Show main menu options user can choose and return to next menu.
    :return: Menu.{name} where 'Menu' is a class derived from Enum and 'name' a class attribute.
    """
    user_choices = list()
    for index, option in enumerate(('Add flashcards', 'Practice flashcards', 'Exit'), start=1):
        user_choices.append(str(index))
        print(f'{index}. {option}')
    chosen_opt = input().strip()
    if chosen_opt == '1':
        return Menu.SUB
    elif chosen_opt == '2':
        return Menu.GET
    elif chosen_opt == '3':
        print('\nBye!')
        return Menu.EXIT
    else:
        print(f'\n{chosen_opt} is not an option\n')
        return show_main_menu()


def main():
    """Main control sequence of menu."""
    menu_status = Menu.MAIN
    session_status = Session.FIRST
    while menu_status is not Menu.EXIT:
        if menu_status is Menu.MAIN:
            menu_status = show_main_menu()
        elif menu_status is Menu.SUB:
            menu_status = show_sub_menu()
        elif menu_status is Menu.GET:
            menu_status, session_status = get_flashcards(session_status)
        elif menu_status is Menu.ADD:
            menu_status = add_flashcard()


if __name__ == '__main__':
    main()
