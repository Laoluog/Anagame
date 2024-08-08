from itertools import combinations
from itertools import permutations

def build_sorted_hash_dict(corpus: list) -> dict:
    '''Creates a fast dictionary look-up of words in a word corpus by anagrammability.
    '''
    dictionary = {}
    for word in corpus:
        x = tuple(sorted(word))
        if x not in dictionary:
            dictionary[x] = [word]
        else:
            dictionary[x].append(word)
    sorted(dictionary)
    return dictionary


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

def build_prime_hash_dict(corpus):
    '''Creates a fast dictionary look-up of words in a word corpus by anagrammability.
    '''
    dictionary = {}
    

    for word in corpus:
        multscore = 1
        score = prime_hash(word)
        if score not in dictionary:
            temp = score
            multscore *= temp
            dictionary[multscore] = [word]
        elif score in dictionary.keys():
            dictionary[score].append(word)
        
    sorted(dictionary)
    print(dictionary)
    return dictionary


def get_most_anagrams(corpus:list)->list:
    '''Uses a fast dictionary look-up to explore all anagram combinations in a word corpus.
    '''
    anaglists = build_prime_hash_dict(corpus)
    list1 = []
    terms = []
    for key in anaglists:
        list1.append(key)
    for x in list1:
        terms.append(sorted(anaglists.get(x)))
    againterms = []
    for i in range(len(terms)):
        if len(terms[i]) > 1:
            againterms.append(terms[i])
    newlist = []
    temp = 0
    for z in againterms:
        if len(z) >= temp:
            temp = len(z)
    for a in againterms:
        if len(a) == temp:  
            newlist.append(a[0])

    newlist = sorted(newlist)

    return newlist
 

def get_all_anagrams(corpus:list[str])->set:
    '''Creates a set of all unique words in a word corpus that could have been used to form an anagram pair.
        Words which can't create any anagram pairs should not be included in the set.
    '''
    anaglists = build_prime_hash_dict(corpus)
    list1 = []
    terms = []
    for key in anaglists:
        list1.append(key)
    for x in list1:
        terms.append(sorted(anaglists.get(x)))
    
    againterms = []
    for i in range(len(terms)):
        if len(terms[i]) > 1:
            againterms.append(terms[i])

    
    newlist = []
    for i in range(len(againterms)):
        for j in range(len(againterms[i])):
            newlist.append(againterms[i][j])
    
    newlist = set(sorted(newlist))

    return newlist

if __name__ == "__main__":
    words1 = ["abed","abet","abets","abut","acme","acre","acres","actors","actress","airmen","alert","alerted","ales","aligned","allergy","alter","altered","amen","anew","angel","angle","antler","apt",
    "bade","baste","bead","beast","beat","beats","beta","betas","came","care","cares","casters","castor","costar","dealing","gallery","glean","largely","later","leading","learnt","leas","mace","mane",
    "marine","mean","name","pat","race","races","recasts","regally","related","remain","rental","sale","scare","seal","tabu","tap","treadle","tuba","wane","wean"]

    words2 = ["rat", "mouse", "tar", "art", "chicken", "stop", "pots", "tops" ]

    print(f"Sorting via the prime hashing function: {sorted(words1, key=prime_hash)}\n")
    
    print(f"Sorted tuple lookup dictionary: {build_sorted_hash_dict(words1)}")
    print(f"Prime hash lookup dictionary: {build_prime_hash_dict(words2)}\n")
    
    print(f"Most anagrams in words1:{get_most_anagrams(words1)}\n")
    print(f"Most anagrams in words2: {get_most_anagrams(words2)}")
