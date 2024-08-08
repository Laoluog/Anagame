from itertools import permutations

def basic_checks(word1:str, word2:str)-> tuple[bool, str, str]:
    '''Implements top-level checks common to each is_anagram approach. 
    '''
    word1 = word1.lower()
    word2 = word2.lower()
    if word1 == word2:
        return False, word1, word2
    newword = ""
    newword2 = ""
    for char in word1:
        if ord(char) <= 122 and ord(char) >= 97:
            newword += char
    for char in word2:
        if ord(char) <= 122 and ord(char) >= 97:
            newword2 += char
    word1 = newword
    word2 = newword2
    if len(newword) != len(newword2):
        return False, word1, word2
    if len(newword) <= 1 or len(newword2) <= 1:
        return False, word1, word2
    return True, word1, word2
    

def is_anagram_exhaustive(word1:str, word2:str)->bool:
    '''Generate all possible permutations of the first word until you find one that is the second word.
       If no permutation of the first word equals the second word, the two are not anagrams.
    '''
    checks = basic_checks(word1, word2)
    if not checks[0]:
        return False
    word1 = checks[1]
    word2 = checks[2]

    perms = permutations(list(word1))
    if tuple(word2) not in (list(perms)):
        return False
    else:
        return True

def is_anagram_checkoff(word1:str, word2:str)->bool:
    '''Create a parallel list-based version of the second word (strings are immutable).
       Check off letters in the list as they are found by setting the value to None.
    '''
    checks = basic_checks(word1, word2)
    if not checks[0]:
        return False
    word1 = checks[1]
    word2 = checks[2]
    
    lst = list(word2)
    wordval = len(list(word2))
    for char in word1 :
        if char in lst:
            lst.remove(char)
    return not bool(lst)
            
def is_anagram_lettercount(word1:str, word2:str)->bool:

    checks = basic_checks(word1, word2)
    if not checks[0]:
        return False
    word1 = checks[1]
    word2 = checks[2]
    
    list1 = [0]*26
    list2 = [0]*26

    for char in word1.lower():
        list1[ord(char) - 97] += 1
    for char in word2.lower():
        list2[ord(char) - 97] += 1

    if list1 == list2:
        return True
    return False

def is_anagram_sort_hash(word1:str, word2:str)->bool:
    '''Sort both words, then compare to see if they are exactly the same.
    '''
    checks = basic_checks(word1, word2)
    if not checks[0]:
        return False
    word1 = checks[1]
    word2 = checks[2]
    
    srt = list(word1)
    srt.sort()
    srt2 = list(word2)
    srt2.sort()
    if srt == srt2:
        return True
    return False

ch_to_prime = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13,
    'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43,
    'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79,
    'w': 83, 'x': 89, 'y': 97, 'z': 101 }

def is_anagram_prime_hash(word1:str, word2:str)->bool:
    '''Create a dictionary of prime numbers (see chToprime above). Use the ascii value of each letter in both
      words to construct a unique numeric representation of the word (called a 'hash').
      Words with the same hash value are anagrams of each other.
    '''
    checks = basic_checks(word1, word2)
    if not checks[0]:
        return False
    word1 = checks[1]
    word2 = checks[2]
    
    count = 1
    for char in word1:
        count *= ch_to_prime[char]

    count2 = 1
    for char in word2:
        count2 *= ch_to_prime[char]

    if count == count2:
        return True
    return False

if __name__ == "__main__":
    algorithms = [is_anagram_exhaustive, is_anagram_checkoff, is_anagram_lettercount, is_anagram_sort_hash, is_anagram_prime_hash]
    word1 = "beast"
    word2 = "baste"
    print(word1, word2, basic_checks("baste2", "beast"))
    print(is_anagram_exhaustive("beast", "baste"))
    print(is_anagram_checkoff("beast", "baste"))


    for algorithm in algorithms:
        print(f"{algorithm.__name__}- {word1}, {word2}: {algorithm(word1, word2)}")