import os
import random
import time
import smtplib
import sys
import config

#Run with python3 StringGuesser.py
#If you want it to text you when done, you must make a config file. 

ENABLE_NOTIFICATIONS = False

letters = list("abcdefghijklmnopqrstuvwxyz ")#ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*")  

def main():

    clear()
    user_input = input("Enter your string to be guessed: ")
    mode = input("\nChose mode and enter to start: \n(1) Random\n(2) Sequential (Statistically faster...)\n(3) Efficient (No Console)\n(4) Wheel of Fortune\n")
    if mode == "1" :
        modeInfo = f"\nWord: {user_input}\nMode: Random\n"
        GuessLoop(user_input, modeInfo)
    if mode == "2" :
        modeInfo = f"\nWord: {user_input}\nMode: Sequential\n"
        GuessLoopSeq(user_input, modeInfo)
    if mode == "3" :
        modeInfo = f"\nWord: {user_input}\nMode: Efficient\n"
        GuessLoopEfficient(user_input, modeInfo)
    if mode == "4" :
        modeInfo = f"\nWord: {user_input}\nMode: Wheel of Fortune\n"
        GuessLoopWOF(user_input, modeInfo)

def GuessLoop(word, modeInfo):  
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

    successMessage = f"{modeInfo}\nPerfect match found! It only took {attempts:,} out of {total_possibilities:,} attempts and {formatted_time}. You were {luckiness:.2f}% lucky.\n "

    print(f"{successMessage}")
    send_message(successMessage)

def GuessLoopSeq(word, modeInfo):  
    clear()
    guessedRight = False
    wordLength = len(word)
    attempts = 0
    start_time = time.time()
    total_possibilities = len(letters) ** wordLength

    indices = [0] * wordLength  

    while not guessedRight:
        attempts += 1
        guessedWord = "".join(letters[i] for i in indices)

        # Timer
        elapsed_time = time.time() - start_time
        formatted_time = format_time(elapsed_time)

        # Calculate estimated time left
        attempts_per_second = attempts / elapsed_time
        time_left = format_time((total_possibilities - attempts) / attempts_per_second)

        print(f"|     {guessedWord}     |     {attempts:,}/{total_possibilities:,}     |     {formatted_time}     |     {time_left}     |")
        guessedRight = guessedWord == word

        #simple base counter used to "count" the characters
        for i in range(wordLength - 1, -1, -1):
            if indices[i] < len(letters) - 1:
                indices[i] += 1
                break
            indices[i] = 0

    successMessage = f"{modeInfo}\nPerfect match found! It only took {attempts:,} out of {total_possibilities:,} attempts and {formatted_time}.\n "

    print(f"{successMessage}")
    send_message(successMessage)

def GuessLoopEfficient(word, modeInfo):  
    #letters = list("etaoinshrdlcumwfgypbvkjxqz ") #more efficient sorting of letters
    clear()
    guessedRight = False
    wordLength = len(word)
    start_time = time.time()

    indices = [0] * wordLength  

    while not guessedRight:
        guessedWord = "".join(letters[i] for i in indices)

        guessedRight = guessedWord == word

        for i in range(wordLength - 1, -1, -1):
            if indices[i] < len(letters) - 1:
                indices[i] += 1
                break
            indices[i] = 0

    elapsed_time = time.time() - start_time
    formatted_time = format_time(elapsed_time)
    successMessage = f"{modeInfo}\nPerfect match found! It only took {formatted_time}.\n "

    print(f"{successMessage}")
    send_message(successMessage)

def GuessLoopWOF(word, modeInfo): 
    #Since this is incredibly fast I am doing all letters, numbers, and symbols
    letters = list("abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*?")  
    clear()
    guessedRight = False
    wordLength = len(word)
    attempts = 0
    start_time = time.time()
    
    guessedWord = ""
    for i in range(wordLength) :
        guessedWord += "_"

    while not guessedRight :
        #Randomly generate characters, if correct, put in slot
        for i in range(wordLength):  
            newChar = letters[random.randint(0, len(letters) - 1)]
            if newChar == word[i] :
                guessedWord = list(guessedWord)
                guessedWord[i] = newChar
                guessedWord = "".join(guessedWord)

        
        attempts += 1

        #Timer
        elapsed_time = time.time() - start_time
        formatted_time = format_time(elapsed_time)

        print(f"|     {guessedWord}     |     {attempts:,}     |     {formatted_time}     |")
        time.sleep(0.08)
        guessedRight = guessedWord == word

    successMessage = f"{modeInfo}\nPerfect match found! It only took {attempts:,} attempts and {formatted_time}.\n "

    print(f"{successMessage}")
    send_message(successMessage)

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
    if not ENABLE_NOTIFICATIONS:
        return
    auth = (config.EMAIL, config.PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], config.NUMBER, message)

if __name__ == "__main__":
    main()