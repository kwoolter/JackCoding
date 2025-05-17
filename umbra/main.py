
# import the modules
from colorama import *
import random
import colorama
from globals import *
from utilities import *


# function for printing areas
def area(title, descrip):
    myprint(f'{Fore.RED}{Style.BRIGHT}{title.upper()}')
    myprint(f'\t{Fore.YELLOW}{descrip}')


# function for printing scenes
def scene(name, descrip, options=None):
    myprint(f'{Fore.BLUE}{Style.BRIGHT}{name}')
    myprint(f'{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{descrip}')

    # if you specified options ask the user to pick one.

    if options is not None:
        return pick(options)


# function for printing and "making" bosses
# gets the values from the bosses dictionary

def boss(bossName):
    description, health, boss_losing = bosses[bossName]
    myprint(f'{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{bossName.upper()}')
    myprint(f'{Fore.MAGENTA}{description} - {health}hp')
    return description, health


# ???
def boss_fight(bossName):
    description, health, boss_losing = bosses[bossName]
    boss(bossName)

    for turn in range(3):
        answer = scene(f"Boss fight with {bossName}", "What weapon do you attack with?", inventory)
        min, max, multiplier = weapons[answer]
        damage = random.randint(min, max) * multiplier
        health -= damage
        if health <= 0:
            health = 0
        myprint(f'you did {damage} damage to  {bossName} with {answer}\n{health}hp left')
        if health <= 0:
            break
    if health <= 0:
        myprint(f'{bossName} fell to ground, he has been defeated')
    elif health > 0:
        for msg in boss_losing:
            myprint(msg)
        return False

    return True


def monkey_forest(name, npc, npc2):
    global fires_lit

    greeting, im = npcs[npc]
    greeting2, im2 = npcs[npc2]
    answer = scene(npc + " vanishes and you find yourself before an archway leading to a forest", "Will you enter?",
                   ["yes", "no"])

    if answer == "yes":
        myprint("you slowly walk into the forest.")
    elif answer == "no":
        myprint("You stand still at the edge of the forest thinking of how you arrived here.")
        myprint("You turn around to see if there is an exit")

        answer = scene(
            "As you walk along the dirt leading away from the forest you notice a monkey engulfed by shadow emerge infront of you.",
            "How do you react?",
            ["Run back to the forest", "fight the monkey head on!"])

        if answer == "fight the monkey head on!":
            myprint("the monkey is faster than usual due to it's shadowed form")
            myprint("It swiftly climbs onto your head and bites you in neck!")
            return False

        elif answer == "Run back to the forest":
            myprint("you run into the forest and hide behind a tree hoping the monkey doesn't see you")
            myprint("the monkey jumps back into the trees leaving you alone")

    area("Monkey Forest", "Home of Monkeys")

    answer = scene("you see someone leaning against a tree 20m away from you",
                   "will you talk to them?",
                   ["yes", "no"])

    if answer == "yes":
        myprint(f'{greeting2} {name}, {im2} {npc2}. nice to meet you.')
        myprint("You will need this sword, the monkeys in this forest are very aggresive since the land was engulfed.")
        myprint("You carry on through the forest")
        inventory.append("sword")

    elif answer == "no":
        myprint("You ignore the peron and carry on through the forest")

    answer = scene("whilst you are walking through the forest 5 monkeys drop down from the trees",
                   "how can you get past",
                   ["fight the monkeys", "carry on running through the forest", "surrender to the monkeys"])

    sword = "sword" in inventory

    if answer == "fight the monkeys":
        if sword is True:
            myprint("you fight off the monkeys with your sword and carry on through the forest!")

        elif sword is False:
            myprint("the monkeys swarm you and with no way of defending yourself you die.")
            return False
    elif answer == "carry on running through the forest":
        myprint("you carry on running but another group of monkeys falls infront of you.")
        myprint("You run through them also like the coward you are!")

    elif answer == "surrender to the monkeys":
        myprint("The monkeys tie you to tree and starve you.")
        return False

    myprint("after walking through the forest you find an oppening in the trees.")
    myprint("you enter the clearing...")

    bossName = "King of Bananas"
    if boss_fight(bossName) is True:

        answer = scene("At the end of the clearing you see a torch with a white flame and an eternal bonfire",
                       "Do you light it?", ["yes", "no"])

        if answer == "yes":
            fires_lit += 1
            myprint("you lit the Monkey forest's flame of light!")
        elif answer == "no":
            myprint("you didn't light the fire and the monkey forest remained in shadows")

        return True
    else:
        return False


# ???
def treasure_island(name,npc, npc2):
  global fires_lit
  
  area("Isle of ancient treasures", "buried with secrets")
  answer = scene("you see a chest on the ground", "do you open it?", ["yes", "no", "smack it!"])
  if answer == "yes":
    myprint("you opened the chest")
    myprint("and it was a mimick!")
    myprint("you manage to pull your fists out quick enough but it was close!")
  elif answer == "no":
    myprint("you carry on ignoring the chest")
  elif answer == "smack it!":
    myprint("the chest was a mimick!")
    myprint("when it died it dropped something")
    myprint("you found the attack multiplier spell")

def black_sea(name, npc, npc2):
    global fires_lit

    greeting, im = npcs[npc]

    myprint(Fore.WHITE + "you follow a path from the bonfire until you find yourself on a beach.")

    area("The Beach of Insanity", "where travellers lose their minds")
    answer = scene("There is a small wooden boat on the beach",
                   "will you sail it or explore the coast some more?",
                   ["sail", "explore"])

    if answer == "explore":
        myprint("you turn left and walk along the beach.")
        myprint("while you are exploring the beach something scuttles out of the water...")

        if boss_fight("Litius") is False:
            return False

        answer = scene("there is someone sitting on a rock behind the crab\'s corpse",
                       "will you talk to them?",
                       ["yes", "no"])

        if answer == "yes":
            myprint(f'{greeting} {name}, {im} {npc}. That\'s quite the feat you achieved. Killing that giant crab.')
            myprint("Thanks to you I can now get to my boat and sail to the island of treasure")
            myprint("legend has it a great knight got lost there and never returned home...")
            myprint("sorry for my waffling, take this axe as a token of my gratitude!")
            myprint(f'you run back to the boat before {npc} gets there and you sail away')
            inventory.append("axe")

        elif answer == "no":
            myprint("You ignore the person, return back to the boat and set sail!")

    elif answer == "sail":
        myprint("you set sail across...")

    area("The black sea", "an ocean, with no forgiveness")
    answer = scene("while you are sailing you see a shark circling you in the water",
                   "how do you fend it off",
                   ["try and sail faster", "stab it!", "punch it's nose then set sail again"])

    if answer == "try and sail faster":
        myprint("you pick up the pace but the shark can swim fast")
        myprint("it leaps out of the water and swallows you whole!")
        return False
    elif answer == "stab it!":
        if "sword" in inventory or "axe" in inventory:
            myprint("you stab the shark and it dies")
            myprint("you carry on sailing")
        else:
            myprint("you have nothing to stab the sword with!")
            myprint("the shark bit off your head")
            return False
    elif answer == "punch it's nose then set sail again":
        myprint("you stop the boat, jump out and punch the shark in the nose!")
        myprint("it is stunned for just enough time and you sail away from the shark")

    answer = scene("You see a storm on the horizon",
                   "where do you go?",
                   ["divert my course south", "divert my course north", "sail into the storm"])

    if answer == "sail into the storm":
        myprint("you sail directly into the storm")
        myprint("in the eye you find an island")
        myprint("and on it...")
        if boss_fight("Mr. Squid") is False:
            return False
        myprint("the storm faded with the squid")
        answer = scene("the squid left behind one of his tentacles", "do you pick it up?", ["yes", "no"])
        if answer == "yes":
            myprint("you pick up the tentacle and sail on")
            inventory.append("tentacle")
        elif answer == "no":
            myprint("you carry on with your journey!")
    elif answer == "divert my course south":
        myprint("you start sailing south and then go to sleep")
        myprint("after all you havent slept since you arrived here!")
        myprint("you wake up and you are on an island")

        area("The forgotten island", "a place of tranquillity")
        answer = scene("there is a lady lying down on the sand",
                       "Will you talk to her or carry on sailing to the marked location?", ["talk", "keep sailing"])

        if answer == "talk":
            myprint(f' hello {name} I am Spees, from Tenebrae (the city east of here)')
            myprint("I came here searching for my brother.")
            myprint("he was a very famous knight and he always strived to be better, more powerful")
            myprint("because of this he went searching for an island called \"treasure island\"")
            myprint("it is said that an anccient sword is kept there called \"The great knight sword\"")
            myprint(
                "it was named after a knight who used it to fight the king of shadows and stop the age of dark 1,000 years ago")
            myprint("my brother wanted to fight him (the king of shadows) but he never returned from his search")
            myprint("that is why I am here, to look for him so he can fight the king of shadows in Umbra castle.")

            answer = scene("", "will you help  me find him?", ["sure", "no thanks"])

            if answer == "sure":
                myprint("Thank you!")
                myprint("take this spear as a gift!")
                inventory.append("spear")
            elif answer == "no thanks":
                myprint("ok then")
            myprint("you get back in your boat and start sailing towards the marked location on your map")
    elif answer == "divert my course north":
        myprint("you quickly divert your course North to avoid the storms wrath")
        myprint("you sail through the whole night and finally see some land to your east")
        answer = scene("you also see a floating helmet to your north", "where will you go?",
                       ["towards the land", "towards the helmet"])
        if answer == "towards the land":
            myprint("yout turn east and set your course land!")
        elif answer == "towards the helmet":
            myprint("you sail in the direction of the helmet for several more hours")
            myprint("finally you arrive on the island")
            if treasure_island(name, npc, npc2) is True:
                myprint("you have survived the ilse of ancient treasures")
            else:
                return False


# ???
def die():
    x = input()
    area("You died", "Umbra will remain in shadow")



# ???
def story():

    npc = random.choice(list(npcs.keys()))
    npc2 = random.choice(list(npcs.keys()))
    # npc = list(npcs.keys())[-1]

    greeting, im = npcs[npc]

    print(Style.BRIGHT)
    name = input("What is your name?\n")
    myprint(f'{greeting} {name}, {im} {npc}. Welcome to...')

    area("Umbra", "The Land of Shadows")

    myprint(Fore.WHITE + "This land is plagued with the curse of the shadows.")
    myprint("The shadows can only be destroyed by lighting each regions flame of light.")
    myprint("Your journey will be cruel and unforgiving, but I trust you can cure the curse.")

    if monkey_forest(name, npc, npc2) is True:
        myprint(Fore.LIGHTYELLOW_EX + "You survived the Monkey Forest")

        if black_sea(name, npc, npc2) is True:
            myprint(Fore.LIGHTYELLOW_EX + "You survived the black sea")
        else:
            die()
    else:
        die()

    myprint(Fore.LIGHTYELLOW_EX +"Here is where the story ends...")


# Main function to run this script
def main():
    global myfile

    # Initialise colorama
    colorama.init()

    # run the story
    story()

    # Close the story output file
    myfile.close()


if __name__ == "__main__":
    main()
