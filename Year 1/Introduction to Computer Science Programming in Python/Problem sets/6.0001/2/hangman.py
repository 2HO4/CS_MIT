# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
WORDLIST_FILENAME = "words_v2.txt"
HIGH_SCORE = 'scores.txt'


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("\n\nLoading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random

    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program

wordlist = load_words()


def score_pos(score):
    """
    :return: int from 1 - 11
    """

    with open(HIGH_SCORE, 'r') as hs_file:
        c = 0
        for line in hs_file:
            c += 1
            if str(score)+'\n' == line:
                return int(c)
        return 11


def add_score(score):
    hs_file = open(HIGH_SCORE, 'r')
    with open(HIGH_SCORE, 'r') as hs_file:
        hs_list = hs_file.readlines()
        if len(hs_list) == 0:
            hs_list.append(str(score)+'\n')

        else:
            for i in range(len(hs_list)):
                if score >= float(hs_list[i]):
                    hs_list = hs_list[:i]+[str(score)+'\n']+hs_list[i:10]
                    break

            if len(hs_list) < 10:
                hs_list.append(str(score) + '\n')

    with open(HIGH_SCORE, 'w') as hs_file:
        hs_file.writelines(hs_list)


def reset_score():
    hs_file = open(HIGH_SCORE, 'w')
    print("\nLeaderboard reset...")


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

    ret = "_ "*(len(secret_word)-1) + "_"
    for i in letters_guessed:
        for j in range(len(secret_word)):
            if secret_word[j] == i:
                ret = ret[0:2*j] + i + ret[2*j+1:]
    n = 1
    while " " in ret:
        if n == len(ret) - 1:
            break

        ret, n = (ret[0:n]+ret[n+1:], n) if (ret[n-1] in string.ascii_lowercase and ret[n+1] in string.ascii_lowercase) else (ret, n+1)

    return ret


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    progress = get_guessed_word(secret_word, letters_guessed)
    return True if "_" not in progress else False


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    alp = string.ascii_lowercase
    for i in letters_guessed:
        alp = alp.replace(i, "")
        
    return alp


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    print("\n\n\n\n" +"Welcome to Hangman!".upper())
    print("\nRules:")
    print("- Having 6 guesses, you lose 2 of them if you gave a vowel but only 1 for a consonant.")
    print("- However, you lose nothing if your guess was correct!")
    print("- Please only input 1 letter; after 3 warnings, your remaining guesses will be affected.")
    print("\nAlright let's started! \nI'm thinking of", "an" if (str(len(secret_word))[-1] == "8" or len(secret_word) == 11) else "a", str(len(secret_word)) + "-letter word!\n\n\n")

    no_guesses = 6
    letters_guessed = []
    warn = 3
    rd = 1
    strks = 0
    h_strks = 0

    print("\n" + "-" * 86 + "\n")
    print("ROUND", str(rd) + ":")
    print(" Warnings:", warn)
    print(" Guesses:", no_guesses)
    print(" Available letters:", get_available_letters(letters_guessed), "\n")

    while no_guesses > 0:
        p_guess = input("Your guess: ")

        if len(p_guess) == 1 and p_guess not in letters_guessed and p_guess in string.ascii_lowercase + string.ascii_uppercase:
            p_guess = p_guess.lower()
            letters_guessed.append(p_guess)

            if p_guess in secret_word:
                strks += 1
                if h_strks < strks:
                    h_strks = strks
                if is_word_guessed(secret_word, letters_guessed):
                    break

                else:
                    print("Good job, that's correct!", " "*8, "Progress:", get_guessed_word(secret_word,
                                                                                           letters_guessed))

            else:
                streaks = 0
                print("Oops! That isn't in my word.", " "*5, "Progress:", get_guessed_word(secret_word, letters_guessed))
                no_guesses -= 2 if p_guess in "aeiou" else 1

            if no_guesses > 0:
                rd += 1
                print("\n" + " "*24 + ".  .  .  " * int(24/5))
                print("ROUND", str(rd) + ":")

        else:
            if warn > 0:
                warn -= 1

            else:
                no_guesses -= 1

            print("\nTry again!", end=' ')

            if len(p_guess) != 1:
                print("Please enter just 1 letter.")

            if p_guess in letters_guessed:
                print("You've already given that guess.")

            for t in p_guess:
                if t not in string.ascii_lowercase + string.ascii_uppercase:
                    print("It should be an English alphabet letter.")

            print(" You have", warn, "free warnings left.\n" if warn>1 else "free warning left.\n")

        print(" Guesses left:", no_guesses)
        print(" Available letters:", get_available_letters(letters_guessed), "\n")

    print("-" * 86, "\n\nGAME ENDED!\n")
    uni_l = 0
    for u in letters_guessed:
        uni_l += 1 if u in get_guessed_word(secret_word, letters_guessed) else 0

    if is_word_guessed(secret_word, letters_guessed):
        score = round((1 + 0.5 * abs(7 - len(secret_word))) \
                * len(get_guessed_word(secret_word, letters_guessed).replace(" ", "").replace("_", "")) \
                * uni_l / (1 + rd - uni_l) + no_guesses + warn\
                + h_strks ** 2.4, 1)

        add_score(score)
        pos = score_pos(score)
        th = "st"
        if pos == 2:
            th = "nd"

        elif pos == 3:
            th = "rd"

        else:
            th = "th"

        print("Congrats, you did it! It was indeed \""+secret_word.capitalize()+"\"!")

        if pos == 1:
            print('\n'+random.choice(['TOP OF THE WORLD!', 'BEST SCORER!', 'THE GREATEST!']))
            print(f'You\'ve just reached the highest place in the human history after achieving {score}!')

        elif pos != 11:
            print('\n'+random.choice(['Huge record!', 'Great score!', 'You\'re so smart!', 'High achiever!']))
            print(f'With {score}, you\'re the {str(pos)+th} most intelligent person in the world!')

        else:
            print("Your score is so high too:", score)

    else:
        score = round((1 + 0.5 * abs(7 - len(secret_word))) \
                * len(get_guessed_word(secret_word, letters_guessed).replace(" ", "").replace("_", "")) \
                * uni_l / (1 + rd - uni_l) + no_guesses + warn\
                + h_strks ** 2.4, 1)

        add_score(score)
        pos = score_pos(score)
        if pos == 2:
            th = "nd"

        elif pos == 3:
            th = "rd"

        else:
            th = "th"

        print("I'm sorry, you will win next time! The word was \""+secret_word.capitalize()+"\".")

        if pos == 1:
            print('\nBUT...' + random.choice(['TOP OF THE WORLD!', 'BEST SCORER!', 'THE GREATEST!']))
            print(f'You\'ve just reached the highest place in the human history after achieving {score}!')

        elif pos != 11:
            print('\nNevertheless,' + random.choice(['huge record!', 'great score!', 'you\'re so smart!',
                                                 'high achiever!']))
            print(f'With {score}, you\'re the {str(pos) + th} most intelligent person in the '
                  f'world!')

        else:
            print("Still, your score is quite impressive:", score)

    return score, str(pos)+th


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''

    mnw = my_word.replace(" ", "")
    for i in range(len(mnw)):
        if len(mnw) != len(other_word):
            return False
        else:
            if mnw[i] != other_word[i] and mnw[i] != "_":
                return False

            elif i == len(other_word)-1:
                return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    ret = []
    for i in wordlist:
        if match_with_gaps(my_word, i):
            ret.append(i)

    return "Possible matches are:\n" + " " + ", ".join(ret)


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    print("\n\n\n\n" +"Welcome to Hangman Special Edition!".upper())
    print("\nRules:")
    print("- Having 6 guesses, you lose 2 of them if you gave a vowel but only 1 for a consonant.")
    print("- However, you lose nothing if your guess was correct!")
    print("- Please only input 1 letter; after 3 warnings, your remaining guesses will be affected.")
    print("- However, if you're stuck, entering an \"*\" may save you! You only have 1 asterisk per game, "
          "so use it wisely.")
    print("\nAlright let's started! \nI'm thinking of", "an" if (str(len(secret_word))[-1] == "8" or len(secret_word) == 11) else "a", str(len(secret_word)) + "-letter word!\n\n\n")

    no_guesses = 6
    letters_guessed = []
    warn = 3
    rd = 1
    strks = 0
    h_strks = 0
    pow = 1

    print("\n" + "-" * 86 + "\n")
    print("ROUND", str(rd) + ":")
    print(" Warnings:", warn)
    print(" Guesses:", no_guesses)
    print(" Available letters:", get_available_letters(letters_guessed), "\n")

    while no_guesses > 0:
        p_guess = input("Your guess: ")

        if p_guess == "*" and pow == 1:
            print("\n" + show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
            pow -= 1
            rd += 1
            print("\n" + " " * 24 + ".  .  .  " * int(24 / 5))
            print("ROUND", str(rd) + ":")

        elif len(p_guess) == 1 and p_guess not in letters_guessed and p_guess in string.ascii_lowercase + \
            string.ascii_uppercase:
            p_guess = p_guess.lower()
            letters_guessed.append(p_guess)

            if p_guess in secret_word:
                strks += 1
                if h_strks < strks:
                    h_strks = strks
                if is_word_guessed(secret_word, letters_guessed):
                    break

                else:
                    print("Good job, that's correct!", " "*8, "Progress:", get_guessed_word(secret_word, letters_guessed))

            else:
                streaks = 0
                print("Oops! That isn't in my word.", " "*5, "Progress:", get_guessed_word(secret_word, letters_guessed))
                no_guesses -= 2 if p_guess in "aeiou" else 1

            if no_guesses > 0:
                rd += 1
                print("\n" + " "*24 + ".  .  .  " * int(24/5))
                print("ROUND", str(rd) + ":")


        else:
            if warn > 0:
                warn -= 1

            else:
                no_guesses -= 1

            print("\nTry again!", end=' ')

            if p_guess == "*":
                print("Your asterisk could only be used once.")

            if len(p_guess) != 1:
                print("Please enter just 1 letter.")

            if p_guess in letters_guessed:
                print("You've already given that guess.")

            for t in p_guess:
                if t not in string.ascii_lowercase + string.ascii_uppercase:
                    print("It should be an English alphabet letter.")

            print("You have", warn, "free warnings left.\n" if warn>1 else "free warning left.\n")

        print(" Guesses left:", no_guesses)
        print(" Available letters:", get_available_letters(letters_guessed), "\n")

    print("-" * 86, "\n\nGAME ENDED!\n")

    uni_l = 0
    for u in letters_guessed:
        uni_l += 1 if u in get_guessed_word(secret_word, letters_guessed) else 0

    if is_word_guessed(secret_word, letters_guessed):
        score = round((1 + 0.5 * abs(7 - len(secret_word))) \
                * len(get_guessed_word(secret_word, letters_guessed).replace(" ", "").replace("_", "")) \
                * uni_l / (1 + rd - uni_l) + no_guesses + warn\
                + h_strks ** 2.4 + 30 * pow, 1)

        add_score(score)
        pos = score_pos(score)
        if pos == 2:
            th = "nd"

        elif pos == 3:
            th = "rd"

        else:
            th = "th"

        print("Congrats, you did it! It was indeed \""+secret_word.capitalize()+"\"!")

        if pos == 1:
            print('\n'+random.choice(['TOP OF THE WORLD!', 'BEST SCORER!', 'THE GREATEST!']))
            print(f'You\'ve just reached the highest place in the human history after achieving {score}!')

        elif pos != 11:
            print('\n'+random.choice(['Huge record!', 'Great score!', 'You\'re so smart!', 'High achiever!']))
            print(f'With {score}, you\'re the {str(pos)+th} most intelligent person in the world!')

        else:
            print("Your score is so high too:", score)

    else:
        score = round((1 + 0.5 * abs(7 - len(secret_word))) \
                * len(get_guessed_word(secret_word, letters_guessed).replace(" ", "").replace("_", "")) \
                * uni_l / (1 + rd - uni_l) + no_guesses + warn\
                + h_strks ** 2.4 + 12 * pow, 1)

        add_score(score)
        pos = score_pos(score)
        th = "st"
        if pos == 2:
            th = "nd"

        elif pos == 3:
            th = "rd"

        else:
            th = "th"

        print("I'm sorry, you will win next time! The word was \"" + secret_word.capitalize() + "\".")

        if pos == 1:
            print('\nBUT...' + random.choice(['TOP OF THE WORLD!', 'BEST SCORER!', 'THE GREATEST!']))
            print(f'You\'ve just reached the highest place in the human history after achieving {score}!')

        elif pos != 11:
            print('\nNevertheless,' + random.choice(['huge record!', 'great score!', 'you\'re so smart!',
                                                 'high achiever!']))
            print(f'With {score}, you\'re the {str(pos) + th} most intelligent person in the '
                  f'world!')

        else:
            print("Still, your score is quite impressive:", score)

    return score, str(pos)+th


def repeated_hangman(game_type):
    secret_word = choose_word(wordlist)
    high_score, high_pos = game_type(secret_word)
    play_again = input('\nDo you want to play again?\nAnswer: ')
    while True:
        if play_again in ('No', 'no'):
            print(f'\nThank you for playing, your highest achievement in this play '
                  f'was {high_score}', end='')
            print(f', ranked {high_pos} in Hangman World Leaderboard.\nSee you again!') \
                if high_pos != '11th' else print('.\nSee you again!')
            break
        elif play_again in ('Yes', 'yes'):
            score, pos = game_type(choose_word(wordlist))
            high_score = score if score > high_score else high_score
            high_pos = pos if int(pos[:-2]) < int(high_pos[:-2]) else high_pos
        else:
            print('\nInvalid answer, please response \'Yes\'/\'yes\' or \'No\'/\'no\'.')
        play_again = input('\nDo you want to play again?\nAnswer: ')



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines.

    # reset_score()

    # Just 1 game
    # secret_word = choose_word(wordlist)
    # hangman_with_hints(secret_word)

    # Repeated games
    repeated_hangman(hangman_with_hints)

