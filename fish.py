import random


class FriendlyCard:
    def __init__(self, name, card_type, description, attack, health):     # defining instance variables
        self.name = name
        self.card_type = card_type
        self.description = description
        self.attack = attack
        self.health = health

    def print_card(self):
        print(self.name + " (" + self.card_type + ") - " + self.description +
              "\nAttack: " + str(self.attack) + ", Health: " + str(self.health) + "\n")

    def get_name(self):
        return self.name


class RobotCard:
    def __init__(self, name, description, attack, health):
        self.name = name
        self.description = description
        self.attack = attack
        self.health = health

    def print_card(self):
        print(self.name + " - " + self.description +
              "\nAttack: " + str(self.attack) + ", Health: " + str(self.health) + "\n")


def main():
    player_deck = []    # Contains all the friendly fish cards
    robot_deck = []     # Contains all the robot fish cards
    hand1 = []          # List of cards in player 1 hand
    hand2 = []          # List of cards in player 2 hand

    # Read-only file
    friendly_file = open("fish_directory.txt", "r")  # Open the file
    player_deck_strings = friendly_file.read().splitlines()  # Each line from the file is stored as a string

    # Iterate through each item of the list (aka line of the file) and make a Card object out of it
    for line in player_deck_strings:
        attribute = line.split(", ")
        num_to_add = int(attribute[5])
        for i in range(num_to_add):
            player_deck.append(
                FriendlyCard(attribute[0], attribute[1], attribute[2], int(attribute[3]), int(attribute[4]))
            )

    # Now do the same for the robot file
    robot_file = open("robot_fish_directory.txt", "r")
    robot_deck_strings = robot_file.read().splitlines()

    for line in robot_deck_strings:
        attribute = line.split(", ")
        num_to_add = int(attribute[4])
        for i in range(num_to_add):
            robot_deck.append(
                RobotCard(attribute[0], attribute[1], int(attribute[2]), int(attribute[3]))
            )

    # Shuffle the cards and draw a hand of 7 for each player
    random.seed(1)
    random.shuffle(player_deck)
    random.shuffle(robot_deck)
    player1 = setup(player_deck, hand1, hand2)

    take_turns(player_deck, robot_deck, hand1, hand2, player1)


def setup(player_deck, hand1, hand2):
    # Get a valid player num
    player_string = input("What player are you? Type 1 or 2: ")
    while not (player_string.isdigit() and (int(player_string) < 3 and int(player_string) > 0)):
        player_string = input("Invalid answer. Type 1 or 2: ")
    player_num = int(player_string)

    if player_num == 1:
        player1 = True   # This boolean is True if the user is player1
    else:
        player1 = False

    # Draw a hand of 7 cards
    for i in range(7):
        draw_card(player_deck, hand1, False)
        draw_card(player_deck, hand2, False)

    return player1


def take_turns(player_deck, robot_deck, hand1, hand2, player1):
    num_coral = 3
    round_num = 0
    player_discard_pile = []
    robot_discard_pile = []

    if player1:
        hand = hand1
    else:
        hand = hand2

    while num_coral > 0:
        round_num += 1

        input("Press enter to begin the next round: ")

        print("\n*********************************** Your hand ***********************************\n")
        for card in hand:
            card.print_card()

        all_player_cards = play_cards(hand1, hand2, player1)
        all_robot_cards = robots_attack(robot_deck, round_num)

        # Menu options
        print("What effects take place?")
        print("1. None.")
        print("2. Each player may draw a card.")
        print("3. Play the top 3 fish from the friendly fish deck.")
        print("4. Each player may discard any number of cards and draw that many cards.")
        print("5. Each player MUST discard a card.")

        choice_string = input("\nType the corresponding number(s) separated by a space: ")
        choice_nums = choice_string.split(" ")
        for i in choice_nums:
            resolve_effects(int(i), player_deck, robot_deck, hand1, hand2, player1, all_player_cards, player_discard_pile)

        # Discard played cards
        for card in all_player_cards:
            player_discard_pile.append(card)

        for card in all_robot_cards:
            robot_discard_pile.append(card)

        print("All effects are completed. Begin the attack. Good luck!")
        print("\n---------------------------- ALL FRIENDLY FISH CARDS ----------------------------\n")
        for card in all_player_cards:
            card.print_card()
        print("\n----------------------------- ALL ROBOT FISH CARDS ------------------------------\n")
        for card in all_robot_cards:
            card.print_card()

        input("Press enter when you have resolved the battle: ")
        saved_coral = int(input("Were you able to save the coral this round? (1) yes, (2) no: "))
        if saved_coral == 1:
            print("Congratulations!\n")
        else:
            num_coral -= 1
        print("Coral left: " + str(num_coral) + "\n")

        # New hand
        if num_coral > 0:
            print("Drawing 2 cards and beginning new round.")
        else:
            print("Game over. You made it through " + str(round_num) + " rounds!")
        for i in range(2):
            draw_card(player_deck, hand1, False)
            draw_card(player_deck, hand2, False)


def resolve_effects(choice, player_deck, robot_deck, hand1, hand2, player1, all_player_cards, player_discard_pile):
    if choice != 1:
        print("Resolving effect " + str(choice) + "...\n")
    if choice == 2:
        print("Below is the card you drew:")
        draw_card(player_deck, hand1, player1)
        draw_card(player_deck, hand2, not player1)
        input("Press enter to continue: ")
    elif choice == 3:
        print("Below are the extra cards to be played from the top of the deck:")
        for i in range(3):
            player_deck[0].print_card()
            all_player_cards.append(player_deck[0])
            player_deck.remove(player_deck[0])
        input("Press enter to continue: ")
    elif choice == 4 or choice == 5:
        if player1:
            hand = hand1
        else:
            hand = hand2

        print("Your hand:")
        for card in hand:
            card.print_card()

        print("Choose what to discard.")

        # Print out the options
        if choice == 4:
            print("1. None")
        else:
            print("1. None - NOT A VALID CHOICE")

        for i in range(len(hand)):
            card = hand[i]
            print("{}. ".format(i + 2) + card.get_name())

        # Allow for user input
        if choice == 4:
            choice_nums = input("\nType the corresponding numbers, separated by a space: ")
        else:
            choice_nums = input("\nType the corresponding number: ")

        cards_chosen = choose_cards(choice_nums, hand, player_discard_pile)  # Removes cards from hand and adds to discard pile
        print("\nYour replacement cards:")
        for i in range(cards_chosen):
            draw_card(player_deck, hand, True)

        if choice == 4:
            choice_nums = input("Type the numbers the other player entered, separated by a space: ")
        else:
            choice_nums = input("Type the number entered by the other player: ")

        if player1:
            cards_chosen = choose_cards(choice_nums, hand2, player_discard_pile)
            for i in range(cards_chosen):       # Draw replacement cards for other player but don't show to user
                draw_card(player_deck, hand2, False)
        else:
            cards_chosen = choose_cards(choice_nums, hand1, player_discard_pile)
            for i in range(cards_chosen):
                draw_card(player_deck, hand1, False)
        input("Press enter to continue: ")
    else:
        print("No effects chosen.")
        input("Press enter to continue: ")


def play_cards(hand1, hand2, player1):
    all_player_cards = []

    # YOU
    print("Which cards would you like to play?")
    if player1:
        hand = hand1
    else:
        hand = hand2

    # Print out the options
    print("1. None")
    for i in range(len(hand)):
        card = hand[i]
        print("{}. ".format(i+2) + card.get_name())

    # Allow for user input
    choice_nums = input("\nType the corresponding numbers, separated by a space: ")
    choose_cards(choice_nums, hand, all_player_cards)   # num_cards_chosen1 is the number of cards YOU played

    # OTHER PLAYER
    choice_nums = input("Type the numbers the other player entered, separated by a space: ")
    if player1:
        choose_cards(choice_nums, hand2, all_player_cards)
    else:
        choose_cards(choice_nums, hand1, all_player_cards)

    return all_player_cards


def robots_attack(robot_deck, round_num):
    all_robot_cards = []

    print("\nThe following robots are attacking this round:")

    for i in range(round_num):
        card = robot_deck[0]
        card.print_card()
        all_robot_cards.append(card)
        robot_deck.remove(card)

    return all_robot_cards


def choose_cards(choice_nums, hand, all_player_cards):
    cards = choice_nums.split(" ")
    cards_chosen = []
    for num in cards:
        card_num = int(num)
        if card_num != 1:
            card = hand[card_num - 2]
            cards_chosen.append(card)
            print("{} card chosen.\n".format(card.get_name()))

    for card in cards_chosen:
        hand.remove(card)
        all_player_cards.append(card)

    return len(cards_chosen)


def draw_card(player_deck, hand, should_print):
    card = player_deck[0]
    hand.append(card)
    player_deck.remove(card)
    if should_print:
        card.print_card()


if __name__ == "__main__":
    main()
