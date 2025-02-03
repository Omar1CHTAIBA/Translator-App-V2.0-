from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QFont, QIcon
from gtts import gTTS
from googletrans import Translator
import pyttsx3, os
from data import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings()
        self.button_clicked()
        self.engine = pyttsx3.init()

    def initUI(self):
        self.input_box = QTextEdit()
        self.output_box = QTextEdit()
        self.reverse = QPushButton('Reverse')
        self.reverse.setToolTip("Reverse")
        self.reset = QPushButton('Reset')
        self.reset.setObjectName("reset")
        self.submit = QPushButton("Translate Now")
        self.read_text = QPushButton("Read Text")  # New Read Text button
        self.input_option = QComboBox()
        self.output_option = QComboBox()

        self.input_option.addItems(values)
        self.output_option.addItems(values)

        self.title = QLabel("Translator")
        self.title.setFont(QFont("bold", 50))

        self.master = QVBoxLayout()
        self.master.setContentsMargins(10, 40, 10, 40)

        row1 = QHBoxLayout()
        row1.addStretch(1)
        row1.addWidget(self.title)
        row1.addStretch(1)

        row2 = QHBoxLayout()
        row2.addWidget(self.input_option)
        row2.addWidget(self.input_box)
        row2.addWidget(self.reverse)
        row2.addWidget(self.output_box)
        row2.addWidget(self.output_option)

        row3 = QHBoxLayout()
        row3.addStretch(1)
        row3.addWidget(self.submit)
        row3.addSpacing(20)  # Adjust the spacing as needed
        row3.addWidget(self.read_text)
        row3.addSpacing(20)  # Adjust the spacing as needed
        row3.addWidget(self.reset)
        row3.addStretch(1)

        self.master.addLayout(row1)
        self.master.addSpacing(30)
        self.master.addLayout(row2)
        self.master.addSpacing(30)
        self.master.addLayout(row3)

        self.setLayout(self.master)

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
                color: #2f3640;
            }

            QLabel {
                color: #2f3640;
                font-weight: bold;
            }

            QTextEdit {
                background-color: white;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                min-height: 200px;
                selection-background-color: #54a0ff;
            }

            QTextEdit:focus {
                border: 2px solid #54a0ff;
            }

            QPushButton {
                background-color: #54a0ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }

            QPushButton:hover {
                background-color: #2e86de;
            }

            QPushButton:pressed {
                background-color: #0984e3;
            }

            QPushButton#reset {
                background-color: #ff6b6b;
            }

            QPushButton#reset:hover {
                background-color: #ee5253;
            }

            QComboBox {
                background-color: white;
                border: 2px solid #dcdde1;
                border-radius: 6px;
                padding: 5px 10px;
                min-width: 150px;
                font-size: 14px;
            }

            QComboBox:drop-down {
                border: none;
                width: 30px;
            }

            QComboBox:down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }

            QComboBox:hover {
                border: 2px solid #54a0ff;
            }

            QMessageBox {
                background-color: white;
            }

            QMessageBox QPushButton {
                min-width: 80px;
                padding: 5px 15px;
            }
        """)

    def settings(self):
        self.setWindowTitle('Translator')
        self.setWindowIcon(QIcon(r'translate.png'))
        self.setGeometry(160, 100, 1400, 800)

    def button_clicked(self):
        self.submit.clicked.connect(self.translate_click)
        self.reset.clicked.connect(self.reset_app)
        self.reverse.clicked.connect(self.reverse_languages)
        self.read_text.clicked.connect(self.text_to_speach_activate)  # Connect the Read Text button

    def translate_click(self):
        value_to_key1 = self.output_option.currentText()
        value_to_key2 = self.input_option.currentText()

        key_to_value1 = [k for k, v in LANGUAGES.items() if v == value_to_key1]
        key_to_value2 = [k for k, v in LANGUAGES.items() if v == value_to_key2]

        self.script = self.translate_text(self.input_box.toPlainText(), key_to_value1[0], key_to_value2[0])
        self.output_box.setText(self.script)

    def reset_app(self):
        self.input_box.clear()
        self.output_box.clear()

    def translate_text(self, text, dest_lang, src_lang):
        if not text.strip():
            info_box = QMessageBox()
            info_box.setIcon(QMessageBox.Icon.Information)
            info_box.setWindowTitle("Translation Info")
            info_box.setText("Please enter some text to translate")
            info_box.exec()
            return ''
        try:
            speaker = Translator()
            translation = speaker.translate(text, dest=dest_lang, src=src_lang)
            return translation.text
        except Exception as e:
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Icon.Warning)
            error_box.setWindowTitle("Translation Error")
            error_box.setText("An error occurred during translation")
            error_box.setDetailedText(str(e))
            error_box.exec()
            return 'Translation failed'

    def text_to_speach_activate(self):
        value_to_key1 = self.output_option.currentText()
        key_to_value1 = [k for k, v in LANGUAGES.items() if v == value_to_key1]

        self.text_to_speach(self.output_box.toPlainText(), dest_lang=key_to_value1[0])

    def text_to_speach(self, text, dest_lang):
        if not text.strip():
            info_box = QMessageBox()
            info_box.setIcon(QMessageBox.Icon.Information)
            info_box.setWindowTitle("Read text")
            info_box.setText("Please translate ifrst !")
            info_box.exec()
            return ''
        try:
            tts = gTTS(text, lang=dest_lang)
            tts.save("translated_audio.mp3")
            os.system("start translated_audio.mp3")
        except Exception as e:
            info_box = QMessageBox()
            info_box.setIcon(QMessageBox.Icon.Information)
            info_box.setWindowTitle("Error")
            info_box.setText(f"{e}")
            info_box.exec()
            return ''

    def read_translated_text(self):
        text = self.output_box.toPlainText()
        if text:
            self.engine.say(text)
            self.engine.runAndWait()

    def reverse_languages(self):
        s1, l1 = self.input_box.toPlainText(), self.input_option.currentText()
        s2, l2 = self.output_box.toPlainText(), self.output_option.currentText()

        self.input_box.setText(s2)
        self.output_box.setText(s1)
        self.input_option.setCurrentText(l2)
        self.output_option.setCurrentText(l1)

        # Force update the layout and widgets
        self.input_box.update()
        self.output_box.update()
        self.input_option.update()
        self.output_option.update()
        self.master.update()
        self.update()


if __name__ == '__main__':
    app = QApplication([])
    main = Window()
    main.show()
    app.exec()
