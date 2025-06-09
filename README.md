# Textilin

Программа для копирования текста с помощью OCR в Linux.
Замена Textify для Linux
## Системные требования

- Linux (Ubuntu/Debian/Mint, Fedora, Arch Linux)
- Python 3.8 или выше
- Tesseract OCR
- Для Wayland: grim и slurp
- Для X11: scrot

## Установка системных зависимостей

### Ubuntu/Debian/Mint
```bash
# Обновление списка пакетов
sudo apt update

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv

# Установка Tesseract OCR
sudo apt install tesseract-ocr

# Установка дополнительных языковых пакетов для Tesseract (опционально)
sudo apt install tesseract-ocr-rus  # для русского языка
sudo apt install tesseract-ocr-eng  # для английского языка

# Установка зависимостей для скриншотов
sudo apt install scrot  # для X11
sudo apt install grim slurp  # для Wayland
```

### Fedora
```bash
# Установка Python и pip
sudo dnf install python3 python3-pip

# Установка Tesseract OCR
sudo dnf install tesseract

# Установка дополнительных языковых пакетов
sudo dnf install tesseract-langpack-rus  # для русского языка
sudo dnf install tesseract-langpack-eng  # для английского языка

# Установка зависимостей для скриншотов
sudo dnf install scrot  # для X11
sudo dnf install grim slurp  # для Wayland
```

### Arch Linux
```bash
# Установка Python и pip
sudo pacman -S python python-pip

# Установка Tesseract OCR
sudo pacman -S tesseract

# Установка дополнительных языковых пакетов
sudo pacman -S tesseract-data-rus  # для русского языка
sudo pacman -S tesseract-data-eng  # для английского языка

# Установка зависимостей для скриншотов
sudo pacman -S scrot  # для X11
sudo pacman -S grim slurp  # для Wayland
```

## Установка программы

### Вариант 1: Установка из исходного кода

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Antonass/textilin.git
cd textilin
```

2. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости Python:
```bash
pip install -r requirements.txt
```
1. Скачайте последнюю версию Textilin-x86_64.AppImage
2. Сделайте файл исполняемым:
```bash
chmod +x create_appimage.sh
```
3. Запустите программу:
```bash
./create_appimage.sh
```

### Вариант 2: Сборка AppImage

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Antonass/textilin.git
cd textilin
```

2. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости Python:
```bash
pip install -r requirements.txt
```

4. Сделайте файл исполняемым:
```bash
chmod +x create_appimage.sh
```
5. Запустите программу:
```bash
./create_appimage.sh
```

## Использование

1. Запустите программу
2. Нажмите кнопку "Копировать текст" или используйте сочетание клавиш Ctrl+Alt+C
3. Выберите область экрана с текстом
4. Текст будет скопирован в буфер обмена и отображен в окне программы

## Особенности

- Копирование текста с помощью OCR
- Работа в системном трее
- Горячие клавиши
- Уведомления
- Поддержка X11 и Wayland
- Автономный AppImage (не требует установки Python и зависимостей)

## Устранение неполадок

### Программа не запускается
- Убедитесь, что файл AppImage имеет права на выполнение
- Проверьте, что установлены необходимые зависимости для скриншотов

### Не работает распознавание текста
- Проверьте качество изображения (текст должен быть четким)
- Убедитесь, что текст на изображении читаемый

### Не работает создание скриншотов
- Для X11: убедитесь, что установлен scrot
- Для Wayland: убедитесь, что установлены grim и slurp
- Проверьте права доступа к экрану

## Лицензия

MIT License 
