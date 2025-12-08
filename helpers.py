import pyodbc
import json, os

def build_conn_str(cfg):
    # [cite_start]Если есть готовая строка подключения, используем её (как в варианте из PDF) [cite: 512-513]
    if cfg.get("connection_string", "").strip():
        return cfg["connection_string"]

    driver = cfg.get('driver', 'ODBC Driver 18 for SQL Server')
    server = cfg.get('server', 'localhost')
    database = cfg.get('database', 'SmartphoneDefectsDB')
    uid = cfg.get('username','')
    pwd = cfg.get('password','')
    
    if uid:
        return f"DRIVER={{{driver}}}; SERVER={server}; DATABASE={database}; UID={uid}; PWD={pwd}" 
    else:
        return f"DRIVER={{{driver}}}; SERVER={server}; DATABASE={database}; Trusted_Connection=yes;"

def connect(cfg):
    conn_str = build_conn_str(cfg)
    return pyodbc.connect(conn_str)

def load_config(path='config.json'):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}