import os
import random
import time

#Run with python3 StringGuesser.py

def main():
    os.system('clear')
    user_input = input("Enter your string to be guessed: ")
    GuessLoop(user_input)


def GuessLoop(word):  
    os.system('clear')
    guessedRight = False
    wordLength = len(word)
    attempts = 0
    alreadyGuessed = []
    start_time = time.time()
    total_possibilities = len(letters) ** wordLength
    probability = 1 / total_possibilities

    while not guessedRight :
        guessedWord = ""
        #Create guess word
        for i in range(wordLength):  
            guessedWord += letters[random.randint(0, len(letters) - 1)]
        if guessedWord in alreadyGuessed:
            continue
        attempts += 1
        alreadyGuessed.append(guessedWord)

        #timer
        elapsed_time = time.time() - start_time
        formatted_time = format_time(elapsed_time)

        # Calculate luckiness
        luckiness = (1 - (attempts - 1) / (total_possibilities - 1)) * 100

        print(f"|     {guessedWord}     |     {attempts:,}/{total_possibilities:,}     |     {formatted_time}     |     {luckiness:.2f}%     |")
        guessedRight = guessedWord == word

    print(f"\nPerfect match found! It only took {attempts:,} out of {total_possibilities:,} attempts and {formatted_time}.")
    print(f"You were {luckiness:.2f}% lucky.\n")


letters = list("abcdefghijklmnopqrstuvwxyz ")  

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{int(minutes)}m, {seconds:.2f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{int(hours)}h, {int(minutes)}m, {seconds:.2f}s"

if __name__ == "__main__":
    main()