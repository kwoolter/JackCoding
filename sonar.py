__author__ = 'user'

import random
import sys
import time
import os
import math
import kwutils
import logging
import KWGameClasses
import pickle
import colorama

# Generate a random level
def random_level(level = 1):

    width = random.randint(4 + level, 6 + level * 2)
    height = random.randint(5, 5 + level)
    chests = random.randint(1 + int(level/2), 3 + int(level/2))
    detectors = random.randint(10 + level, 10 + level * 2)
    junk = random.randint(int(level/2), level)

    return width, height, chests, detectors, junk

# Pick a sonar level file and load it
def pick_levels():
    game_files = []

    for file in os.listdir("."):
        if file.endswith(".lvl"):
            game_files.append(file)

    logging.info("Found %s levcel files." % str(game_files))

    level_file = kwutils.pick("level", game_files, auto_pick=True)

    levels = load_level(level_file)

    return levels


# Load levels from a specified file name
def load_level(file_name : str):

    levels =[]

    try:
        game_file = open(file_name, "rb")
        levels = pickle.load(game_file)
        game_file.close()
        logging.info("\n%s loaded.\n" % file_name)

    except FileNotFoundError:
        logging.warning("Level file %s not found." % file_name)

    return levels

# Save levels to a specified file name
def save_levels(levels, file_name : str):

    file_name += ".lvl"
    game_file = open(file_name, "wb")
    pickle.dump(levels, game_file)
    game_file.close()
    logging.info("%s saved." % file_name)

    return

# Utility function for creating sonar level files
def util_build_level_files():

    # level parameters = width, height, treasures, max_detectors, junk
    levels =((16,10,1,10,0), (16,10,3,10,0), (16,10,3,10,1), (20,15,3,15,1), (20,15,5,15,2), (20,15,5,15,3),
             (30,20,10,30,4))

    save_levels(levels, "sonar_evil")

    return

# Fill the board with sea graphics
def initialise_board(rows, width, height):

    graphics = ["~", "`"]
    for y in range(0, height):
        row = []
        for x in range(0, width):
            row.append(graphics[random.randint(0,len(graphics))-1])
        rows.append(row)

# Print the whole board
def print_board(rows):

    # get the width of the board
    width = len(rows[0])

    INDENT = " " * int((GameOptions.TITLE_WIDTH/2 - 2 - (width)/2))

    # Print the game logo
    print(GameOptions.COLOUR_LOGO + "-" * GameOptions.TITLE_WIDTH + GameOptions.COLOUR_TEXT)
    print(GameOptions.COLOUR_LOGO + ")   S O N A R   (".center(GameOptions.TITLE_WIDTH, "-") + GameOptions.COLOUR_TEXT)
    print(GameOptions.COLOUR_LOGO + "-" * GameOptions.TITLE_WIDTH + GameOptions.COLOUR_TEXT)


    # Print Top major coordinate numbers
    sys.stdout.write(GameOptions.COLOUR_BACKGROUND + INDENT + "  " + GameOptions.COLOUR_COORDS)
    for i in range(0, width):
        if i % 10 == 0:
            sys.stdout.write(str(i // 10))
        else:
           sys.stdout.write(" ")
    print(GameOptions.COLOUR_BACKGROUND + " " * int(GameOptions.TITLE_WIDTH/2 - width/2) + GameOptions.COLOUR_TEXT)

    # Print Top minor coordinate numbers
    print(GameOptions.COLOUR_BACKGROUND + INDENT + "  " + GameOptions.COLOUR_COORDS, end="")
    for i in range(0, width):
        sys.stdout.write(str(i % 10))
    print(GameOptions.COLOUR_BACKGROUND + " " * int((GameOptions.TITLE_WIDTH/2 - width/2))+ GameOptions.COLOUR_TEXT)

    # Print the main board
    # For each row on the board
    for y in range(0, len(rows)):

        # Get the row details
        row = rows[y]

        sys.stdout.write(GameOptions.COLOUR_BACKGROUND + INDENT + GameOptions.COLOUR_COORDS)

        # Print left hand side major coordinates
        if y % 10 == 0:
            sys.stdout.write(GameOptions.COLOUR_COORDS + str(y // 10))
        else:
            sys.stdout.write(GameOptions.COLOUR_COORDS + " ")

        # Print left hand side minor coordinates
        sys.stdout.write(str(y % 10))

        # Print the row details
        for x in range(len(row)):
            if row[x] in ("~","`"):
                sys.stdout.write(GameOptions.COLOUR_SEA)
            else:
                sys.stdout.write(GameOptions.COLOUR_DETECTOR)

            sys.stdout.write(row[x])

        # Print the right hand side minor coordinates
        sys.stdout.write(GameOptions.COLOUR_COORDS + str(y % 10))

        # Print the right hand side major coordinates
        if y % 10 == 0:
            sys.stdout.write(str(y // 10))
        else:
            sys.stdout.write(" ")

        sys.stdout.flush()
        print(GameOptions.COLOUR_BACKGROUND  + " " * int(GameOptions.TITLE_WIDTH/2 - 2 - width/2) + GameOptions.COLOUR_TEXT)

    # Print Bottom Minor Coordinates
    sys.stdout.write(GameOptions.COLOUR_BACKGROUND + INDENT + "  " + GameOptions.COLOUR_COORDS)
    for i in range(0, width):
        sys.stdout.write(str(i % 10))
    print(GameOptions.COLOUR_BACKGROUND + " " * int((GameOptions.TITLE_WIDTH/2 - width/2))+ GameOptions.COLOUR_TEXT)

    # Print bottom Major coordinates
    sys.stdout.write(GameOptions.COLOUR_BACKGROUND + INDENT + "  " + GameOptions.COLOUR_COORDS)
    for i in range(0, width):
        if i % 10 == 0:
            sys.stdout.write(str(i // 10))
        else:
           sys.stdout.write(" ")

    print(GameOptions.COLOUR_BACKGROUND + " " * int((GameOptions.TITLE_WIDTH/2 - width/2))+ GameOptions.COLOUR_TEXT)

    print(GameOptions.COLOUR_SEA + "-" * GameOptions.TITLE_WIDTH + GameOptions.COLOUR_TEXT)

    return

# Get the user to input a valid coordinate
def get_valid_postion(width : int, height : int):
    x = y = -1

    print("Enter coordinates:")
    while x < 0 or x >= width:
        selection = input("X:")
        if kwutils.is_numeric(selection) != None:
            x = int(selection)

    while y < 0 or y >= height:
        selection = input("Y:")
        if kwutils.is_numeric(selection) != None:
            y = int(selection)

    return x,y

# Calculate the distance between a detector and a chest
def get_distance(detector, item):

    x,y = detector
    chest_x, chest_y = item

    return math.sqrt(math.pow(abs(x - chest_x),2) + math.pow(abs(y - chest_y),2))

# Add the detectors to the board based on distance from nearest item
def add_detectors(rows, detectors, chests, junk_items = []):

    all_items = chests + junk_items
    logging.info("Checking detectors against %s" % str(all_items))

    # Go through each of the detectors
    for detector in detectors:

        # Extract detector coordinates
        x,y = detector

        smallest_distance = 1000

        #  Go through each item and see how far away it is from the current detector....
        for item in all_items:

            # Get the distance between the current detector and chest
            distance = get_distance(detector, item)

            # Record the smallest distance from this detector to am item
            if distance < smallest_distance:
                smallest_distance = distance

        row = rows[y]

        # If distance to the nearest chest is too far away set detector value to '?' - out of range
        if smallest_distance >= 10:
            row[x] = "?"
        # Else display the distance to the nearest chest from the detector
        else:
            row[x] = str(int(smallest_distance))


class GameOptions:

    COLOUR_LOGO = "\x1B[36;44m"
    COLOUR_SEA = "\x1B[36;44m"
    COLOUR_TEXT = "\x1B[30;48m"
    COLOUR_COORDS = "\x1B[30;47m"
    COLOUR_DETECTOR = "\x1B[30;103m"
    COLOUR_BACKGROUND = "\x1B[30;96m"
    TITLE_WIDTH = 46
    RANDOM_LEVELS = 10

    @staticmethod
    def colour_on(on : bool = True):
        if on is True:
            GameOptions.COLOUR_LOGO = "\x1B[36;44m"
            GameOptions.COLOUR_SEA = "\x1B[36;44m"
            GameOptions.COLOUR_TEXT = "\x1B[30;48m"
            GameOptions.COLOUR_BACKGROUND = "\x1B[30;46m"
            GameOptions.COLOUR_COORDS = "\x1B[30;47m"
            GameOptions.COLOUR_DETECTOR = "\x1B[30;103m"
        else:
            GameOptions.COLOUR_LOGO = ""
            GameOptions.COLOUR_SEA = ""
            GameOptions.COLOUR_TEXT = ""
            GameOptions.COLOUR_BACKGROUND = ""
            GameOptions.COLOUR_COORDS = ""
            GameOptions.COLOUR_DETECTOR = ""

        return

# Main
def main():

    #colorama.init()

    logging.basicConfig(level = logging.WARNING)

    # util_build_level_files()

    GameOptions.colour_on(kwutils.confirm("Do you want to play in colour"))

    TITLE_WIDTH = GameOptions.TITLE_WIDTH

    # Load levels from a .lvl file....
    if kwutils.confirm("Do you want to load levels from file?") is True:
        levels = pick_levels()
    # ...or randomly generate levels
    else:
        kwutils.type("Generating random levels.......")
        levels = []
        for i in range(1, GameOptions.RANDOM_LEVELS):
            levels.append(random_level(i))

    high_score_table = KWGameClasses.HighScoreTable("SONAR", 10)
    high_score_table.load()

    running = True

    # While player keeps wanting to play
    while running == True:

        playing = True
        score = 0
        level = 1

        kwutils.type("Welcome to......")

        # Print the game logo
        print(GameOptions.COLOUR_LOGO + "-" * TITLE_WIDTH + GameOptions.COLOUR_TEXT)
        print(GameOptions.COLOUR_LOGO + ")   S O N A R   (".center(TITLE_WIDTH, "-") + GameOptions.COLOUR_TEXT)
        print(GameOptions.COLOUR_LOGO + "-" * TITLE_WIDTH + GameOptions.COLOUR_TEXT)

        print("%i Levels loaded." % len(levels))
        print("Place sonar detectors in the sea to find all of the treasure!")
        print("The value on a detector indicates how far away from an object it is.\n")
        high_score_table.print()

        time.sleep(2)

        # Main game loop
        while playing == True:

            kwutils.type("\nStarting Level %i...\n" % level)

            time.sleep(2)

            # Define lists for storing game state
            detectors = []
            chests = []
            junk_items = []
            board = []

            # Get the details of the new level
            width, height, treasures, max_detectors, junk = levels[level - 1]

            # Fill the board with sea graphics
            initialise_board(board, width, height)

            # Generate treasure chests in unique random positions
            for i in range(0,treasures):
                while True:
                    new_item = (random.randint(0,width -1),random.randint(0,height -1))
                    if new_item not in chests:
                        break

                chests.append(new_item)

            logging.info("Added chests: %s" % str(chests))

            # Generate junk in unique random positions, and not in same position as treasure
            for i in range(0,junk):
                while True:
                    new_item = (random.randint(0,width -1),random.randint(0,height -1))
                    if new_item not in chests and new_item not in junk_items:
                        break

                junk_items.append(new_item)

            logging.info("Added junk: %s" % str(junk_items))


            # Play the current level
            # Loop while...
            # You still have detectors to use AND
            # You still have some treasure chests to find!
            while (len(detectors) < max_detectors) and (len(chests) > 0):

                logging.info("Active chests: %s" % str(chests))
                logging.info("Active junk: %s" % str(junk_items))
                logging.info("Active detectors: %s" % str(detectors))

                # Add the live detectors and their current distances to the board
                add_detectors(board, detectors, chests, junk_items)

                # Print the board
                print_board(board)

                # Print current level status
                print("Level %i, Score %i: Detectors %i/%i, Chests %i/%i" % (level, score, len(detectors), max_detectors, treasures - len(chests), treasures))

                # Ask user for new coordinates
                while True:
                    new_coord = get_valid_postion(width, height)
                    if new_coord not in detectors:
                        break
                    else:
                        print("Already a detector at this location!")

                # Add the new detector to the active list
                detectors.append(new_coord)

                # Check if you have found a chest...
                if new_coord in chests:

                    # If you have found one then remove chest from the active list
                    chests.remove(new_coord)
                    kwutils.type("\nYou found......a chest!!!")

                    # If that was not the last chest, did you find a detector in the chest?
                    if len(chests) > 0 and random.randint(1,10) > 7:
                        kwutils.type("...the treasure chest contained a sonar detector!")
                        max_detectors += 1

                    time.sleep(2)


                # Check if you have found some junk...
                if new_coord in junk_items:

                    # If you have found some then remove the junk from the active list
                    junk_items.remove(new_coord)
                    kwutils.type("\nYou found......some old junk!!!")

                    # Did you find a treasure map in the junk?
                    if random.randint(1,10) > 7:
                        x, y = random.choice(chests)
                        kwutils.type("...the junk contained a map to some treasure at %i,%i!" % (x, y))

                    time.sleep(2)

            # We have finished the game, so...
            # ...see if we found all of the chests?
            if len(chests) == 0:
                print("\nCongratulations you completed Level %i! You found all %i treasure chests!!!" % (level, treasures))
                level += 1
                # Get 10 points for finishing the level + bonus for unused detectors
                score += 10 + (max_detectors - len(detectors))

            # If we didn't find all of the chests then it is game over!
            else:
                print("Bad luck you used up all of your detectors! You managed to find %i of the %i treasure chests!" % (treasures - len(chests), treasures))
                playing = False

            # If we have reached the last level then we are done!
            if level > len(levels):
                kwutils.type("Amazing. You completed the final level!!!!")
                score += 20
                playing = False

            time.sleep(2)

        kwutils.type("-" * 40, wait=0.02)
        kwutils.type(")   G A M E   O V E R   (".center(40, "-"))
        kwutils.type("-" * 40, wait=0.02)


        if high_score_table.is_high_score(score) is True:

            print("\nYour score of %i got you into the high score table!" % score)
            initials = input("Enter Initials:")
            high_score_table.add(initials, score)
            high_score_table.save()

        if kwutils.confirm("Do you want to play again?") is False:
            running = False



# Call the main function
if __name__ == "__main__":
    main()













