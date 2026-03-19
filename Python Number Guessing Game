import random

lowest_num = 1
highest_num = 100
answer = random.randint(lowest_num, highest_num)
guesses = 0
is_running = True

print("Python Number Guessing Game")
print(f"Select a number between {lowest_num} and {highest_num}")

while is_running:
    guess = input("Guess a number: ")


    if guess.isdigit():
        guess = int(guess)
        guesses += 1

        if guess < lowest_num or guess > highest_num:
            print(f"Please enter a number between {lowest_num} and {highest_num}")

        elif guess > answer:
            print("Too high!")

        elif guess < answer:
            print("Too low!")

        if guess == answer:
            print(f"CORRECT! The number is: {answer}!")
            print(f"Total number of guesses: {guesses}!")
            is_running = False

    else:
        print("Invalid Input")
