__author__      = "Ahmed Fathy "
__copyright__   = "Copyright 2018 "
__version__ = "1.0"
__email__ = "https://www.facebook.com/profile.php?id=100016846006190"

'''
                  You can  add, edit in program 
                  do what you want but keep the source or mention it ..
                  thank you. 
'''


import sqlite3, sys, os, string, pyttsx3



# import PyQt5 packages
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.uic import loadUiType    # load Qt files

from googletrans import Translator # to translate online

# Create A DataBase
db = sqlite3.connect('google_words.db')        # Connect To Database
cursor = db.cursor()                           # Cursor
cursor.execute('''
CREATE TABLE IF NOT EXISTS words(
ID INTEGER PRIMARY KEY NOT NULL,
ar,
en);
''')                     # Make a new table if not exists with two rows for arabic, english words




#___________________Open PyQt Designs __________________

FORM_CLASS, _ = loadUiType(os.path.join(
    os.path.dirname(__file__), 'moon.ui'))

ADD_CLASS, _ = loadUiType(os.path.join(
    os.path.dirname(__file__), 'add.ui'))

EDIT_CLASS, _ = loadUiType(os.path.join(
    os.path.dirname(__file__), 'edit.ui'))

DELETE_CLASS, _ = loadUiType(os.path.join(
    os.path.dirname(__file__), 'delete.ui'))

SETTINGS_CLASS, _ = loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings.ui'))

CONTENT_CLASS, _ = loadUiType(os.path.join(
    os.path.dirname(__file__), 'help.ui'))

ABOUT_CLASS, _ = loadUiType(os.path.join(
    os.path.dirname(__file__), 'about.ui'))


translator = Translator()   # inheritance translator class in google translate module
engine = pyttsx3.init()     # inheritance pyttsx3.init() class in pyttsx3  module
online = False              # set variable to see if user want to translate online or not [see setting_dialog() class ]
speak = False               # set variable to see if user want to speaks words or not [see setting_dialog() class ]

class main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(QMainWindow,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.move(400, 180)   # move window position
        self.tree()           # program organization



    def tree(self):

        self.show()                                      # that's will show the main class
        self.search_b.clicked.connect(self.search)       # search button
        self.exit_b.clicked.connect(self.quit)           # exit   button
        self.add_b.clicked.connect(self.add_form)        # add    button
        self.edit_b.clicked.connect(self.edit_form)      # edit   button
        self.delete_b.clicked.connect(self.delete_form)  # delete   button
        self.settings_t.triggered.connect(self.settings) # settings in menu bar
        self.content_t.triggered.connect(self.content)
        self.about_t.triggered.connect(self.about_me)


    def search(self):

        if online == True :
            print(" online is enabled ")
            try :
                word = self.search_bar.text().lower()

                if word[0] in  string.ascii_letters :              # Detect english or arabic
                    self.textBrowser.clear()                       # clear textbrowser to avoid conflict with old translate words
                    self.label.setText('')                         # clear status bar to not show not found word with online option
                    i = translator.translate(word, dest='ar')      # translate the word to arabic
                    self.textBrowser.append(i.text)                # print word in textBrowser
                    if speak == True :
                        print(" Speak is enabled ")
                        engine.say(word)                             # To speak the word
                        engine.runAndWait()
                    else :
                        print(" Speak is disabled ")

                else :
                    self.textBrowser.clear()
                    self.label.setText('')
                    i = translator.translate(word, dest='en')      # translate the word to english
                    self.textBrowser.append(i.text)
                    if speak == True :
                        print(" Speak is enabled ")
                        engine.say(i.text)
                        engine.runAndWait()
                    else :
                        print(" Speak is disabled ")
            except :
                self.label.setText("الرجاء التحقق من وصول شبكه الانترنت")

        else :
            print(" online is disabled ")

            data = cursor.execute('SELECT * FROM words')
            word = self.search_bar.text().lower()

            if word[0] in  string.ascii_letters : # Detect english or arabic
                    print(" English")
                    self.textBrowser.clear()

                    for i in data :
                        if word in i :
                            self.label.setText('') # to set label empty if found the word
                            print(i[1])
                            if speak == True :
                                print(" Speak is enabled ")
                                engine.say(word)                             # To speak the word
                                engine.runAndWait()
                            else :
                                print(" Speak is disabled ")
                            return self.textBrowser.append(i[1]) # 1 is english column words
                    else:
                        self.label.setText(" لم يتم العثور علي الكلمة")
                        print(" Not found")
            else:
                print(' Arabic')
                self.textBrowser.clear()

                for i in data :
                    if word in i :
                        self.label.setText('')
                        print(i[2])
                        if speak == True :
                            print(" Speak is enabled ")
                            engine.say(word)
                            engine.runAndWait()
                        else :
                            print(" Speak is disabled ")
                        return self.textBrowser.append(i[2])

                else :
                    self.label.setText(" لم يتم العثور علي الكلمة")
                    return print(" Not found")



    def add_form(self):
        self.adding = add_dialog()
        self.adding.exec()    # without .show() that's better

    def edit_form(self):
        self.editing = edit_dialog()
        self.editing.exec_()

    def delete_form(self):
         self.deleting = delete_dialog()
         self.deleting.exec_()


    def settings(self):
        settigs_dialog().exec_()

    def content(self):
        content_dialog().exec_()

    def about_me(self):
        about_me_dialog().exec_()



    def quit(self):
         m = QMessageBox.question(win, 'Message', 'Do you want Exit', QMessageBox.Yes|QMessageBox.No)
         if m == QMessageBox.Yes :
             print('exit')
             exit(0)
         else :
             pass


class add_dialog(QDialog, ADD_CLASS):
    def __init__(self, parent=None):
        super(QDialog,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.add_b.clicked.connect(self.add)
        self.back_b.clicked.connect(self.back)



    def add(self):
        if self.ar_text.text() == '' or self.en_text.text() == '':
           empty = QMessageBox.critical(self,  'خطأ', 'برجاء عدم ادخال خانات فارغة ', QMessageBox.Ok)

        else :
            ar = self.ar_text.text()
            en = self.en_text.text()
            cursor.execute('INSERT INTO words(en, ar) VALUES(?, ?)', (en, ar))
            db.commit()
            m = QMessageBox.question(self, 'Message', 'تمت الاضافه بنجاح {} {} {} {}'.format('\n', ar, '\n', en) , QMessageBox.Ok)
    def back(self):

        self.hide()





class edit_dialog(QDialog, EDIT_CLASS):
    def __init__(self, parent=None):
        super(QDialog,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.search_b.clicked.connect(self.edit_search)
        self.edit_b.clicked.connect(self.save_edit)
        self.back_b.clicked.connect(self.hide)

    def edit_search(self):
        data = cursor.execute('SELECT * FROM words')
        word = self.edit_search_bar.text().lower()
        print(word)

        if word[0] in string.ascii_letters :
            print(" English word ")
            for i in data :
                if word in i :
                    print(i[1])
                    self.result_bar.setPlainText(i[1])
                    break                                   # break loop so else statement not gonna work with same result
            else :
                return QMessageBox.critical(self, 'Message', 'لم يتم العثور علي الكلمه', QMessageBox.Ok)


        else :
            print(" arabic word")
            for i in data :
                if word in i :
                    self.result_bar.setPlainText(i[2])
                    break
            else :
                return QMessageBox.critical(self, 'Message', 'لم يتم العثور علي الكلمه', QMessageBox.Ok)

    def save_edit(self):
        old_word1 = self.edit_search_bar.text()
        old_word2 = self.result_bar.toPlainText()       # toPlainText() to read text from plain text object
        print(old_word1, old_word2)
        data = cursor.execute("SELECT * FROM words")
        if old_word1[0] in string.ascii_letters :
            for i in data :
                cursor.execute("UPDATE words  SET ar = ? WHERE en = ? ", (old_word2, old_word1))
                db.commit()
                QMessageBox.about(self, 'Message', 'تم حفظ التعديلات بنجاح !')

        else :
            for i in data :
                cursor.execute("UPDATE words  SET en = ? WHERE ar = ? ", (old_word2, old_word1))
                db.commit()
                QMessageBox.about(self, 'Message', 'تم حفظ التعديلات بنجاح !')


class delete_dialog(QDialog, DELETE_CLASS):
    def __init__(self, parent=None):
        super(QDialog,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.search_b.clicked.connect(self.delete_search)
        self.delete_b.clicked.connect(self.save_delete)
        self.back_b.clicked.connect(self.hide)

    def delete_search(self):
        word = self.search_bar.text().lower()

        data = cursor.execute('SELECT * FROM words')

        if word[0] in string.ascii_letters :
            print(" English word")
            for i in data :
                if word in i :
                    self.result_bar.setPlainText(i[1])
                    break
            else :
                return QMessageBox.critical(self, 'Message', 'لم يتم العثور علي الكلمه', QMessageBox.Ok)
        else :
            print(" Arabic word")
            for i in data :
                if word in i :
                    self.result_bar.setPlainText(i[2])
                    break
            else :
                return QMessageBox.critical(self, 'Message', 'لم يتم العثور علي الكلمه', QMessageBox.Ok)


    def save_delete(self):
        old_word1 = self.search_bar.text()
        old_word2 = self.result_bar.toPlainText()       # toPlainText() to read text from plain text object

        data = cursor.execute("SELECT * FROM words")

        confirm = QMessageBox.critical(self, 'Message', 'هــل تريد حذف هذه الكلمه ؟', QMessageBox.Yes|QMessageBox.No)

        if confirm == QMessageBox.Yes :               # confirm message to delete the word
            if old_word1[0] in string.ascii_letters :

                for i in data :
                    cursor.execute("DELETE FROM words  WHERE en = ? ", (old_word1,) ) # Notice that is " delete " method in sqlite3  require a single quote after last variable
                    db.commit()
                    self.search_bar.clear()
                    self.result_bar.setPlainText('')
                    QMessageBox.about(self, 'Message', 'تم الحذف بنجاح !')

            else :

                for i in data :
                    cursor.execute("DELETE FROM words  WHERE en = ? ", (old_word2,) )
                    db.commit()
                    self.search_bar.clear()
                    self.result_bar.setPlainText('')
                    QMessageBox.about(self, 'Message', 'تم حفظ الحذف بنجاح !')
        else :
            pass


class settigs_dialog(QDialog, SETTINGS_CLASS):
    def __init__(self, parent=None):
        super(QDialog,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.ok_b.clicked.connect(self.save_settings)
        self.back_b.clicked.connect(self.back)

        if online == True :
            self.trans_b.setChecked(True)    # To set checkbox correct mark [to keep mark after closing widget ]
        if speak == True :
            self.speak_b.setChecked(True)

    def save_settings(self):
        if self.trans_b.isChecked() :
            global online       # i used global online variable to change variable out side the class
            online = True

        else :

            online = False

        if  self.speak_b.isChecked() :
            global speak
            speak = True
        else :
            speak = False

        self.hide()

    def back(self):
        self.destroy()  # To close setting window hide() also works fine i just wanna show you more methods ^_^






class content_dialog(QDialog, CONTENT_CLASS):
    def __init__(self, parent=None):
        super(QDialog,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)


        self.back_b.clicked.connect(self.hide)



class about_me_dialog(QDialog, ABOUT_CLASS):
    def __init__(self, parent=None):
        super(QDialog,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)


        self.back_b.clicked.connect(self.hide)



app = QApplication([])
win = main()

app.exec_()



'''
Notes :

you need to convert your resources file to py by :
pyrcc5 -o  qt_rc.py  resources.qrc
pyrcc5 -o  <file to create.py> <your resource file.qrc>



'''
