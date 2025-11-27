# About Day 05 assignment

I have written a code that implements the game "**WORD LADDER**"

# WORD LADDER

Word Ladder is a word game where you transform one word into another by changing a single letter at each step, with each new combination forming a valid word. 
Example: change "cat" to "big"- "cat" → "bat" → "bit" → "big"

# About the code

This is a simple, easy-to-use Python code that runs on CLI.
The game can be played on two levels: Level-1 and Level-2.

# 1. Level-1 (word_ladder_L1):
* The code loads a word list from a separate file called wordlist_3Letter.txt
* This word list acts as a dictionary that conatins all the **1,351 valid three-letter words** in the English language that have been approved by Collins Dictionary and also used in Scrabble [https://scrabble.collinsdictionary.com/word-lists/three-letter-words-in-scrabble/].
* The program imports the package random and chooses a 3-letter word randomly from the wordlist_3Letter.txt
* The user then has to build a word ladder of **3-letter words** by changing only one letter at a time till five different valid words are built.
* The program terminates when a ladder of **5 different words** has been built.
* The user gets a maximum of **2 incorrect attempts**.
* The program also terminates when the user either enters an invalid word (not defined by Collins Dictionary) or changes more than one letter at a time or enters more than 3 letters.
* The program also keeps a track of your score. Once the maximum 5 word ladder is reached, the program displays your score.

# 2. Level-2 (word_ladder_L2):
* The code loads a word list from a separate file called wordlist_4Letter.txt
* This word list acts as a dictionary that conatins all the **5,663 valid four-letter words** in the English language that have been approved by Collins Dictionary and also used in Scrabble [https://scrabble.collinsdictionary.com/word-lists/four-letter-words-in-scrabble/].
* The program imports the package random and chooses a 4-letter word at random from the wordlist_4Letter.txt
* The user then has to build a word ladder of **4-letter words** by changing only one letter at a time until eight different valid words are built.
* The program terminates when a ladder of **8 different words** has been built.
* The user gets a maximum of **3 incorrect attempts**.
* The program also terminates when the user either enters an invalid word (not defined by Collins Dictionary) or changes more than one letter at a time or enters more than 4 letters.
* The program also keeps a track of your score. Once the maximum 8 word ladder is reached, the program displays your score.

## LIMITATIONS

* The program is written only for 3-letter and 4-letter English words and maximum ladder of 5 words and 8 words respectively can be built.
* Since this is a basic program for test run, it can be extended to a longer length of the word ladder (eg. 10 word ladder).
* For 5-letter/6-letter words etc., a new wordlist file (.txt) verified by global English standards can be added.

## Dependencies

* A word list saved as .txt file (Unicode UTF-8). Only one word saved in a line, preferably in lowercase, no special characters or numbers. File should be in the same folder. 
* Python version = 3.8.2
* Package = random
