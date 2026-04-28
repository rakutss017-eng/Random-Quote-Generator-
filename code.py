import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Создание переменой с названием файла для хранения истории
HISTORY_FILE = 'quotes_history.json'

# Список цитат
quotes = [
    {"text": "Будь тем изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "мотивация"},
    {"text": "Успех — это сумма маленьких усилий, повторяемых день за днём.", "author": "Роберт Коллье", "topic": "успех"},
    {"text": "Жизнь — это то, что происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "жизнь"},
]

history = []

def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

def save_history():
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def generate_quote():
    quote = random.choice(quotes)
    display_quote(quote)
    # Добавляем в историю
    history.append(quote)
    save_history()
    update_history_listbox()

def display_quote(quote):
    quote_text.config(state='normal')
    quote_text.delete(1.0, tk.END)
    quote_text.insert(tk.END, f'"{quote["text"]}"\n\n- {quote["author"]}\nТема: {quote["topic"]}')
    quote_text.config(state='disabled')

def update_history_listbox():
    listbox_history.delete(0, tk.END)
    for q in reversed(history):
        listbox_history.insert(tk.END, f'"{q["text"]}" — {q["author"]} ({q["topic"]})')

def filter_quotes():
    author_filter = entry_author.get().strip().lower()
    topic_filter = entry_topic.get().strip().lower()

    filtered = []
    for q in history:
        if author_filter and author_filter not in q["author"].lower():
            continue
        if topic_filter and topic_filter not in q["topic"].lower():
            continue
        filtered.append(q)

    listbox_history.delete(0, tk.END)
    for q in reversed(filtered):
        listbox_history.insert(tk.END, f'"{q["text"]}" — {q["author"]} ({q["topic"]})')

def clear_filters():
    entry_author.delete(0, tk.END)
    entry_topic.delete(0, tk.END)
    update_history_listbox()

window = tk.Tk()
window.title("Random Quote Generator")
window.geometry("300x300")

frame_controls = tk.Frame(window)
frame_controls.pack(padx=10, pady=10)

# Кнопка генерации
btn_generate = tk.Button(frame_controls, text="Сгенерировать цитату", command=generate_quote)
btn_generate.pack()

quote_text = tk.Text(window, height=8, width=60, wrap='word', state='disabled', font=('Arial', 12))
quote_text.pack(padx=10, pady=10)

# Фильтры
frame_filters = tk.Frame(window)
frame_filters.pack(padx=10, pady=5)

tk.Label(frame_filters, text="Автор:").grid(row=0, column=0, padx=5, pady=5)
entry_author = tk.Entry(frame_filters)
entry_author.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_filters, text="Тема:").grid(row=0, column=2, padx=5, pady=5)
entry_topic = tk.Entry(frame_filters)
entry_topic.grid(row=0, column=3, padx=5, pady=5)

btn_filter = tk.Button(frame_filters, text="Фильтр", command=filter_quotes)
btn_filter.grid(row=0, column=4, padx=5, pady=5)

btn_clear = tk.Button(frame_filters, text="Сбросить фильтр", command=clear_filters)
btn_clear.grid(row=0, column=5, padx=5, pady=5)

# История
tk.Label(window, text="История цитат:").pack()
listbox_history = tk.Listbox(window, width=80, height=10)
listbox_history.pack(padx=10, pady=10)

load_history()
update_history_listbox()

window.mainloop()
