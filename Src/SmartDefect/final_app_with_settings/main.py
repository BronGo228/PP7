import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os, json
from helpers import connect, load_config
# Импортируем ОБА диалога
from dialogs import RecordDialog 
from connection_dialog import ConnectionDialog

CONFIG_FILE = 'config.json'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Обнаружения царапин и сколов на экранах смартфонов')
        self.geometry('1100x650')
        self.minsize(900, 600)
        
        self.conn = None
        self.cfg = load_config(CONFIG_FILE)
        self.current_table = None
        
        # --- Меню настроек ---
        menubar = tk.Menu(self)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Настройки подключения", command=self.open_settings)
        menubar.add_cascade(label="Настройки", menu=settings_menu)
        self.config(menu=menubar)
        # ---------------------
        
        self.create_ui()

    def create_ui(self):
        root = ttk.Frame(self, padding=0)
        root.pack(fill='both', expand=True)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ttk.Frame(root, width=200, padding=10, relief='flat')
        sidebar.grid(row=0, column=0, sticky='nsw')
        
        ttk.Label(sidebar, text='Меню', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 8))
        
        for name in ['Устройства', 'Проверка', 'Дефекты', 'Пользователи']:
            btn = ttk.Button(sidebar, text=name, width=20, 
                             command=lambda n=name: self.show_table(n))
            btn.pack(anchor='w', pady=4)
            
        ttk.Separator(sidebar, orient='horizontal').pack(fill='x', pady=8)
        
        ttk.Button(sidebar, text='Подключить', command=self.connect_db).pack(fill='x', pady=4)
        ttk.Button(sidebar, text='Отключить', command=self.disconnect_db).pack(fill='x', pady=4)
        ttk.Button(sidebar, text='Добавить пользователя', command=self.add_sql_user).pack(fill='x', pady=4)
        ttk.Button(sidebar, text='Создать роль', command=self.add_sql_role).pack(fill='x', pady=4)

        # Main Area
        main = ttk.Frame(root, padding=10)
        main.grid(row=0, column=1, sticky='nsew')
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        self.header_var = tk.StringVar(value='Отключено')
        header = ttk.Label(main, textvariable=self.header_var, font=('Segoe UI', 14, 'bold'))
        header.grid(row=0, column=0, sticky='w')

        toolbar = ttk.Frame(main)
        toolbar.grid(row=0, column=1, sticky='e')
        
        ttk.Button(toolbar, text='Добавить', command=self.add_record).pack(side='left', padx=4)
        ttk.Button(toolbar, text='Изменить', command=self.edit_record).pack(side='left', padx=4)
        ttk.Button(toolbar, text='Удалить', command=self.delete_record).pack(side='left', padx=4)
        ttk.Button(toolbar, text='Обновить', command=self.refresh_table).pack(side='left', padx=4)

        table_frame = ttk.Frame(main)
        table_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(8, 0))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, show='headings')
        vsb = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Details
        details = ttk.Frame(root, width=320, padding=10, relief='groove')
        details.grid(row=0, column=2, sticky='nse', padx=(6, 10), pady=10)
        
        ttk.Label(details, text='Подробности', font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        self.detail_text = tk.Text(details, height=20, width=40, wrap='word')
        self.detail_text.pack(fill='both', expand=True, pady=(6, 0))

        # Status Bar
        self.status_var = tk.StringVar(value='Готов к работе')
        status = ttk.Label(self, textvariable=self.status_var, relief='sunken', anchor='w')
        status.pack(side='bottom', fill='x')

    # --- Открытие настроек ---
    def open_settings(self):
        dlg = ConnectionDialog(self)
        self.wait_window(dlg)
        self.cfg = load_config(CONFIG_FILE)
        self.status_var.set("Конфигурация обновлена.")

    # --- БД Методы ---
    def connect_db(self):
        if self.conn:
            messagebox.showinfo('Info', 'Уже подключен')
            return
        
        # Здесь программа может "повиснуть" на 15 сек, если сервер недоступен
        # Это нормально для pyodbc, если конфиг неверный
        try:
            self.conn = connect(self.cfg)
            srv = self.cfg.get('server', 'Server')
            db = self.cfg.get('database', 'DB')
            self.header_var.set(f"Подключен: {db} @ {srv}")
            self.status_var.set('Подключен к базе данных')
            messagebox.showinfo('Connected', 'Успешно подключен к базе данных')
        except Exception as e:
            messagebox.showerror('Ошибка подключения', f"Не удалось подключиться.\nПроверьте настройки.\n\nОшибка: {str(e)}")
            self.status_var.set('Ошибка подключения')

    def disconnect_db(self):
        if self.conn:
            try:
                self.conn.close()
            except:
                pass
        self.conn = None
        self.header_var.set('Отключен')
        self.status_var.set('Отключен')
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = ()
        self.detail_text.delete('1.0', 'end')

    def show_table(self, table_name):
        if not self.conn:
            messagebox.showwarning('Warning', 'Сначала подключитесь к базе данных')
            return
        
        self.current_table = table_name
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM [{table_name}]")
            rows = cur.fetchall()
            
            if cur.description:
                cols = [c[0] for c in cur.description]
            else:
                cols = []

            self.tree.delete(*self.tree.get_children())
            self.tree['columns'] = cols
            
            for c in cols:
                self.tree.heading(c, text=c)
                self.tree.column(c, width=120, anchor='w')
            
            for r in rows:
                self.tree.insert('', 'end', values=[str(x) if x is not None else '' for x in r])
                
            self.status_var.set(f'Таблица: {table_name}, записей: {len(rows)}')
            self.detail_text.delete('1.0', 'end')
            
        except Exception as e:
            messagebox.showerror('Ошибка загрузки таблицы', str(e))

    def refresh_table(self):
        if self.current_table:
            self.show_table(self.current_table)

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], 'values')
        cols = self.tree['columns']
        
        txt = '\n'.join([f"{c}: {v}" for c, v in zip(cols, vals)])
        self.detail_text.delete('1.0', 'end')
        self.detail_text.insert('1.0', txt)

    def add_record(self):
        if not self.current_table:
            messagebox.showwarning('Warning', 'Выберите таблицу')
            return
            
        cols = self.tree['columns']
        if not cols:
            return

        fields = {c: '' for c in cols[1:]}
        dlg = RecordDialog(self, title=f'Добавить в {self.current_table}', fields=fields)
        
        if dlg.result:
            # Превращаем пустые строки в None для NULL в базе
            data_to_insert = {k: (v if v.strip() != '' else None) for k, v in dlg.result.items()}
            
            vals = list(data_to_insert.values())
            cols_names = ','.join([f"[{k}]" for k in data_to_insert.keys()])
            placeholders = ','.join(['?'] * len(vals))
            
            sql = f"INSERT INTO [{self.current_table}] ({cols_names}) VALUES ({placeholders})"
            
            try:
                cur = self.conn.cursor()
                cur.execute(sql, vals)
                self.conn.commit()
                self.status_var.set('Запись добавлена')
                self.refresh_table()
            except Exception as e:
                messagebox.showerror('Ошибка добавления', str(e))

    def edit_record(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Warning', 'Выберите строку')
            return
            
        vals = self.tree.item(sel[0], 'values')
        cols = self.tree['columns']
        pk_col = cols[0]
        pk_val = vals[0]
        
        fields = {c: v for c, v in zip(cols[1:], vals[1:])}
        dlg = RecordDialog(self, title=f'Изменить {self.current_table}', fields=fields)
        
        if dlg.result:
            data_to_update = {k: (v if v.strip() != '' else None) for k, v in dlg.result.items()}
            
            set_clause = ','.join([f"[{c}]=?" for c in data_to_update.keys()])
            params = list(data_to_update.values()) + [pk_val]
            
            sql = f"UPDATE [{self.current_table}] SET {set_clause} WHERE [{pk_col}]=?"
            
            try:
                cur = self.conn.cursor()
                cur.execute(sql, params)
                self.conn.commit()
                self.status_var.set('Запись обновлена')
                self.refresh_table()
            except Exception as e:
                messagebox.showerror('Ошибка обновления', str(e))

    def delete_record(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Warning', 'Выберите строку')
            return
            
        if not messagebox.askyesno('Подтверждение', 'Удалить запись?'):
            return
            
        vals = self.tree.item(sel[0], 'values')
        cols = self.tree['columns']
        pk_col = cols[0]
        pk_val = vals[0]
        
        try:
            cur = self.conn.cursor()
            cur.execute(f"DELETE FROM [{self.current_table}] WHERE [{pk_col}]=?", (pk_val,))
            self.conn.commit()
            self.status_var.set('Запись удалена')
            self.refresh_table()
        except Exception as e:
            messagebox.showerror('Ошибка удаления', str(e))

    def add_sql_user(self):
        if not self.conn:
            messagebox.showwarning('Warning', 'Нет подключения к БД')
            return
        login = simpledialog.askstring('Add SQL Login', 'Login:')
        pwd = simpledialog.askstring('Add SQL Login', 'Password:', show='*')
        if not login or not pwd: return
            
        try:
            cur = self.conn.cursor()
            cur.execute(f"CREATE LOGIN [{login}] WITH PASSWORD = '{pwd}'")
            cur.execute(f"CREATE USER [{login}] FOR LOGIN [{login}]")
            self.conn.commit()
            messagebox.showinfo('Success', f'Пользователь {login} создан')
        except Exception as e:
            messagebox.showerror('Ошибка', str(e))

    def add_sql_role(self):
        if not self.conn:
            messagebox.showwarning('Warning', 'Нет подключения к БД')
            return
        role = simpledialog.askstring('Create Role', 'Role name:')
        if not role: return
            
        try:
            cur = self.conn.cursor()
            cur.execute(f"CREATE ROLE [{role}]")
            self.conn.commit()
            messagebox.showinfo('Success', f'Роль {role} создана')
        except Exception as e:
            messagebox.showerror('Ошибка', str(e))

if __name__ == '__main__':
    app = App()
    app.mainloop()