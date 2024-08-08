from itertools import combinations

prime_map = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13,
    'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43,
    'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79,
    'w': 83, 'x': 89, 'y': 97, 'z': 101 }

def prime_hash(word: str):
  #calculates the prime hash value for a given word
        hash_value = 1
        for letter in word:
            hash_value *= prime_map[letter]
        return hash_value

class AnagramExplorer:
    def __init__(self, all_words: list[str]):
        self.__corpus = all_words
        self.anagram_lookup = self.build_lookup_dict() # Only calculated once, when the explorer object is created

    @property
    def corpus(self):
        return self.__corpus
    
    def is_valid_anagram_pair(self, pair:tuple[str], letters:list[str]) -> bool:
       '''Checks whether a pair of words:
            -are both included in the allowable word list (self.corpus)
            -are both at least 3 letters long (and the same)
            -form a valid anagram pair
            -consist entirely of letters chosen at the beginning of the game
       '''       
       word1, word2 = pair
       word1 = word1.lower()
       word2 = word2.lower()
       if word1 == word2:
           return False
       listt = [word1, word2]
       for word in listt:
           score = prime_hash(word)
           lscore = prime_hash(letters)
           if lscore % score != 0:
               return False
           if len(word) < 3:
               return False
           if word not in self.corpus:
               return False
       srt = list(listt[0])
       srt.sort()
       srt2 = list(listt[1])
       srt2.sort()
       if srt != srt2:
           return False
       return True
               
    def build_lookup_dict(self) -> dict:
        '''Creates a fast dictionary look-up (via either prime hash or sorted tuple) of all anagrams in a word corpus.
       
            Args:
                corpus (list): A list of words which should be considered

            Returns:
                dict: Returns a dictionary with  keys that return sorted lists of all anagrams of the key (per the corpus)
        '''
        dictionary = {}
        for word in self.__corpus:
           score = prime_hash(word)
           if score not in dictionary:
              dictionary[score] = [word]
           else:
              if score in dictionary.keys():
                dictionary[score].append(word)
        return dictionary


    def get_all_anagrams(self, letters: list[str]) -> set:
        '''Creates a set of all unique words that could have been used to form an anagram pair.
           Words which can't create any anagram pairs should not be included in the set.

            Ex)
            corpus: ["abed", "mouse", "bead", "baled", "abled", "rat", "blade"]
            all_anagrams: {"abed",  "abled", "baled", "bead", "blade"}

            Args:
              letters (list): A list of letters from which the anagrams should be created

            Returns:
              set: all unique words in corpus which form at least 1 anagram pair
        '''
        list1 = self.anagram_lookup.values() 
        lstt = set()
        lscore = prime_hash(letters)
        for lst in list1:
            if len(lst) > 1:
                for i in lst:
                    score = prime_hash(i)
                    if lscore % score == 0 and len(i) > 2:
                        lstt.add(i)

        return lstt
           
    def get_most_anagrams(self, letters:list[str]) -> str:
        '''Returns any word from one of the largest lists of anagrams that 
           can be formed using the given letters.
           
            Args:
              letters (list): A list of letters from which the anagrams should be created

            Returns:
              str: a single word from the largest anagram families
        '''
        lstt = self.get_all_anagrams(letters)
        hashlist = []
        for x in lstt:
            hash = prime_hash(x)
            hashlist.append(hash)
        temp = 0
        nlist = []
        for key in self.anagram_lookup:
            if key in hashlist and len(self.anagram_lookup[key]) > temp:
                temp = len(self.anagram_lookup[key])
        for key in self.anagram_lookup:
            if len(self.anagram_lookup[key]) == temp and key in hashlist:
                nlist.append(self.anagram_lookup[key][0])
        return nlist[0]


if __name__ == "__main__":
  words1 = [
     "abed","abet","abets","abut","acme","acre","acres","actors","actress","airmen","alert","alerted","ales","aligned","allergy","alter","altered","amen","anew","angel","angle","antler","apt",
     "bade","baste","bead","beast","beat","beats","beta","betas","came","care","cares","casters","castor","costar","dealing","gallery","glean","largely","later","leading","learnt","leas","mace","mane",
     "marine","mean","name","pat","race","races","recasts","regally","related","remain","rental","sale","scare","seal","tabu","tap","treadle","tuba","wane","wean"
  ]
  words2 = ["rat", "mouse", "tar", "art", "chicken", "stop", "pots", "tops" ]

  letters = ["l", "o", "t", "s", "r", "i", "a"]

  my_explorer = AnagramExplorer(words2)

  print(my_explorer.is_valid_anagram_pair(("rat", "tar"), letters))
  print(my_explorer.is_valid_anagram_pair(("stop", "pots"), letters))
  print(my_explorer.get_most_anagrams(letters))
  print(my_explorer.get_all_anagrams(letters))