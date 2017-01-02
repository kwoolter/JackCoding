__author__ = 'user'

def tester(test : str):
    test = "xxx"

import kwutils

test = "zzz"
tester(test)
print(test)


answer = kwutils.confirm("Do you want to play again?")

print(answer)

choices = ("sword", "axe", "spear")

choice =kwutils.pick("Weapon", choices)
print(choice)



