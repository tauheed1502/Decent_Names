import random, os
import utilities as utl

adjectives = utl.file_to_array('./data/adjectives_clean.txt')
nouns = utl.file_to_array('./data/nouns_clean.txt')
names = utl.file_to_array('./data/names_clean.txt')
good_words = adjectives + nouns + names
bad_words = utl.file_to_array('./data/bad_words_cmu.txt')
bad_words_obfs = utl.file_to_array('./data/bad_words_google.txt')

obfuscation_dictionary = {'A':'4','a':'4','E':'3','e':'3','I':'1','i':'1','O':'0','o':'0','L':'1','l':'1','S':'5','s':'5'}

def obfuscate(username):
    return_username = username
    for i, char in enumerate(username, 0):
        if char in obfuscation_dictionary and random.randint(0, 1) == 1:
            return_username = return_username[:i] + obfuscation_dictionary[char] + return_username[i+1:]
    return return_username

def run_username_generator(outputFile, label, num_to_generate, obfuscation, list_1, list_2):
    with open(outputFile, 'a') as oFile:
        for i in range(int(num_to_generate)):
            ran_1 = random.choice(list_1)
            ran_2 = random.choice(list_2)

            username = ran_1 + ran_2

            if random.randint(0, 1) == 1:
                username = ran_2 + ran_1

            if (obfuscation):
                username = obfuscate(username)

            oFile.write(utl.print_name_data(str(label), username))

def generate_usernames(outputFile, count, percent_offensive, percent_obfuscated):

    if os.path.exists(outputFile):
        os.remove(outputFile)

    run_username_generator(outputFile, 0, count * (1 - percent_offensive) * (1 - percent_obfuscated), False, good_words, good_words)
    run_username_generator(outputFile, 0, count * (1 - percent_offensive) * percent_obfuscated, True, good_words, good_words)
    run_username_generator(outputFile, 1, count * percent_offensive * (1 - percent_obfuscated), False, good_words, bad_words)
    run_username_generator(outputFile, 1, count * percent_offensive * percent_obfuscated, True, good_words, bad_words)

