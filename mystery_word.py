import random
import string
#creating normal text without whitespace, digits, and capital letters
def normal_text(text):
        text = text.casefold()  
        valid_chars = string.ascii_letters + string.whitespace + string.digits        
        new_text = ""
        for char in text:
            if char in valid_chars:
                new_text += char
        text = new_text
        text = text.replace("\n", " ")
        text = remove_words(text)
        return text
#creating the variable "hidden word"
def hide_the_word(word):
    hidden_word = {}
    idx = 0
    for letter in word:
        hidden_word[idx] = '_'
        idx += 1
    return hidden_word
#Creating a way to get rid of dashes and replace them with letters.
def final_hidden_word(hidden_word, your_word, guess):
    idx = 0    
    for letter in your_word:
        if guess == letter and hidden_word[idx] == '_':
            hidden_word[idx] = letter
        idx += 1
    return hidden_word
#creating a way to keep track of the letters guessed and compare them to if they're in the word 
def guess_right(word, guess, guesses):
    for letter in word:
        if letter == guess and guess not in guesses:
            print ("Lucky guess.")
            return True
        if letter == guess and guess in guesses:
            print ("You fool, you already guessed that letter!")
            return False
        if letter != guess and guess in guesses:
            return False           
        if letter != guess:
            continue
    return True
#Needed to edit out words less than 4 digits
def remove_words(text):
    words = []
    for word in text.split(" "):
        if word != '' and len(word) >= 4:
            words.append(word) 
    return words
#Created difficulty settings Easy=4-6 characters, Normal=6-8 characters, Hard=everything above 8.
def difficulty_list(text, difficulty):
    list = normal_text(text)
    new_list = []
    if difficulty == "easy":        
        new_list = [word for word in list if word != '' and len(word) >= 4 and len(word) <= 6]        
    if difficulty == "normal":
        new_list = [word for word in list if word != '' and len(word) >= 6 and len(word) <= 8]
    if difficulty == "hard":
        new_list = [word for word in list if word != '' and len(word) >= 8]           
    return new_list           
#Adds letters to "hidden word" when user guesses them
def show_mystery_word(hidden_word):
    display_word = ''
    for letter in hidden_word:
        display_word += hidden_word[letter]
    return display_word
#Creates the amount of remaining guesses a user has before game ends.
def remaining_guesses (word, guess, guesses):
    guess_limit = True
    for letter in word:
        if letter == guess and guess not in guesses:
            guess_limit = True
            break
        if letter == guess and guess in guesses:
            guess_limit = True
            break
        if letter != guess and guess in guesses:
            guess_limit = True
            break    
        if letter != guess: 
            guess_limit = False
            continue
    return guess_limit
#Gives the user the option to play again
def continue_play ():
    play_again = input ("Care to try again? (y/n or yes/no)").lower()
    if play_again.isalpha() and play_again == "y" or play_again == "yes":
        print ("Alright, may the force be with you!")
        return True
    if play_again.isalpha() and play_again == "n" or play_again == "no":
        print ("Coward.")
        return False 
#While the game is being played it will show this text initially prompting the user to guess a letter.
game_again = True
while game_again:
    game_on = True
    while game_on:
        print("Welcome to Hang-man! Er...Mystery word!")
        print("In this non violent game you have to guess the mystery word.")
        print("If you guess 8 letters not in the word you will lose, although don't worry...")
        print("no one will be harmed if you lose!")
        print("What level of difficulty would you like to play on?")
        #Lets user pick difficulty
        difficulty = input("(easy, normal, hard): ")
        if difficulty.isalpha() and difficulty == 'easy' or difficulty == 'normal' or difficulty == 'hard':
            #Line above this comment calls back to previous function depending on what user inputs and selects difficulty based on what is inputted.
            with open("words.txt") as file:
                text = file.read()
                your_word = difficulty_list(text, difficulty)
                your_word = random.choice(your_word)
                hidden_word = hide_the_word(your_word)
                display_word = show_mystery_word(hidden_word)
                print ("Your word "+" ".join(display_word))
                #Calls the text file to randomly pick a word and hides it after the text has all been normalized.
                guesses_left = 8
                guesses = []
                updated_word = {}
                #If user still has guesses left display the amount they have left and prompt them to guess more
                while guesses_left != 0 and your_word != display_word:
                    print (f"You've guessed: {guesses}.")
                    guess = input ("Guess a letter: ").lower()
                    if guess.isalpha() and len(guess) == 1:
                        #Line above comment makes it so that the program checks to see if the user inputed a letter
                        #Also checks the length of the guess to make sure that it does not equal zero(is an applicable guess)
                        check = remaining_guesses(your_word, guess, guesses)
                        if check == False:
                            guesses_left -= 1
                            print ("You fool, that letters not in the word.")
                            #Checks remaining guesses, if not equal zero displays "print" and deducts 1 from guesses_left
                        if guess_right(your_word, guess, guesses) == True:
                            guesses.append(guess)
                            #If user guesses right add guessed letter to guesses 
                        print (f"You only have {guesses_left} left.")
                        updated_word = final_hidden_word(hidden_word, your_word, guess)
                        display_word = show_mystery_word(updated_word)
                        print (" ".join(display_word))
                    else:
                        print ("Stop cheating. Only enter one letter at a time.")
            game_on = False
        else:
            print ("What difficulty?.")
    if guesses_left != 0 and your_word == display_word:        
        print ("Good work, you saved a stick figures life!")           
        game_again = continue_play()
    if guesses_left == 0:
        print ("You lost! You are hated by the whole stick figure community.")
        print (f"This was the word you were too dumb to guess: {your_word.upper()}")
        game_again = continue_play()
    