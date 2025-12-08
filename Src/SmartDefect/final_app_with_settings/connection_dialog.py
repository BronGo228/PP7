import tkinter as tk
from tkinter import ttk, messagebox
import json
import pyodbc

class ConnectionDialog(tk.Toplevel):
    def __init__(self, parent, config_path="config.json"):
        super().__init__(parent)
        self.title("Настройки подключения")
        self.resizable(False, False)
        self.config_path = config_path
        
        # Пытаемся загрузить существующий конфиг
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.cfg = json.load(f)
        except:
            self.cfg = {}

        # Интерфейс
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        self.e_server = self._entry(frm, "Server:", self.cfg.get("server", ""))
        self.e_db = self._entry(frm, "Database:", self.cfg.get("database", ""))
        self.e_user = self._entry(frm, "Username:", self.cfg.get("username", ""))
        self.e_pwd = self._entry(frm, "Password:", self.cfg.get("password", ""), show="*")
        
        # Драйвер по умолчанию
        default_driver = self.cfg.get("driver", "ODBC Driver 18 for SQL Server")
        self.e_driver = self._entry(frm, "Driver:", default_driver)

        ttk.Label(frm, text="Connection string (генерируется автоматически):").pack(anchor="w", pady=(10, 0))
        self.txt_conn = tk.Text(frm, height=4, width=50, wrap="word")
        self.txt_conn.pack(fill="x", pady=4)
        self.txt_conn.insert("1.0", self.cfg.get("connection_string", ""))

        # Кнопки
        btns = ttk.Frame(frm)
        btns.pack(fill="x", pady=15)
        
        ttk.Button(btns, text="Сформировать", command=self.generate).pack(side="left", padx=4)
        ttk.Button(btns, text="Проверить", command=self.test).pack(side="left", padx=4)
        ttk.Button(btns, text="Сохранить", command=self.save).pack(side="right", padx=4)
        
        # Настройки окна
        self.grab_set()
        self.focus_set()

    def _entry(self, frm, label, val, show=None):
        ttk.Label(frm, text=label).pack(anchor="w")
        e = ttk.Entry(frm, show=show)
        e.pack(fill="x", pady=(0, 5))
        if val:
            e.insert(0, val)
        return e

    def generate(self):
        server = self.e_server.get()
        db = self.e_db.get()
        user = self.e_user.get()
        pwd = self.e_pwd.get()
        driver = self.e_driver.get()
        
        # Формирование строки подключения
        # Важно: фигурные скобки для драйвера нужны, если в названии есть пробелы
        base = f"DRIVER={{{driver}}};SERVER={server};DATABASE={db};"
        
        if user.strip():
            conn_str = base + f"UID={user};PWD={pwd};"
        else:
            conn_str = base + "Trusted_Connection=yes;"
            
        self.txt_conn.delete("1.0", "end")
        self.txt_conn.insert("1.0", conn_str)

    def test(self):
        conn_str = self.txt_conn.get("1.0", "end").strip()
        if not conn_str:
            messagebox.showwarning("Внимание", "Сначала сформируйте строку подключения")
            return
        try:
            pyodbc.connect(conn_str)
            messagebox.showinfo("Успех", "Подключение успешно установлено!")
        except Exception as e:
            messagebox.showerror("Ошибка подключения", str(e))

    def save(self):
        cfg = {
            "server": self.e_server.get(),
            "database": self.e_db.get(),
            "username": self.e_user.get(),
            "password": self.e_pwd.get(),
            "driver": self.e_driver.get(),
            "connection_string": self.txt_conn.get("1.0", "end").strip()
        }
        
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Сохранено", "Настройки сохранены. Переподключитесь в главном меню.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))