import os
import cv2 as cv
import numpy as np
from PIL import Image, ImageEnhance
import tkinter as tk
from tkinter import font, filedialog, messagebox, scrolledtext, ttk

FILE_PATH = 'braille_image.txt'

SIMPLE_BRAILLE_CHARACTERS = [
    '\u2800',  # ⠀ 
    '\u2819',  # ⠙ 
    '\u283A',  # ⠺ 
    '\u28B6',  # ⠶ 
    '\u287F',  # ⡿ 
    '\u289F',  # ⢟ 
    '\u28F6',  # ⣶ 
    '\u28FF',  # ⣿ 
]

BRAILLE_CHARACTERS = [
    '\u2801', '\u2803', '\u2809', '\u2819', '\u2811',
    '\u280b', '\u281b', '\u2813', '\u280a', '\u281a',
    '\u2805', '\u2807', '\u280d', '\u281d', '\u2809',
    '\u280f', '\u281f', '\u2817', '\u280e', '\u281e',
    '\u2825', '\u2827', '\u283a', '\u282d', '\u283d',
    '\u2835', '\u2800'
]

ASCII_CHARACTERS = [
    ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',',
    '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
    'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', ']', '^', '_', '`',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '{', '|', '}', '~'
]

def center_window(root, width=800, height=600):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    root.geometry(f'{width}x{height}+{x}+{y}')

# this will be replaced by a GUI form :3
def pick_image():
    images_dir = os.path.expanduser('images/')

    image_names = [name
                   for root, dirs, files in os.walk(images_dir)
                   for name in files
                   if name.endswith((".jpeg", ".png", ".jpg"))]

    for number, i in enumerate(image_names):
        print(f"[{number + 1}] {i}")
    
    pick = int(input("which image would you like to convert?: "))

    path = f'images/{image_names[pick - 1]}'
    image = Image.open(path)

    return image

def open_file(text_widget):
    try:
        with open(FILE_PATH, 'r') as file:
            content = file.read()
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)  
    except FileNotFoundError:
        text_widget.insert(tk.END, "File not found.")
    
def resize_image(image, new_width):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def colorize(image, colored_image):
    colors = colored_image.getdata()
    characters = []
    for i, character in enumerate(image):
        color = colors[i]
        characters.append(f"\x1b[38;2;{color[0]};{color[1]};{color[2]}m{character}\x1b[0m")
        
    return characters

def grayscaleimage(image):
    grayscale_image = image.convert("L")
    return grayscale_image

def enhance_contrast(image, value):
    enhancer = ImageEnhance.Contrast(image)
    enhanced_image = enhancer.enhance(value)  
    return enhanced_image


def pixels_to_braille(image, style, enhanced_image):
    pixels = enhanced_image.getdata()
    if style == 'braille':
        characters = "".join([BRAILLE_CHARACTERS[pixel // 32] for pixel in pixels])
    elif style == 'simple': 
        characters = "".join([SIMPLE_BRAILLE_CHARACTERS[pixel // 32] for pixel in pixels])
    else:
        characters = "".join([ASCII_CHARACTERS[pixel // 32] for pixel in pixels])
    return characters
    
def user_controls(root, attributes):
    def size_slider_change(value):
        rounded_value = round(float(value) / 10) * 10 
        size_slider_label.config(text=f"Size Slider: {rounded_value}")
        attributes['size'] = rounded_value
        main(attributes, False)
        open_file(text_widget)

    def contrast_slider_change(value):
        contrast_slider_label.config(text=f"Contrast Slider: {value}")
        attributes['contrast'] = float(value)
        main(attributes, False)
        open_file(text_widget)

    def ascii_button():
        attributes.update({'style': 'ascii'})
        main(attributes, False)
        open_file(text_widget)
    
    def braille_button():
        attributes.update({'style': 'braille'})
        main(attributes, False)
        open_file(text_widget)
    
    def simple_button():
        attributes.update({'style': 'simple'})
        main(attributes, False)
        open_file(text_widget)
    
    def color_button():
        main(attributes, True)
    
    right_bar = tk.Frame(root, width=100, bg='lightgray', padx=10, pady=10)
    right_bar.pack(side=tk.RIGHT, fill='y')

    text_widget = scrolledtext.ScrolledText(root, wrap='word', bg='black', fg='white', font=('TkFixedFont', 18))
    text_widget.pack(expand=True, fill='both', padx=10, pady=10)

    small_font = font.Font(family="Courier New", size=6)

    text_widget.configure(font=small_font)

    open_file(text_widget)

    button1 = ttk.Button(right_bar, text="ASCII", command=ascii_button)
    button1.pack(pady=5, fill='x')

    button2 = ttk.Button(right_bar, text="BRAILLE", command=braille_button)
    button2.pack(pady=5, fill='x')

    button3 = ttk.Button(right_bar, text="SIMPLE", command=simple_button)
    button3.pack(pady=5, fill='x')

    button4 = ttk.Button(right_bar, text="COLORS", command=color_button)
    button4.pack(pady=5, fill='x')

    size_slider_label = ttk.Label(right_bar, text="Size Slider:")
    size_slider_label.pack(pady=(10, 5), anchor=tk.W)

    size_slider = ttk.Scale(right_bar, from_=100, to=200, length=200, orient=tk.HORIZONTAL ,command=size_slider_change)
    size_slider.pack(fill='x')

    contrast_slider_label = ttk.Label(right_bar, text="Contrast Slider:")
    contrast_slider_label.pack(pady=(10, 5), anchor=tk.W)

    contrast_slider = ttk.Scale(right_bar, from_=1, to=2, length=200, orient=tk.HORIZONTAL, command=contrast_slider_change)
    contrast_slider.pack(fill='x')

def main(attributes, print_colors):
    image = attributes['image']
    new_width = attributes['size']

    resized_image = resize_image(image, new_width)
    grayscale_image = grayscaleimage(resized_image)
    enhanced_image = enhance_contrast(grayscale_image, attributes['contrast'])
    new_image_data = pixels_to_braille(enhanced_image, attributes['style'], enhanced_image)
    
    colorized_image = colorize(new_image_data, resized_image)

    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i + new_width)] for i in range(0, pixel_count, new_width))

    with open("braille_image.txt", "w") as f:
        f.write(ascii_image)
    
    if print_colors == True:
        colored_pixel_count = len(colorized_image)
        colored_ascii_image = "\n".join("".join(colorized_image[i:(i + new_width)]) for i in range(0, colored_pixel_count, new_width))
        print(colored_ascii_image)

    
    

if __name__ == "__main__":
    attributes = {
        'size' : 100,
        'style' : 'braille',
        'contrast' : 1,
        'image' : pick_image()
    }
    main(attributes, print_colors=False)
    root = tk.Tk()
    root.title("IMG Converter")
    center_window(root, width=1920, height=1080)
    user_controls(root, attributes)
    root.mainloop()