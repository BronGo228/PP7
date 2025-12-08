import tkinter as tk
from tkinter import ttk

class RecordDialog(tk.Toplevel):
    def __init__(self, parent, title='Record', fields=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.resizable(False, False)
        self.result = None
        
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill='both', expand=True)
        
        self.entries = {}
        if not fields:
            fields = {}
            
        # Создаем поля ввода
        for i, (k, v) in enumerate(fields.items()):
            ttk.Label(frm, text=f"{k}:").grid(row=i, column=0, sticky='w', pady=4, padx=5)
            e = ttk.Entry(frm, width=30)
            e.grid(row=i, column=1, sticky='ew', pady=4, padx=5)
            
            # Если есть значение (редактирование), вставляем его
            if v is not None:
                e.insert(0, str(v))
            
            self.entries[k] = e
            
        # Кнопки
        btns = ttk.Frame(frm)
        btns.grid(row=len(fields), column=0, columnspan=2, pady=(15, 0))
        
        ttk.Button(btns, text='OK', command=self.on_ok).pack(side='left', padx=6)
        ttk.Button(btns, text='Отмена', command=self.destroy).pack(side='left', padx=6)
        
        self.columnconfigure(0, weight=1)
        
        # Модальность окна
        self.wait_visibility()
        self.grab_set()
        self.focus_set() 
        self.wait_window(self)

    def on_ok(self):
        # Собираем данные. Пустые строки оставляем как есть,
        # обработка NULL будет происходить в main.py
        data = {k: e.get() for k, e in self.entries.items()}
        self.result = data
        self.destroy()