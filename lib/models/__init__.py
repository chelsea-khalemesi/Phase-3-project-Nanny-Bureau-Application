import sqlite3

CONN = sqlite3.connect('nanny_bureau.db')
CURSOR = CONN.cursor()