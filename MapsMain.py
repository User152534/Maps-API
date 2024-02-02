# API: задача №2
# Запросить карту через Static API
# и отрисовать её в графическом окне.


import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox

SCREEN_SIZE = (600, 450)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.tmp_file = None  # Временный файл, в который будем помещать изображение
        self.getImage()
        self.initUI()

    def getImage(self):
        """Функция запроса файла с сервера и сохранения его на диске37.530887,55.703118"""
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={input()}&spn=10,0.002&l=map"
        response = requests.get(map_request)

        if not response:
            print('Ошибка выполнения запроса:')
            print(map_request)
            print(f'HTTP-статус: {response.status_code} - {response.reason}')
            sys.exit(1)

        # Записываем полученное изображение во временный файл:
        self.tmp_file = 'tmp_image.png'
        with open(self.tmp_file, 'wb') as f:
            f.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        # Помещаем изображение в графическое окно
        # на виджет QLable размером с окно:
        self.pixmap = QPixmap(self.tmp_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SCREEN_SIZE)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """Переопределяем стандартный метод закрытия окна"""
        close = QMessageBox()
        close.setText('Закрыть окно?')
        # Кнопки "Да" и "Отмена":
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()  # Перехватываем номер кнопки при подтверждении закрытия
        if close == QMessageBox.Yes:
            os.remove(self.tmp_file)  # При закрытии окна удаляем и временный файл
            event.accept()  # Принимаем событие
        else:
            event.ignore()  # Игнорируем событие


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())