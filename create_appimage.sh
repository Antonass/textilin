#!/bin/bash

# Устанавливаем архитектуру
export ARCH=x86_64

# Создаем необходимые директории
mkdir -p Textilin.AppDir/usr/{bin,lib,share}

# Копируем основной скрипт
cp textilin.py Textilin.AppDir/usr/bin/

# Создаем директорию для Python пакетов и копируем их
mkdir -p Textilin.AppDir/usr/lib/python3.12/site-packages
cp -r venv/lib/python3.12/site-packages/* Textilin.AppDir/usr/lib/python3.12/site-packages/

# Копируем Python интерпретатор
cp venv/bin/python3 Textilin.AppDir/usr/bin/

# Копируем системные библиотеки
ldd venv/bin/python3 | grep "=> /" | awk '{print $3}' | xargs -I '{}' cp -v '{}' Textilin.AppDir/usr/lib/ || true

# Создаем директорию для данных Tesseract и копируем их
mkdir -p Textilin.AppDir/usr/share/tessdata
if [ -d "/usr/share/tesseract-ocr/5/tessdata" ]; then
    cp -r /usr/share/tesseract-ocr/5/tessdata/* Textilin.AppDir/usr/share/tessdata/
else
    echo "Ошибка: Директория /usr/share/tesseract-ocr/5/tessdata не найдена"
    echo "Установите Tesseract OCR: sudo apt install tesseract-ocr"
    exit 1
fi

# Проверяем наличие файлов языковых пакетов
if [ ! -f "Textilin.AppDir/usr/share/tessdata/eng.traineddata" ]; then
    echo "Ошибка: Файл eng.traineddata не найден"
    echo "Установите английский языковой пакет: sudo apt install tesseract-ocr-eng"
    exit 1
fi

if [ ! -f "Textilin.AppDir/usr/share/tessdata/rus.traineddata" ]; then
    echo "Ошибка: Файл rus.traineddata не найден"
    echo "Установите русский языковой пакет: sudo apt install tesseract-ocr-rus"
    exit 1
fi

# Создаем AppRun скрипт
cat > Textilin.AppDir/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin/:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib/:${LD_LIBRARY_PATH}"
export PYTHONPATH="${HERE}/usr/lib/python3.12/site-packages:${PYTHONPATH}"
export TESSDATA_PREFIX="${HERE}/usr/share/tessdata"

# Проверяем наличие tessdata
if [ ! -d "${TESSDATA_PREFIX}" ]; then
    echo "Ошибка: директория tessdata не найдена"
    exit 1
fi

if [ ! -f "${TESSDATA_PREFIX}/eng.traineddata" ]; then
    echo "Ошибка: файл eng.traineddata не найден"
    exit 1
fi

if [ ! -f "${TESSDATA_PREFIX}/rus.traineddata" ]; then
    echo "Ошибка: файл rus.traineddata не найден"
    exit 1
fi

# Запускаем программу
exec "${HERE}/usr/bin/python3" "${HERE}/usr/bin/textilin.py" "$@"
EOF

chmod +x Textilin.AppDir/AppRun

# Создаем .desktop файл
cat > Textilin.AppDir/Textilin.desktop << EOL
[Desktop Entry]
Name=Textilin
Exec=AppRun
Icon=Textilin
Type=Application
Categories=Utility;
Comment=Программа для копирования текста с экрана с помощью OCR
EOL

# Копируем иконку
cp Textilin.png Textilin.AppDir/

# Скачиваем appimagetool
wget -O appimagetool "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
chmod +x appimagetool

# Создаем AppImage
./appimagetool Textilin.AppDir

# Очищаем временные файлы
rm -f appimagetool
rm -rf Textilin.AppDir 