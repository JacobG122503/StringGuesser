import os
import random
import time
import smtplib
import sys
import config

#Run with python3 StringGuesser.py
#If you want it to text you when done, you must make a config file. 

def main():
    clear()
    user_input = input("Enter your string to be guessed: ")
    GuessLoop(user_input)


def GuessLoop(word):  
    clear()
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
        
        #Calculate Chance
        chance = (1/(total_possibilities - attempts)) * 100
        
        attempts += 1
        alreadyGuessed.append(guessedWord)

        #Timer
        elapsed_time = time.time() - start_time
        formatted_time = format_time(elapsed_time)

        #Calculate estimated time left
        attempts_per_second = attempts / elapsed_time
        time_left = format_time((total_possibilities - attempts) / attempts_per_second)


        #Calculate luckiness
        luckiness = (1 - (attempts - 1) / (total_possibilities - 1)) * 100

        print(f"|     {guessedWord}     |     {attempts:,}/{total_possibilities:,}     |     {formatted_time}     |     {luckiness:.2f}%     |     {chance:.5f}%     |     {time_left}     |")
        guessedRight = guessedWord == word

    successMessage = f"\nPerfect match found! It only took {attempts:,} out of {total_possibilities:,} attempts and {formatted_time}. You were {luckiness:.2f}% lucky.\n "

    print(f"{successMessage}")
    send_message(successMessage)



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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def send_message(message):
    auth = (config.EMAIL, config.PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], config.NUMBER, message)

if __name__ == "__main__":
    main()