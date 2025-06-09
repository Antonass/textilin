from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Создаем изображение 256x256 пикселей
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Рисуем круг
    circle_color = (0, 120, 215, 255)  # Синий цвет
    draw.ellipse([20, 20, size-20, size-20], fill=circle_color)
    
    # Добавляем текст
    try:
        # Пробуем использовать системный шрифт
        font = ImageFont.truetype("DejaVuSans-Bold", 80)
    except:
        # Если не получилось, используем шрифт по умолчанию
        font = ImageFont.load_default()
    
    text = "T"
    text_color = (255, 255, 255, 255)  # Белый цвет
    
    # Вычисляем размер текста для центрирования
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Позиционируем текст по центру
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Рисуем текст
    draw.text((x, y), text, font=font, fill=text_color)
    
    # Сохраняем иконку
    image.save("Textilin.png")
    print("Иконка Textilin.png создана успешно!")

if __name__ == "__main__":
    create_icon() 