import sqlite3

def init_db(db_path='database.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vouchers (
                id INTEGER PRIMARY KEY,
                code TEXT NOT NULL UNIQUE,
                used BOOLEAN NOT NULL DEFAULT FALSE
            );
        ''')
        conn.commit()

def get_db_connection(db_path='database.db'):
    return sqlite3.connect(db_path)

def insert_voucher_codes(db_path, voucher_codes):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Prepare the insert statement
        insert_stmt = 'INSERT OR IGNORE INTO vouchers (code, used) VALUES (?, FALSE);'
        # Insert each voucher code
        for code in voucher_codes:
            cursor.execute(insert_stmt, (code,))
        conn.commit()

# You can now call init_db() and insert_voucher_codes() from elsewhere when needed