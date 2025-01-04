def file_to_array(string):
    with open(string, 'r') as openFile:
        return openFile.read().splitlines()

def print_name_data(label, name):
    return label + "\t" + name + "\n"

"""
Code executed once for cleaning data. Archived for discussion lter
"""
# def clean_words():
#     for bad_word in bad_words:
#         if bad_word in nouns:
#             nouns.remove(bad_word)
#         if bad_word in adjectives:
#             adjectives.remove(bad_word)
#         if bad_word in names:
#             names.remove(bad_word)
    
#     with open("./data/names_clean.txt", 'w') as names_file:
#         for name in names:
#             names_file.write(name + "\n")

#     with open("./data/nouns_clean.txt", 'w') as nouns_file:
#         for noun in nouns:
#             nouns_file.write(noun + "\n")

#     with open("./data/adjectives_clean.txt", 'w') as adjectives_file:
#         for adjective in adjectives:
#             adjectives_file.write(adjective + "\n")