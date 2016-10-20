import random

def play_game(switch):
    doors = list(range(3))
    winner = random.choice(doors)
    initial_choice = random.choice(doors)
    remove_losing_door(doors, initial_choice, winner)

    if switch:
        switched_choice = random.choice(doors)
        return switched_choice == winner

    else:
        return initial_choice == winner

def remove_losing_door(doors, initial_choice, winner):
    doors.remove(initial_choice)

    if winner == initial_choice:
        removed = doors.pop()
    else:
        doors.remove(winner)
        removed = doors.pop()
        doors.append(winner)
