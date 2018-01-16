__author__      = "Ahmed Fathy"

import sqlite3
from googletrans import Translator
from time import sleep
import string
from time import sleep

db = sqlite3.connect('google_words.db')
cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS words(
ID INTEGER PRIMARY KEY NOT NULL,
ar,
en);
''')

translator = Translator()




f = open('words_alpha.txt', 'r')
data = f.readlines()
count = 0
c = 0
for n in data :
    count = count + 1




for i in data :
    word = translator.translate(i, dest='ar')
    
    db.commit()
    print(i, word.text)
    try :
        if word.text[0] in string.ascii_letters:
            print(" Repetead " + '\n' + '='*75)
            count = count - 1
        else :
            cursor.execute('INSERT INTO words(en, ar) VALUES(?, ?)', (i.split()[0], word.text.split()[0]))
            print(" New word Added  {}  contain {} words {}  chanses for new words is {} ".format('\n', str(c), '\n', str(count)))
            count = count - 1
            c = c + 1
            sleep(2)
    except Exception as e:
        print(e)
        sleep(5)
