from globals import myfile
from colorama import Fore, Style

# myprint function (substitue print with myprint and put it into the file)
def myprint(text, press_enter=True):
    print(text)
    print(text, file=myfile, flush=True)
    if press_enter is True:
        input()

# pick function for creating menus and making them idiots proof
def pick(choices):

    myprint(Fore.WHITE + Style.BRIGHT, press_enter = False)

    # while loop to make sure you enter a valid value
    valid = False
    while valid is False:

        # printing the options to choose from
        for i, option in enumerate(choices):
            myprint(f"\t{i + 1}) {option}", press_enter = False)

        # getting the input
        x = input("select an option?\n")

        # is the input an integer?
        try:
            x = int(x)

            # is the input in the range of choices
            if x in range(1, len(choices) + 1):
                valid = True
            # if the input isn't valid but is an integer print...
            else:
                myprint(f"{x} is not a valid option, please try again")

        # if the input isn't an integer print...
        except:
            myprint(f"{x} is not a number, please select the numbers not their answers.")

    # return what you picked from the choices
    return choices[x - 1]

