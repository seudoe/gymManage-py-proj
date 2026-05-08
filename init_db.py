import sqlite3
from passlib.hash import sha256_crypt

# Connect to database (creates if doesn't exist)
conn = sqlite3.connect('gym.db')
cursor = conn.cursor()

# Drop tables if they exist
cursor.execute('DROP TABLE IF EXISTS progress')
cursor.execute('DROP TABLE IF EXISTS members')
cursor.execute('DROP TABLE IF EXISTS trainors')
cursor.execute('DROP TABLE IF EXISTS receps')
cursor.execute('DROP TABLE IF EXISTS plans')
cursor.execute('DROP TABLE IF EXISTS equip')
cursor.execute('DROP TABLE IF EXISTS info')

# Create tables
cursor.execute('''
CREATE TABLE info(
    username TEXT PRIMARY KEY,
    password TEXT,
    name TEXT,
    prof INTEGER,
    street TEXT,
    city TEXT,
    phone TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE plans(
    name TEXT,
    exercise TEXT,
    sets INTEGER,
    reps INTEGER,
    PRIMARY KEY(name, exercise)
)
''')

cursor.execute('''
CREATE TABLE receps(
    username TEXT PRIMARY KEY,
    FOREIGN KEY(username) REFERENCES info(username)
)
''')

cursor.execute('''
CREATE TABLE trainors(
    username TEXT PRIMARY KEY,
    FOREIGN KEY(username) REFERENCES info(username)
)
''')

cursor.execute('''
CREATE TABLE members(
    username TEXT PRIMARY KEY,
    plan TEXT,
    trainor TEXT,
    FOREIGN KEY(username) REFERENCES info(username),
    FOREIGN KEY(plan) REFERENCES plans(name),
    FOREIGN KEY(trainor) REFERENCES trainors(username)
)
''')

cursor.execute('''
CREATE TABLE progress(
    username TEXT,
    date DATE,
    daily_result TEXT,
    rate INTEGER,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(username, date),
    FOREIGN KEY(username) REFERENCES members(username)
)
''')

cursor.execute('''
CREATE TABLE equip(
    name TEXT PRIMARY KEY,
    count INTEGER
)
''')

# Insert admin user with password "Password"
hashed_password = sha256_crypt.hash('Password')
cursor.execute('''
INSERT INTO info(username, password, name, prof, street, city, phone)
VALUES(?, ?, ?, ?, ?, ?, ?)
''', ('eswar_123', hashed_password, 'Parameswar K', 1, 'Adarshnagar', 'Anantapur', '9666585361'))

# Insert sample trainer with password "Password"
cursor.execute('''
INSERT INTO info(username, password, name, prof, street, city, phone)
VALUES(?, ?, ?, ?, ?, ?, ?)
''', ('trainer_john', hashed_password, 'John Smith', 3, 'Main Street', 'Anantapur', '9876543210'))

cursor.execute('''
INSERT INTO trainors(username) VALUES(?)
''', ('trainer_john',))

# Insert sample receptionist with password "Password"
cursor.execute('''
INSERT INTO info(username, password, name, prof, street, city, phone)
VALUES(?, ?, ?, ?, ?, ?, ?)
''', ('recep_mary', hashed_password, 'Mary Johnson', 2, 'Park Avenue', 'Anantapur', '9123456789'))

cursor.execute('''
INSERT INTO receps(username) VALUES(?)
''', ('recep_mary',))

# Insert sample workout plans
sample_plans = [
    ('Beginner', 'Push-ups', 10, 3),
    ('Beginner', 'Squats', 15, 3),
    ('Beginner', 'Plank', 30, 3),
    ('Intermediate', 'Bench Press', 12, 4),
    ('Intermediate', 'Deadlift', 10, 4),
    ('Intermediate', 'Pull-ups', 8, 4),
    ('Advanced', 'Weighted Squats', 15, 5),
    ('Advanced', 'Military Press', 12, 5),
    ('Advanced', 'Barbell Rows', 12, 5),
]

for plan_name, exercise, reps, sets in sample_plans:
    cursor.execute('''
    INSERT INTO plans(name, exercise, sets, reps)
    VALUES(?, ?, ?, ?)
    ''', (plan_name, exercise, sets, reps))

# Insert sample equipment
sample_equipment = [
    ('Treadmill', 5),
    ('Dumbbells', 20),
    ('Bench Press', 3),
    ('Squat Rack', 2),
    ('Pull-up Bar', 4),
]

for equip_name, count in sample_equipment:
    cursor.execute('''
    INSERT INTO equip(name, count) VALUES(?, ?)
    ''', (equip_name, count))

conn.commit()
conn.close()

print("Database initialized successfully!")
print("\nLogin Credentials:")
print("  Admin    - Username: eswar_123, Password: Password")
print("  Trainer  - Username: trainer_john, Password: Password")
print("  Receptionist - Username: recep_mary, Password: Password")
print("\nSample data added:")
print("  - Workout plans: Beginner, Intermediate, Advanced")
print("  - Equipment: Treadmill, Dumbbells, Bench Press, Squat Rack, Pull-up Bar")
print("  - 1 Trainer: John Smith")
print("  - 1 Receptionist: Mary Johnson")
