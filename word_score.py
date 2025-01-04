#!/usr/bin/env python3

import sys
import doctest
import utilities as util
pylevenshtein = __import__('Levenshtein')

"""TODO add title"""

""" CONSTANTS """

BAD_WORD_LIST_FILEPATH = 'data/bad_words_cmu.txt' #TODO switch to the master and combine the bad word files
LEETSPEAK_TO_ENGLISH_DICT = {'0':'o',
                             '1':'l', #TODO handle 1 -> i translation
                             '3':'e', 
                             '4':'a', 
                             '5':'s', #TODO handle alternate 5 -> h translation
                             '7':'t', #TODO handle x -> k translation
                             '8':'b', 
                             '!':'i',
                             '@':'a',
                             '$':'s',
                             '+':'t'}

""" FUNCTIONS """

def score_username(usr: str, debug=False) -> float:
    """Returns a score for a username between 0 and 1, 0 being surely inoffensive and 1 being surely offensive."""

    # check for empty paramter
    if not usr:
        raise ValueError('Missing username arguement')

    # loads bad word list
    bad_words = util.file_to_array(BAD_WORD_LIST_FILEPATH)

    # preprocess username
    processed_usr = preprocess_username(usr)

    # check if the whole username is match for any in the bad list, return a strong bad score if so
    whole_usr_score = score_word(processed_usr, bad_words, debug=debug)

    # if max score is above a threshold, return 

    # parse name for recognizable word, preferring the longest possible ones

    # check if any words are in the bad list, return a strong bad score if so

    # check every combination of words with leftover adjacent text against bad list using soundex and jaro-winkler distance

    # check versions with numbers replaced with similar letters (leetspeak check)

    # return the largest score of the word combinations
    return whole_usr_score

def preprocess_username(usr: str, debug=False) -> str:
    """Prepares a word for scanning by removing characters outside of alphanumeric characters and forcing all lowerspace."""
    
    #TODO remove all non-alphanumeric characters
    
    # convert to all lowercase characters
    usr = usr.lower()

    return usr

def generate_username_scores(username: str, debug=False) -> list:
    """Return the greatest Jaro score, greatest Levenshtein score and Levenshtein score between 2 most suspect words."""
    
    # loads bad word list
    bad_words = util.file_to_array(BAD_WORD_LIST_FILEPATH)

    # create a list of possible leetspeak translations of the word, along with the original word
    leetspeak_segs = leetspeak_to_english(username, debug)

    greatest_jaro_score = 0
    greatest_lev_score = 0
    most_similar_bad_word_jaro = ''
    most_similar_bad_word_lev = ''
    most_suspect_word_jaro = ''
    most_suspect_word_lev = ''

    for suspect_seg in [username] + leetspeak_segs:

        # loop through all the bad words in the list
        for bad_word in bad_words:

            # compare all suspect words against current bad word with jaro and levenshtein, store greatest score
            jaro_score = pylevenshtein.jaro(suspect_seg, bad_word)
            lev_score = pylevenshtein.ratio(suspect_seg, bad_word)

            if debug:
                print('SCORING: Suspect word', suspect_seg, 'when compared to', bad_word, 'has a score of', jaro_score, 'by Jaro and', lev_score, 'by Levenshtein')

            if jaro_score > greatest_jaro_score:
                greatest_jaro_score = jaro_score
                most_similar_bad_word_jaro = bad_word
                most_suspect_word_jaro = suspect_seg

            if lev_score > greatest_lev_score:
                greatest_lev_score = lev_score
                most_similar_bad_word_lev = bad_word
                most_suspect_word_lev = suspect_seg

    if debug:
        print('SCORING_RESULT: Greatest Jaro score is', greatest_jaro_score, 'between', most_suspect_word_jaro, 'and', most_similar_bad_word_jaro)
        print('SCORING_RESULT: Greatest Levenshtein score is', greatest_lev_score, 'between', most_suspect_word_lev, 'and', most_similar_bad_word_lev)

    # calculate the Levenshtein score between the most similar bad words by Jaro and Levenshtein methods
    comparison_lev_score = pylevenshtein.ratio(most_similar_bad_word_jaro, most_similar_bad_word_lev)

    if debug:
        print('SCORING_RESULT: Comparision score is', comparison_lev_score, 'between', most_similar_bad_word_jaro, 'and', most_similar_bad_word_lev)

    return [greatest_jaro_score, greatest_lev_score, comparison_lev_score]

def score_word(seg: str, bad_words: list, method='both', debug=False) -> float:
    """Returns a score for a word between 0 and 1, 0 being surely inoffensive and 1 being surely offensive.
    The method parameter can be both, jaro or levenshtein. Both returns whichever is higher, and the other
    two options force the score that is returned to be from that method.
    """
    
    # create a list of possible leetspeak translations of the word, along with the original word
    leetspeak_segs = leetspeak_to_english(seg, debug)

    greatest_jaro_score = 0
    greatest_lev_score = 0
    most_similar_bad_word_jaro = ''
    most_similar_bad_word_lev = ''
    most_suspect_word_jaro = ''
    most_suspect_word_lev = ''

    for suspect_seg in [seg] + leetspeak_segs:

        # loop through all the bad words in the list
        for bad_word in bad_words:

            # compare all suspect words against current bad word with jaro and levenshtein, store greatest score
            jaro_score = pylevenshtein.jaro(suspect_seg, bad_word)
            lev_score = pylevenshtein.ratio(suspect_seg, bad_word)

            if debug:
                print('SCORING: Suspect word', suspect_seg, 'when compared to', bad_word, 'has a score of', jaro_score, 'by Jaro and', lev_score, 'by Levenshtein')

            if jaro_score > greatest_jaro_score:
                greatest_jaro_score = jaro_score
                most_similar_bad_word_jaro = bad_word
                most_suspect_word_jaro = suspect_seg

            if lev_score > greatest_lev_score:
                greatest_lev_score = lev_score
                most_similar_bad_word_lev = bad_word
                most_suspect_word_lev = suspect_seg

    if debug:
        print('SCORING_RESULT: Greatest Jaro score is', greatest_jaro_score, 'between', most_suspect_word_jaro, 'and', most_similar_bad_word_jaro)
        print('SCORING_RESULT: Greatest Levenshtein score is', greatest_lev_score, 'between', most_suspect_word_lev, 'and', most_similar_bad_word_lev)

    # return the greatest score of all comparisions
    if method == 'both':
        return max(greatest_jaro_score, greatest_lev_score)
    elif method == 'jaro':
        return greatest_jaro_score
    elif method == 'levenshtein':
        return greatest_lev_score

def leetspeak_to_english(seg: str, debug=False) -> list:
    """Returns a list of strings with all non-alphabetic character replaced by similar looking alphabetic characters.
    
    NOTE: This returns a list of strings to consider multiple possible translations of characters, but that functionality is not currently implemented.

    >>> leetspeak_to_english('41ph483+')
    ['alphabet']

    >>> leetspeak_to_english('8ad@$$g00n')
    ['badassgoon']

    >>> leetspeak_to_english('normaltestwoowoo')
    ['normaltestwoowoo']

    >>> leetspeak_to_english('8!+ch')
    ['bitch']
    """

    translations = ['']

    for char in seg:
        
        if char in LEETSPEAK_TO_ENGLISH_DICT:
            translations[0] += LEETSPEAK_TO_ENGLISH_DICT[char]
        
        else:
            translations[0] += char
    
    if debug: 
        print('LEETSPEAK: Leetspeak translations of', seg + ':', translations[0])
    
    return translations


""" MAIN GUARD """

if __name__ == '__main__':

    debug_flag = False

    # get a username if not provided by arguement
    if len(sys.argv) < 2:
        cur_username = input('Please enter a username to score: ')

    # check if the user is running a doctest
    elif sys.argv[1] == 'doctest':
        doctest.testmod()
        exit()

    # get the username from the arguements passed
    else:
        if '-d' in sys.argv or '--debug' in sys.argv:
            debug_flag = True
        cur_username = sys.argv[1]

    # score the provided username
    cur_score = score_username(cur_username, debug_flag)
    print('Score calculated for the username above:', str(cur_score))