import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Создаём главное окно
root = tk.Tk()
root.title("Text Editor")
root.geometry("700x500")  # Сделаем окно побольше для удобства

# Создаём текстовое поле с полосой прокрутки
text_frame = tk.Frame(root)
text_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text = tk.Text(text_frame, yscrollcommand=scrollbar.set, undo=True)
text.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=text.yview)

# Настройка растягивания окна
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


# --- Функция сохранения файла ---
def saveas():
    global text
    t = text.get("1.0", "end-1c")
    savelocation = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"),
                                                           ("All files", "*.*")])
    if savelocation:
        with open(savelocation, "w", encoding="utf-8") as file1:
            file1.write(t)
        root.title(f"Text Editor - {savelocation}")


# --- Модификация 1: Открытие файлов ---
def open_file():
    open_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text files", "*.txt"),
                                                      ("All files", "*.*")])
    if open_path:
        with open(open_path, "r", encoding="utf-8") as file:
            content = file.read()
        text.delete("1.0", tk.END)
        text.insert("1.0", content)
        root.title(f"Text Editor - {open_path}")


# --- Модификация 2: Тёмная тема ---
dark_mode = False


def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        root.configure(bg="#2b2b2b")
        text_frame.configure(bg="#2b2b2b")
        text.configure(bg="#3c3f41", fg="#ffffff", insertbackground="white")
        scrollbar.configure(bg="#4a4a4a", troughcolor="#2b2b2b")
        for widget in [button, open_button, clear_button, search_button, font, dark_button]:
            widget.configure(bg="#4a4a4a", fg="white", activebackground="#666666")
        word_count_label.configure(bg="#2b2b2b", fg="#888888")
    else:
        root.configure(bg="#f0f0f0")
        text_frame.configure(bg="#f0f0f0")
        text.configure(bg="white", fg="black", insertbackground="black")
        scrollbar.configure(bg="#e0e0e0", troughcolor="#f0f0f0")
        for widget in [button, open_button, clear_button, search_button, font, dark_button]:
            widget.configure(bg="#e0e0e0", fg="black", activebackground="#cccccc")
        word_count_label.configure(bg="#f0f0f0", fg="#666666")


# --- Модификация 3: Очистить всё ---
def clear_all():
    """Очищает всё текстовое поле"""
    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить весь текст?"):
        text.delete("1.0", tk.END)
        update_word_count()  # Обновляем счётчик


# --- Модификация 4: Счётчик слов ---
def update_word_count(event=None):
    """Обновляет счётчик слов в реальном времени"""
    content = text.get("1.0", "end-1c")

    # Считаем символы (без пробелов и с пробелами)
    char_count = len(content)
    char_no_space = len(content.replace(" ", "").replace("\n", ""))

    # Считаем слова
    words = content.split()
    word_count = len(words)

    # Считаем строки
    lines = content.split("\n")
    line_count = len(lines)

    word_count_label.config(text=f"Слов: {word_count} | Символов: {char_count} | Строк: {line_count}")


# --- Модификация 5: Поиск текста ---
def search_text():
    """Поиск текста в документе"""
    search_term = simpledialog.askstring("Поиск", "Введите текст для поиска:")
    if not search_term:
        return

    # Снимаем предыдущую подсветку
    text.tag_remove("search", "1.0", tk.END)

    # Ищем все вхождения
    start_pos = "1.0"
    found_count = 0

    while True:
        start_pos = text.search(search_term, start_pos, stopindex=tk.END)
        if not start_pos:
            break

        end_pos = f"{start_pos}+{len(search_term)}c"
        text.tag_add("search", start_pos, end_pos)
        found_count += 1
        start_pos = end_pos

    # Настройка подсветки найденного
    text.tag_config("search", background="yellow", foreground="black")

    # Показываем результат
    if found_count > 0:
        messagebox.showinfo("Результат поиска", f"Найдено {found_count} совпадений")
        # Перемещаемся к первому результату
        text.see("1.0")
    else:
        messagebox.showinfo("Результат поиска", "Текст не найден")


# --- Кнопки ---
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=5, sticky="ew")

button = tk.Button(button_frame, text="💾 Save", command=saveas, padx=10)
button.pack(side=tk.LEFT, padx=2, pady=5)

open_button = tk.Button(button_frame, text="📂 Open", command=open_file, padx=10)
open_button.pack(side=tk.LEFT, padx=2, pady=5)

clear_button = tk.Button(button_frame, text="🗑 Очистить всё", command=clear_all, padx=10)
clear_button.pack(side=tk.LEFT, padx=2, pady=5)

search_button = tk.Button(button_frame, text="🔍 Поиск", command=search_text, padx=10)
search_button.pack(side=tk.LEFT, padx=2, pady=5)

dark_button = tk.Button(button_frame, text="🌙 Dark Mode", command=toggle_theme, padx=10)
dark_button.pack(side=tk.LEFT, padx=2, pady=5)


# --- Меню шрифта ---
def FontHelvetica():
    global text
    text.config(font=("Helvetica", 12))


def FontCourier():
    global text
    text.config(font=("Courier", 12))


font = tk.Menubutton(button_frame, text="✏ Font", relief=tk.RAISED, padx=10)
font.pack(side=tk.LEFT, padx=2, pady=5)
font.menu = tk.Menu(font, tearoff=0)
font["menu"] = font.menu

helvetica = tk.IntVar()
courier = tk.IntVar()

font.menu.add_checkbutton(label="Helvetica", variable=helvetica, command=FontHelvetica)
font.menu.add_checkbutton(label="Courier", variable=courier, command=FontCourier)

# --- Счётчик слов (внизу) ---
word_count_label = tk.Label(root, text="Слов: 0 | Символов: 0 | Строк: 0",
                            font=("Arial", 9), anchor="w")
word_count_label.grid(row=2, column=0, columnspan=5, sticky="ew", padx=5, pady=2)

# Привязываем обновление счётчика к изменению текста
text.bind("<KeyRelease>", update_word_count)
text.bind("<<Modified>>", update_word_count)

# Запускаем приложение
root.mainloop()
