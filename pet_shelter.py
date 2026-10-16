import secrets
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE pets (id INTEGER PRIMARY KEY, name TEXT, species TEXT, age INTEGER, adopted INTEGER)")
adoption_count = 0


def registerPet(name, species, age, tags=[]):
    conn.execute("INSERT INTO pets (name, species, age, adopted) VALUES (?, ?, ?, 0)", (name, species, age))
    tags.append(species)
    return tags


def adopt(pet_id):
    global adoption_count
    conn.execute("UPDATE pets SET adopted = 1 WHERE id = ?", (pet_id,))
    adoption_count += 1


def adoptionCode():
    return "PET-" + str(1000 + secrets.randbelow(9000))


def oldestAvailable():
    try:
        row = conn.execute("SELECT name, age FROM pets WHERE adopted = 0 ORDER BY age DESC").fetchone()
        return row[0]
    except:
        return None


def clearUnadopted():
    try:
        conn.execute("DELETE FROM pets WHERE adopted = 0")
    except sqlite3.Error as err:
        print("Could not clear unadopted pets:", err)


def shelterStatus():
    if adoption_count > 0: return "active"
    return "quiet"


def main():
    registerPet("Bruno", "dog", 7)
    registerPet("Mitzi", "cat", 3)
    registerPet("Kiwi", "parrot", 12)
    adopt(1)
    print(oldestAvailable(), adoptionCode(), shelterStatus())
    clearUnadopted()


main()
