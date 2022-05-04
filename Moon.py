# todo : add licence to the repo & readme.md


import pyttsx3
import sqlite3
from os import path
from string import ascii_letters

# import PyQt5 packages
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType  # load Qt files
from googletrans import Translator  # to translate online

# Create A DataBase
db = sqlite3.connect('google_words.db')  # Connect To Database
cursor = db.cursor()  # Cursor
cursor.execute('''
CREATE TABLE IF NOT EXISTS words(
ID INTEGER PRIMARY KEY NOT NULL,
ar,
en);
''')  # Make a new table if not exists with two rows for arabic, english words

BASE_DIR = path.dirname(path.realpath(__file__))
FORMS_DIR = path.join(BASE_DIR, 'forms')

FORM_CLASS, _ = loadUiType(path.join(FORMS_DIR, 'moon.ui'))
ADD_CLASS, _ = loadUiType(path.join(FORMS_DIR, 'add.ui'))
EDIT_CLASS, _ = loadUiType(path.join(FORMS_DIR, 'edit.ui'))
DELETE_CLASS, _ = loadUiType(path.join(FORMS_DIR, 'delete.ui'))
SETTINGS_CLASS, _ = loadUiType(path.join(FORMS_DIR, 'settings.ui'))
CONTENT_CLASS, _ = loadUiType(path.join(FORMS_DIR, 'help.ui'))
ABOUT_CLASS, _ = loadUiType(path.join(FORMS_DIR, 'about.ui'))

translator = Translator()  # inheritance translator class in google translate module
engine = pyttsx3.init()  # inheritance pyttsx3.init() class in pyttsx3  module
online = False  # set variable to see if user want to translate online or not [see setting_dialog() class ]
speak = False  # set variable to see if user want to speaks words or not [see setting_dialog() class ]


class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        QMainWindow.__init__(self)
        self.deleting = DeletD()
        self.editing = EditD()
        self.adding = AddD()
        self.setupUi(self)

        self.move(400, 180)  # move window position
        self.tree()  # program organization

    def tree(self):

        self.show()  # that's will show the main class
        self.search_b.clicked.connect(self.search)  # search button
        self.exit_b.clicked.connect(self.quit)  # exit   button
        self.add_b.clicked.connect(self.add_form)  # add    button
        self.edit_b.clicked.connect(self.edit_form)  # edit   button
        self.delete_b.clicked.connect(self.delete_form)  # delete   button
        self.settings_t.triggered.connect(self.settings)  # settings in menu bar
        self.content_t.triggered.connect(self.content)
        self.about_t.triggered.connect(self.about_me)

    def search(self):

        if online:
            try:
                word = self.search_bar.text().lower()

                if word and word[0] in ascii_letters:  # Detect english or arabic   # todo: make a switch function
                    self.textBrowser.clear()  # clear textbrowser to avoid conflict with old translate words
                    self.label.setText('')  # clear status bar to not show not found word with online option
                    i = translator.translate(word, dest='ar').text  # translate the word to arabic
                    self.textBrowser.append(i)  # print word in textBrowser

                    if speak:
                        engine.say(word)  # To speak the word
                        engine.runAndWait()

                else:
                    self.textBrowser.clear()
                    self.label.setText('')
                    i = translator.translate(word, dest='en')  # translate the word to english
                    self.textBrowser.append(i.text)
                    if speak:
                        engine.say(i.text)
                        engine.runAndWait()

            except Exception as online_error:
                print(f"online_error {online_error}")
                self.label.setText("الرجاء التحقق من وصول شبكه الانترنت")

        else:

            data = cursor.execute('SELECT * FROM words')
            word = self.search_bar.text().lower()

            if word and word[0] in ascii_letters:  # Detect english or arabic
                self.textBrowser.clear()

                for i in data:
                    if word in i:
                        self.label.setText('')  # to set label empty if found the word
                        if speak:
                            engine.say(word)  # To speak the word
                            engine.runAndWait()

                        return self.textBrowser.append(i[1])  # 1 is english column words
                else:
                    self.label.setText(" لم يتم العثور علي الكلمة")
            else:
                self.textBrowser.clear()

                for i in data:
                    if word in i:
                        self.label.setText('')
                        if speak:
                            engine.say(word)
                            engine.runAndWait()
                        return self.textBrowser.append(i[2])

                else:
                    self.label.setText(" لم يتم العثور علي الكلمة")

    def add_form(self):
        self.adding.exec()  # without .show() that's better

    def edit_form(self):
        self.editing.exec_()

    def delete_form(self):
        self.deleting.exec_()

    @staticmethod
    def settings():
        SettingsD().exec_()

    @staticmethod
    def content():
        ContentD().exec_()

    @staticmethod
    def about_me():
        AboutD().exec_()

    @staticmethod
    def quit():
        m = QMessageBox.question(win, 'Message', 'Do you want Exit', QMessageBox.Yes | QMessageBox.No)
        if m == QMessageBox.Yes:
            exit(0)


class AddD(QDialog, ADD_CLASS):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.add_b.clicked.connect(self.add)
        self.back_b.clicked.connect(self.back)

    def add(self):
        if self.ar_text.text() == '' or self.en_text.text() == '':
            QMessageBox.critical(self, 'خطأ', 'برجاء عدم ادخال خانات فارغة ', QMessageBox.Ok)

        else:
            ar = self.ar_text.text()
            en = self.en_text.text()
            cursor.execute('INSERT INTO words(en, ar) VALUES(?, ?)', (en, ar))
            db.commit()
            QMessageBox.question(self, 'Message', 'تمت الاضافه بنجاح {} {} {} {}'.format('\n', ar, '\n', en),
                                 QMessageBox.Ok)

    def back(self):
        self.hide()


class EditD(QDialog, EDIT_CLASS):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.search_b.clicked.connect(self.edit_search)
        self.edit_b.clicked.connect(self.save_edit)
        self.back_b.clicked.connect(self.hide)

    def edit_search(self):
        data = cursor.execute('SELECT * FROM words')
        word = self.edit_search_bar.text().lower()

        if word[0] in ascii_letters:
            for i in data:
                if word in i:
                    self.result_bar.setPlainText(i[1])
                    break  # break loop so else statement not gonna work with same result
            else:
                return QMessageBox.critical(self, 'Message', 'لم يتم العثور علي الكلمه', QMessageBox.Ok)

        else:
            for i in data:
                if word in i:
                    self.result_bar.setPlainText(i[2])
                    break
            else:
                return QMessageBox.critical(self, 'Message', 'لم يتم العثور علي الكلمه', QMessageBox.Ok)

    def save_edit(self):

        word = self.edit_search_bar.text()
        new_word = self.result_bar.toPlainText()  # toPlainText() to read text from plain text object
        # todo set a switch to update ar to en and vice versa
        cursor.execute("UPDATE words  SET ar = ? WHERE en = ? ", (new_word, word))
        db.commit()
        QMessageBox.about(self, 'Message', 'تم حفظ التعديلات بنجاح !')


class DeletD(QDialog, DELETE_CLASS):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.search_b.clicked.connect(self.delete_search)
        self.delete_b.clicked.connect(self.save_delete)
        self.back_b.clicked.connect(self.hide)

    def delete_search(self):
        word = self.search_bar.text().lower()
        if word[0] in ascii_letters:
            # todo: add switch to select between ar and en
            # returns a tuple of one element
            data = cursor.execute('SELECT ar FROM words where en = ? ', (word,)).fetchone()[0]
            if data:
                self.result_bar.setPlainText(data)
            else:
                return QMessageBox.critical(self, 'Message', 'لم يتم العثور علي الكلمه', QMessageBox.Ok)

    def save_delete(self):
        old_word1 = self.search_bar.text()

        confirm = QMessageBox.critical(self, 'Message', 'هــل تريد حذف هذه الكلمه ؟', QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:  # confirm message to delete the word
            if old_word1[0] in ascii_letters:
                cursor.execute("DELETE FROM words  WHERE en = ? ", (old_word1,))
                db.commit()
                self.search_bar.clear()
                self.result_bar.setPlainText('')
                QMessageBox.about(self, 'Message', 'تم الحذف بنجاح !')


class SettingsD(QDialog, SETTINGS_CLASS):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.ok_b.clicked.connect(self.save_settings)
        self.back_b.clicked.connect(self.back)

        if online:
            self.trans_b.setChecked(True)  # To set checkbox correct mark [to keep mark after closing widget ]
        if speak:
            self.speak_b.setChecked(True)

    def save_settings(self):
        # todo: save user settings in database
        if self.trans_b.isChecked():
            global online  # i used global online variable to change variable out side the class
            online = True
        else:
            online = False

        if self.speak_b.isChecked():
            global speak
            speak = True
        else:
            speak = False

        self.hide()

    def back(self):
        self.hide()


class ContentD(QDialog, CONTENT_CLASS):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.back_b.clicked.connect(self.hide)


class AboutD(QDialog, ABOUT_CLASS):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.back_b.clicked.connect(self.hide)


app = QApplication([])
win = Main()

app.exec_()

# todo : add notes in readme.md
'''
Notes :

you need to convert your resources file to py by :
pyrcc5 -o  qt_rc.py  resources.qrc
pyrcc5 -o  <file to create.py> <your resource file.qrc>



'''
