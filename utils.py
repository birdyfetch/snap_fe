import os
import json
import hashlib
import requests
import re
import logging
from db_utils import get_db_connection


# Database path
DB_PATH = 'database.db'

def load_voucher_codes():
    with get_db_connection(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT code FROM vouchers WHERE used = FALSE;')
        vouchers = [row[0] for row in cursor.fetchall()]
    return vouchers

def is_voucher_valid(voucher):
    with get_db_connection(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM vouchers WHERE code = ? AND used = FALSE;', (voucher,))
        is_valid = cursor.fetchone()[0] > 0
    return is_valid

def mark_voucher_as_used(voucher):
    with get_db_connection(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE vouchers SET used = TRUE WHERE code = ?;', (voucher,))
        conn.commit()


def register_user(username, email, password):
    url = os.getenv("REGISTRATION_ENDPOINT")
    if not url:
        logging.error("API endpoint error please send an email to admin@snapvisite360.com")
        return {'status': 'error', 'message': 'Registration error please send an email to admin@snapvisite360.com'}
    data = {"username": username, "email": email, "password": password, "id_plan": 9564524654}
    try:
        response = requests.post(url, json=data, timeout=10)
        logging.info(f"API Response Status Code: {response.status_code}")
        if response.status_code == 200:
            # If the status code is 200, we consider it a success
            return {'status': 'success', 'data': response.text}  # You can change 'data' to None if you don't need the response body
        else:
            # If the status code is not 200, we consider it an error
            logging.error(f"API responded with non-200 status code: {response.status_code}")
            return {'status': 'error', 'message': 'Registration failed. Please try again later.'}
    except requests.exceptions.RequestException as err:
        logging.error(f"Request failed: {err}")
        return {'status': 'error', 'message': 'Registration failed due to a network error. Please check your connection and try again.'}

def is_email_valid(email):
    regex = (r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return re.match(regex, email) is not None