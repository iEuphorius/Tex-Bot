import sqlite3

conn = sqlite3.connect("game.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS characters (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    char_class TEXT,
    level INTEGER,
    credits INTEGER,
    hp INTEGER,
    maxHP INTEGER
)
""")

conn.commit()

class Character:
    def __init__(self, user_id, name, char_class, level=1, credits=1000, hp=100):
        self.user_id = user_id
        self.name = name
        self.char_class = char_class
        self.level = level
        self.credits = credits
        self.hp = hp
        self.maxHP = hp
        
def create_character(character):
    # Check if user already has a character
    cursor.execute("""
    SELECT * FROM characters WHERE user_id = ?
    """, (character.user_id,))

    if cursor.fetchone():
        return False  # already exists

    cursor.execute("""
    INSERT INTO characters (user_id, name, char_class, level, credits, hp, maxHP)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        character.user_id,
        character.name,
        character.char_class,
        character.level,
        character.credits,
        character.hp,
        character.maxHP
    ))

    conn.commit()
    return True

def get_character(user_id):
    cursor.execute("""
    SELECT * FROM characters WHERE user_id = ?
    """, (user_id,))

    row = cursor.fetchone()

    if not row:
        return None

    return {
        "user_id": row[0],
        "name": row[1],
        "class": row[2],
        "level": row[3],
        "credits": row[4],
        "hp": row[5],
        "maxHP": row[6]
    }
    
def update_credits(user_id, amount):
    cursor.execute("""
    UPDATE characters
    SET credits = ?
    WHERE user_id = ?
    """, (amount, user_id))

    conn.commit()
    
def update_hp(user_id, new_hp):
    cursor.execute("""
    UPDATE characters
    SET hp = ?
    WHERE user_id = ?
    """, (new_hp, user_id))

    conn.commit()
    
def delete_character(user_id):
    cursor.execute("""
    DELETE FROM characters
    WHERE user_id = ?
    """, (user_id,))

    conn.commit()

    return cursor.rowcount > 0

def get_character_by_user_id(user_id):
    cursor.execute("""
    SELECT * FROM characters
    WHERE user_id = ?
    """, (user_id,))

    return cursor.fetchone()

def update_character_field(user_id, field, value):
    ALLOWED_FIELDS = ["name", "char_class", "level", "credits", "hp", "maxHP"]
    if field not in ALLOWED_FIELDS:
        return False

    cursor.execute(f"""
    UPDATE characters
    SET {field} = ?
    WHERE user_id = ?
    """, (value, user_id))

    conn.commit()
    return True