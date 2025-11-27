# About Day 05 assignment

I have written a code that implements the game "**WORD LADDER**".

# WORD LADDER

Word Ladder is a word game where you transform one word into another by changing a single letter at each step, with each new combination forming a valid word. 
Example: change "cat" to "big"- "cat" → "bat" → "bit" → "big"

# About the code

This is a simple, easy-to-use Python code that runs on CLI.
* The code loads a word list from a separate file called wordlist.txt
* This word list acts as a dictionary that conatins all 1,351 valid three-letter words in the English language that have been approved by Collins Dictionary and also used in Scrabble [https://scrabble.collinsdictionary.com/word-lists/three-letter-words-in-scrabble/].
* The program imports the package random and chooses a 3-letter word randomly from the wordlist.txt
* The user then has to build a word ladder of 3-letter words by changing only one letter at a time till five different valid words are built.
* The program terminates when a ladder of 5 different words has been built.
* The user gets a maximum of two incorrect attempts.
* The program also terminates when the user either enters an invalid word (not defined by Collins Dictionary) or changes more than one letter at a time or enters more than 3 letters.
* The program also keeps a track of your score. Once the maximum 5 word ladder is reached, the program displays your score.

## LIMITATIONS

* The program is written only for 3-letter English words and maximum ladder of 5 words can built.
* Since this is a basic program for test run, it can be changed to a longer length of word ladder (eg. 10 word ladder).
* For 4-letter/5-letter/6-letter words etc., a new wordlist verified by global English standards can be added
