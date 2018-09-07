import random

letters = 'abcdefghijklmnopqrstuvwxyz'

#get a random letter
letter = letters[random.randint(0,25)]

#loop until the user guesses correctly
while True:
    #prompt them to type a letter
    guess = input("Type a lower-case letter: ")
    #check that it’s actually a letter
    if guess not in letters:
        print("That is not a lower-case letter.")
        continue
    #if they’re right
    if guess == letter:
        print("That’s right!")
        break
    #give them a hint if they’re wrong
    if guess > letter:
        print("It’s earlier in the alphabet.")
    else:
        print("It’s later in the alphabet.")
