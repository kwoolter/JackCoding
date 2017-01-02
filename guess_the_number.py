__author__ = 'user'

import random

# My first Python program

print("Welcome to the game!")

name = input("What is your name?")

print("Well," +  name + ", I am thinking of a number between 1 and 20.")

number = random.randint(1,20)

# print("I thought of a number " + str(number))

guess = 0

while guess != number:
    guess = int(input("Take a guess."))

    if guess == number:
        print("Well done " + name +" you guessed the number that I thought of")

    elif guess < number:
        print("Your guess is too low.")

    elif guess > number:
        print ("your guess is too high")


print("The End!")


exit(-999)
