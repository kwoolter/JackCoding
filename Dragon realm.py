# DRAGON REALM
import random
import time
import kwutils
import KWGameClasses
import logging

def reset():

    global total_treasure
    global level
    global weapon
    global armour

    total_treasure = 0
    total_treasure = 500
    weapon = "None"
    armour = "None"
    level = 1

def displayIntro():

    print("\nYou are in a land full of dragons.")
    print("In front of you there are three caves,")
    print("one with a friendly dragon,")
    print("who is kind and will share his treasure with you,")
    print("and another who is greedy and hungry,")
    print("he will try to gobble you up!")
    print("and the third cave....who knows?\n")

def choosecave():

    choices = ("Cave 1", "Cave 2", "Cave 3")
    choice = kwutils.pick("Cave", choices)
    cave = choices.index(choice) + 1

    return cave

def check_item(item : str):

    chance = random.randint(1,10)
    logging.info("Item %s break check vs. %i" % (item, chance))

    if item != "None" and chance > 7:
        print("...but your %s broke!" % item)
        item = "None"

    return item

def high_score(high_score_table : KWGameClasses.HighScoreTable, score):

    if high_score_table.is_high_score(score) is True:

        print("\nYour score of %s got you into the high score table!" % format(score,",d"))
        initials = input("Enter Initials:")
        high_score_table.add(initials, score)
        high_score_table.save()


def fight_dragon(dragon_name : str, dragon_stat : float, weapon : str, armour : str):

    global sleep_time
    global weapon_stats
    global armour_stats

    success = True

    weapon_stat = weapon_stats[weapon]
    armour_stat = armour_stats[armour]

    kwutils.type("You found the %s!!!!" % dragon_name)
    time.sleep(sleep_time)

    if weapon != "None":
        print("...you have a " + weapon + "...")
    else:
        print("...you are unarmed...")

    time.sleep(sleep_time)

    if armour != "None":
        print("...you have " + armour + " to protect you...")
    else:
        print("...you have no protection...")

    time.sleep(sleep_time)

    print("...you attack the %s..." % dragon_name)

    time.sleep(sleep_time)

    chance = random.randint(1, 10)

    logging.info("Dragon (%i) vs. weapon (%d) chance" % (chance, weapon_stat * dragon_stat))

    if chance > weapon_stat * dragon_stat:

        print("...the %s attacks you..." % dragon_name)

        time.sleep(sleep_time)

        chance = random.randint(1, 10)

        logging.info("Dragon (%i) vs. armour (%d) chance" % (chance, armour_stat * dragon_stat))

        if chance > armour_stat * dragon_stat:
            success = False
            print("...you lost the fight and died!")
            reset()
        else:
            print("...your %s protects you from the attack and you escape from the cave!" % armour)
    else:
        print("...you defeated the %s!!!" % dragon_name)

    return success

def checkcave(choice : int):

    global total_treasure
    global level
    global weapon
    global armour
    global sleep_time
    global weapon_stats
    global weapon_cost
    global armour_stats
    global armour_cost
    global output_width
    global level_high_score_table
    global treasure_high_score_table

    caves = ["friendly dragon", "hungry dragon", "craftsman", "blacksmith", "empty"]
    random.shuffle(caves)
    selected_cave = caves[choice - 1]
    #selected_cave = "blacksmith"

    print("You chose cave number " + str(choice) + "...")
    time.sleep(sleep_time)

    if level == 30:

        kwutils.type("You made it through the Dragon Realm!")
        kwutils.type("Your quest is complete!")
        print("\nLevel: %i, Treasure: $%s, Weapon: %s" %  (level, format(total_treasure,",d"), weapon))

        print("-" * output_width)
        print(")   T H E   E N D   (".center(output_width, "-"))
        print("-" * output_width)

        high_score(level_high_score_table, level)
        high_score(treasure_high_score_table, total_treasure)

        kwutils.type("\nBack to the start of the Dragon Realm...")
        reset()

    elif level == 25:

        dragon_name = "King Dragon"

        success = fight_dragon(dragon_name, 1/2, weapon, armour)

        time.sleep(sleep_time)

        if success == True:
            treasure = 1000000000
            print("...and you found $" + format(treasure,",d") + "!")

            time.sleep(sleep_time)
            weapon = check_item(weapon)
            time.sleep(sleep_time)
            armour = check_item(armour)

            total_treasure += treasure
            level += 1

    elif level == 20:

        dragon_name = "Queen Dragon"

        success = fight_dragon(dragon_name, 6/10, weapon, armour)

        time.sleep(sleep_time)

        if success == True:
            treasure = 1000000000
            print("...and you found $" + format(treasure,",d") + "!")

            time.sleep(sleep_time)
            weapon = check_item(weapon)
            time.sleep(sleep_time)
            armour = check_item(armour)

            total_treasure += treasure
            level += 1

    elif level == 15:

        dragon_name = "Prince Dragon"

        success = fight_dragon(dragon_name, 7/10, weapon, armour)

        time.sleep(sleep_time)

        if success == True:
            treasure = 1000000000
            print("...and you found $" + format(treasure,",d") + "!")

            time.sleep(sleep_time)
            weapon = check_item(weapon)
            time.sleep(sleep_time)
            armour = check_item(armour)

            total_treasure += treasure
            level += 1

    elif level == 10:

        dragon_name = "Guard Dragon"

        success = fight_dragon(dragon_name, 7/8, weapon, armour)

        time.sleep(sleep_time)

        if success == True:
            treasure = 1000000000
            print("...and you found $" + format(treasure,",d") + "!")

            time.sleep(sleep_time)
            weapon = check_item(weapon)
            time.sleep(sleep_time)
            armour = check_item(armour)

            total_treasure += treasure
            level += 1

    elif selected_cave == "friendly dragon":

        print("You found the friendly dragon...")
        time.sleep(sleep_time)

        treasure = random.randint(1000, 1000000)
        print("...and he shared with you $" + format(treasure,",d") + "!")

        total_treasure += treasure
        level += 1

    elif selected_cave == "hungry dragon":

            dragon_name = "Hungry Dragon"

            success = fight_dragon(dragon_name, 1, weapon, armour)

            time.sleep(sleep_time)
            if success == True:
                treasure = random.randint(500000, 2000000)
                print("...and you found $" + format(treasure,",d") + "!")

                time.sleep(sleep_time)
                weapon = check_item(weapon)
                time.sleep(sleep_time)
                armour = check_item(armour)

                total_treasure += treasure
                level += 1

    elif selected_cave == "craftsman":

        print("You found a craftsman...")
        time.sleep(sleep_time)

        affordable_weapons = []

        for item in weapon_cost.keys():
            if 0 <= weapon_cost[item] <= total_treasure:
                affordable_weapons.append(item)

        if len(affordable_weapons) > 0:

            try:
                affordable_weapons.sort()
                item = kwutils.pick("weapon", affordable_weapons)
                print("You bought %s for $%s." % (item,format(weapon_cost[item],",d")))
                total_treasure -= weapon_cost[item]
                weapon = item
            except Exception as err:
                print("You didn't buy a weapon")
        else:
            print("...but you can't afford any of his weapons!!!")

        level += 1

    elif selected_cave == "blacksmith":

        print("You found a blacksmith...")
        time.sleep(sleep_time)

        affordable_armour = []

        for item in armour_cost.keys():
            if 0 <= armour_cost[item] <= total_treasure:
                affordable_armour.append(item)

        if len(affordable_armour) > 0:
            try:
                affordable_armour.sort()
                item = kwutils.pick("item", affordable_armour)
                print("You bought %s for $%s." % (item,format(armour_cost[item],",d")))
                total_treasure -= armour_cost[item]
                armour = item
            except Exception as err:
                print("You didn't buy an item")
        else:
            print("...but you can't afford any of his items!!!")

        level += 1

    else:
        time.sleep(sleep_time)
        print("The cave is empty!")
        level +=1



# Finished defining the functions, now....

# Start of the main program...

# Define global variables
sleep_time = 1
output_width = 60

weapon_stats = {"None" :  1, "club" : 2, "sword" : 5,"bow" : 3, "axe" : 5, "spear" : 4, "fire bomb" : 6, "dragon slayer" : 9}
weapon_cost = {"None" : -1, "club" : 500, "sword" : 975000,"bow" : 425000, "axe" : 975000, "spear" : 950000, "fire bomb" : 1000000, "dragon slayer" : 999999999}

armour_cost = {"None" : -1, "helmet" : 500, "gauntlets" : 10000, "shield" : 300000, "leather boots" : 50000, "chainmail" : 500000, "scale mail": 1000000}
armour_stats = {"None" : 0, "helmet" : 2, "gauntlets" : 3, "shield" : 5, "leather boots" : 4, "chainmail" : 6, "scale mail" : 7}

# Define the main function
def main():

    logging.basicConfig(level = logging.WARNING)

    level_high_score_table = KWGameClasses.HighScoreTable("Dragon Realm Level", max_size=10, prefix="LV.")
    level_high_score_table.load()

    treasure_high_score_table = KWGameClasses.HighScoreTable("Dragon Realm Treasure", max_size=10, prefix="$")
    treasure_high_score_table.load()

    playing = True

    while playing == True:

        print("-" * output_width)
        print(")   D R A G O N     R E A L M   (".center(output_width, "-"))
        print("-" * output_width)
        level_high_score_table.print()
        treasure_high_score_table.print()

        reset()
        displayIntro()

        keep_going = True

        while keep_going == True:

            try:

                my_choice = choosecave()
                checkcave(my_choice)

                time.sleep(sleep_time)

                print("\nLevel: %i, Treasure: $%s, Weapon: %s, Armour: %s" %  (level, format(total_treasure,",d"), weapon, armour))

                time.sleep(sleep_time)

                keep_going = kwutils.confirm("\nKeep going?")

            except:
                keep_going = False

        high_score(level_high_score_table, level)
        high_score(treasure_high_score_table, total_treasure)

        playing = kwutils.confirm("Play again?")

    # All finished...
    exit(0)

# Call the main function
if __name__ == "__main__":
    main()