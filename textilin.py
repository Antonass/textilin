#!/usr/bin/env python3
import sys
import os
import pyperclip
import tesserocr
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                            QVBoxLayout, QWidget, QLabel, QSystemTrayIcon, 
                            QMenu, QStyle, QTextEdit, QHBoxLayout, QComboBox)
from PyQt6.QtCore import Qt, QPoint, QRect, QTimer
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QPainter, QColor, QScreen, QShortcut
from PIL import Image

def is_wayland():
    """Определяет, запущен ли Wayland"""
    return os.environ.get('XDG_SESSION_TYPE', '').lower() == 'wayland'

def get_screenshot_command():
    """Возвращает команду для создания скриншота в зависимости от окружения"""
    if is_wayland():
        # Для Wayland используем grim
        return "grim -g \"$(slurp)\" temp_screenshot.png"
    else:
        # Для X11 используем scrot
        return "scrot -s temp_screenshot.png"

def get_icon_path():
    """Возвращает путь к иконке программы"""
    # Сначала ищем в текущей директории
    if os.path.exists("Textilin.png"):
        return "Textilin.png"
    # Затем в директории с программой
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "Textilin.png")
    if os.path.exists(icon_path):
        return icon_path
    # Если иконка не найдена, возвращаем None
    return None

class SelectionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                          Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.CrossCursor)
        
        self.start_point = None
        self.end_point = None
        self.is_selecting = False
        
    def paintEvent(self, event):
        if self.start_point and self.end_point:
            painter = QPainter(self)
            painter.setPen(QColor(0, 120, 215))
            painter.setBrush(QColor(0, 120, 215, 30))
            rect = QRect(self.start_point, self.end_point)
            painter.drawRect(rect)
            
    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = self.start_point
        self.is_selecting = True
        
    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end_point = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        self.is_selecting = False
        if self.start_point and self.end_point:
            self.capture_area()
        self.close()
        
    def capture_area(self):
        try:
            if is_wayland():
                # В Wayland используем внешние утилиты
                import subprocess
                try:
                    # Проверяем наличие необходимых утилит
                    subprocess.run(['which', 'grim', 'slurp'], check=True, capture_output=True)
                    
                    # Запускаем процесс выбора области и создания скриншота
                    subprocess.run(get_screenshot_command(), shell=True, check=True)
                    
                    if not os.path.exists("temp_screenshot.png"):
                        raise Exception("Не удалось создать скриншот")
                        
                except subprocess.CalledProcessError:
                    self.parent.show_notification("Ошибка: Установите grim и slurp для работы в Wayland")
                    return
                except FileNotFoundError:
                    self.parent.show_notification("Ошибка: Установите grim и slurp для работы в Wayland")
                    return
            else:
                # В X11 используем стандартный механизм Qt
                screen = QApplication.primaryScreen()
                rect = QRect(self.start_point, self.end_point)
                rect = rect.normalized()
                
                # Получаем скриншот выбранной области
                screenshot = screen.grabWindow(0, rect.x(), rect.y(), 
                                            rect.width(), rect.height())
                
                # Конвертируем в формат PNG
                image = screenshot.toImage()
                image.save("temp_screenshot.png")
            
            # Распознаем текст
            with tesserocr.PyTessBaseAPI(lang=self.parent.current_language) as api:
                api.SetImageFile("temp_screenshot.png")
                text = api.GetUTF8Text()
                text = text.strip()
            
            # Удаляем временный файл
            if os.path.exists("temp_screenshot.png"):
                os.remove("temp_screenshot.png")
            
            if text:
                # Копируем в буфер обмена
                pyperclip.copy(text)
                
                # Показываем результат в главном окне
                if self.parent:
                    self.parent.show_result(text)
                    self.parent.show_notification("Текст скопирован в буфер обмена!")
            else:
                if self.parent:
                    self.parent.show_notification("Не удалось распознать текст")
                    
        except Exception as e:
            if self.parent:
                self.parent.show_notification(f"Ошибка: {str(e)}")

class TextilinLinux(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = "eng"  # По умолчанию английский
        self.initUI()
        self.setupTrayIcon()
        self.setupShortcuts()
        
    def initUI(self):
        self.setWindowTitle('Textilin')
        self.setGeometry(100, 100, 400, 300)
        
        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Добавляем метку с инструкциями
        self.status_label = QLabel('Нажмите Ctrl+Alt+C для копирования текста')
        layout.addWidget(self.status_label)
        
        # Добавляем выбор языка
        language_layout = QHBoxLayout()
        language_label = QLabel('Язык распознавания:')
        self.language_combo = QComboBox()
        self.language_combo.addItems(['Английский', 'Русский'])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        layout.addLayout(language_layout)
        
        # Добавляем текстовое поле для отображения результата
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Здесь появится распознанный текст...")
        layout.addWidget(self.result_text)
        
        # Создаем горизонтальный layout для кнопок
        button_layout = QHBoxLayout()
        
        # Добавляем кнопку для копирования
        copy_button = QPushButton('Копировать текст')
        copy_button.clicked.connect(self.start_selection)
        button_layout.addWidget(copy_button)
        
        # Добавляем кнопку закрытия
        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(self.quit_application)
        button_layout.addWidget(close_button)
        
        # Добавляем layout с кнопками в основной layout
        layout.addLayout(button_layout)
        
        # Устанавливаем флаги окна
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                          Qt.WindowType.FramelessWindowHint)
        
        # Устанавливаем стиль окна
        self.setStyleSheet("""
            QMainWindow {
                background: #2b2b2b;
                border: 1px solid #3f3f3f;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                padding: 5px;
                background: #3f3f3f;
                border: 1px solid #4f4f4f;
                border-radius: 3px;
                color: #ffffff;
            }
            QPushButton:hover {
                background: #4f4f4f;
            }
            QTextEdit {
                border: 1px solid #3f3f3f;
                border-radius: 3px;
                background: #3f3f3f;
                color: #ffffff;
            }
            QComboBox {
                padding: 5px;
                background: #3f3f3f;
                border: 1px solid #4f4f4f;
                border-radius: 3px;
                color: #ffffff;
            }
            QComboBox:hover {
                background: #4f4f4f;
            }
        """)
        
    def change_language(self, index):
        self.current_language = "rus" if index == 1 else "eng"
        
    def setupTrayIcon(self):
        # Создаем иконку в системном трее
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        
        # Создаем меню для иконки в трее
        tray_menu = QMenu()
        
        # Добавляем действия в меню
        show_action = QAction("Показать", self)
        quit_action = QAction("Выход", self)
        
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_application)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Добавляем обработку клика по иконке в трее
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # Одиночный клик
            if self.isVisible():
                self.hide()
            else:
                self.show()
                
    def setupShortcuts(self):
        # Создаем глобальное сочетание клавиш
        self.shortcut = QShortcut(QKeySequence("Ctrl+Alt+C"), self)
        self.shortcut.activated.connect(self.start_selection)
        
    def start_selection(self):
        self.hide()  # Скрываем основное окно
        QTimer.singleShot(100, self.show_selection_window)  # Небольшая задержка
        
    def show_selection_window(self):
        self.selection_window = SelectionWindow(self)
        self.selection_window.showFullScreen()
        
    def show_notification(self, message):
        self.tray_icon.showMessage("Textilin", message, 
                                  QSystemTrayIcon.MessageIcon.Information, 2000)
        
    def show_result(self, text):
        self.result_text.setText(text)
        self.show()  # Показываем окно с результатом
        
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()
        
    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()
        
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        
    def quit_application(self):
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Не закрывать приложение при закрытии окна
    window = TextilinLinux()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 