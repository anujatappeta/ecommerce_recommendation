import sqlite3

# -------------------------
# 🔹 CONNECT DATABASE
# -------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# -------------------------
# 🔹 CREATE TABLE
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    user_type TEXT NOT NULL
)
""")

conn.commit()


# -------------------------
# 🔹 CREATE USER
# -------------------------
def create_user(email, password, user_id, user_type="new"):
    try:
        cursor.execute(
            "INSERT INTO users (email, password, user_id, user_type) VALUES (?, ?, ?, ?)",
            (email, password, user_id, user_type)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


# -------------------------
# 🔹 GET USER
# -------------------------
def get_user(email):
    cursor.execute(
        "SELECT email, password, user_id, user_type FROM users WHERE email = ?",
        (email,)
    )
    return cursor.fetchone()


# -------------------------
# 🔹 GET NEXT USER ID
# -------------------------
def get_next_user_id():
    cursor.execute("SELECT MAX(user_id) FROM users")
    result = cursor.fetchone()[0]

    if result is None:
        return 100   # start from 100
    return result + 1


# -------------------------
# 🔹 UPDATE USER TYPE (IMPORTANT)
# -------------------------
def update_user_type(email, user_type):
    cursor.execute(
        "UPDATE users SET user_type = ? WHERE email = ?",
        (user_type, email)
    )
    conn.commit()