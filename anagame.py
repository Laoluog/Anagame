import time
import random
import math
from valid_anagame_words import get_valid_word_list
from AnagramExplorer import AnagramExplorer


def generate_letters(fun_factor: int, distribution: str, explorer:AnagramExplorer) -> list:
   '''Generates a list of 7 randomly-chosen lowercase letters which can form at least 
      fun_factor unique anagramable words
   '''
   letter_value = {'a':1 , 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j':8, 'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':8, 'w':4, 'x':8, 'y':4, 'z':10}
   scrabbleletters = ['a']*9 + ['b']*2 + ['c']*2 + ['d']*4 + ['e']*12 + ['f']*2 +['g']*3 + ['h']*2 + ['i']*9 + ['m']*2 + ['n']*6 + ['o']*8 + ['p']*2 + ['q'] + ['r']*6 + ['s']*4 + ['t']*6 + ['u']*4 + ['v']*2 + ['w']*2 + ['x'] + ['y']*2 + ['z']
   wordlist = []
   alpha = []
   for k in letter_value.keys():
      alpha.append(k)
   if distribution == "scrabble":
      wordlist = random.sample(scrabbleletters, k=7)
   if distribution == "uniform":
      wordlist = random.choices(alpha, k=7)
   while len(explorer.get_all_anagrams(wordlist)) < fun_factor and distribution == "scrabble":
      wordlist = random.sample(scrabbleletters, k=7)      
   while len(explorer.get_all_anagrams(wordlist)) < fun_factor and distribution == "uniform":
      wordlist = random.choices(alpha, k=7)
   if len(explorer.get_all_anagrams(wordlist)) >= fun_factor:
      return wordlist
      
      

def parse_guess(guess:str) -> tuple:
   '''Splits an entered guess into a two word tuple with all white space removed
   '''
   wordx = []

   guess = guess.strip("")
   if guess.count(",") == 0 or guess.count(",") > 1:
      return ("", "")
   if guess.count(",") == 1:
      wordx = guess.split(",")
      word1 = wordx[0].strip()
      word2 = wordx[1].strip()
      return (word1, word2)

def play_game(time_limit: int, letters: list, explorer:AnagramExplorer) -> list:
    '''Plays a single game of AnaGame
   '''
    guesses = [] 
    quit = False

    start = time.perf_counter() #start the stopwatch (sec)
    stop = start + time_limit

    while time.perf_counter() < stop and not quit:
        guess = input('')
        if guess.strip() == "quit":
            quit = True
        elif guess.strip() == "hint":
            print(f"Try working with: {explorer.get_most_anagrams(letters)}")
        else:
          tuple_guess = parse_guess(guess)
          if len(tuple_guess[0]) > 1:
            guesses.append(tuple_guess)
          else:
            print("Invalid input")

        print(f"{letters} {round(stop - time.perf_counter(), 2)} seconds left")

    return guesses

def calc_stats(guesses: list, letters: list, explorer: AnagramExplorer) -> dict:
    '''Aggregates several statistics into a single dictionary with the following key-value pairs:
    '''
    stats = {}
    stats["valid"] = []   #list of tuples
    stats["invalid"] = [] #list of tuples
    stats["score"] = 0    #total score per the rules of the game
    stats["accuracy"] = 0 #truncated int percentage representing valid player guesses out of all player guesses
    stats["skill"] = 0    #truncated int percentage representing unique guessed words out of all possible unique anagram words
    stats["guessed"] = set() #unique valid guessed words
    stats["not guessed"] = set() #unique words the player could have guessed, but didn’t

    if guesses == []:
       stats["not guessed"] = set(explorer.get_all_anagrams(letters))
       return stats 
    guesseslist = []
    
    for i in set(guesses):
       if explorer.is_valid_anagram_pair(i, letters) and sorted(set(i)) not in guesseslist:
          stats["valid"].append(tuple(sorted(i)))
          guesseslist.append(sorted(set(i)))
          stats["score"] += (len(i[0]) - 2)
          stats["guessed"].add(i[0])
          stats["guessed"].add(i[1])

       else:
          stats["invalid"].append(i)
    if len(stats["valid"]) == 0:
       stats["accuracy"] = 0
    elif len(stats["invalid"]) == 0:
       stats["accuracy"] = 100
    else:
       stats["accuracy"] = int((len(stats["valid"]))*100/len(guesses))
    stats["skill"] = int ((len(stats["guessed"]))*100/(len(explorer.get_all_anagrams(letters))))
    stats["not guessed"] = set(explorer.get_all_anagrams(letters)) - stats["guessed"]


        
    return stats

def display_stats(stats):
    '''Prints a string representation of the game results
    '''
    
    print("\nThanks for playing Anagame!\n")
    print("------------")
    print(f"Accuracy: {round(stats['accuracy'], 2)}%")
    print(f" valid guesses ({len(stats['valid'])}):", end=" ")
    for guess in stats['valid']:
        print(f"  {guess[0]},{guess[1]}", end=" ")
    print(f"\n invalid guesses ({len(stats['invalid'])}):", end=" ")
    for guess in stats['invalid']:
        print(f"  {guess[0]},{guess[1]}", end=" ")
    print("\n------------")
    print(f"Skill: {stats['skill']}% ")
    print(f" Unique words used:", end=" ")
    for guess in sorted(stats['guessed']):
        print(f"  {guess}", end=" ")
    print(f"\n Words you could have used:", end=" ")
    for guess in sorted(stats['not guessed']):
        print(f"  {guess}", end=" ")
    print("\n------------")
    print(f"AnaGame - Final Score: {stats['score']}")
    print("------------")


if __name__ == "__main__":
  time_limit = 60

  explorer = AnagramExplorer(get_valid_word_list()) #helper object
  letters = generate_letters(100, "uniform", explorer)

  print("\nWelcome to Anagame!\n")
  print("Please enter your anagram guessess separated by a comma: eat,tea")
  print("Enter 'quit' to end the game early, or 'hint' to get a useful word!\n")
  print(f"You have {time_limit} seconds to guess as many anagrams as possible!")
  print(f"{letters}")

  guesses = play_game(time_limit, letters, explorer)
  stats_dict = calc_stats(guesses, letters, explorer)
  display_stats(stats_dict)