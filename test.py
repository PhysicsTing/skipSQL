from skipsql import Db

db = Db(database='test_ai',
        host='localhost',
        user='root',
        schema_file='test_ai.txt')

print()

db.ask("What is Daniel Faviet's salary?")

db.ask("What is the average salary of Daniel Faviet's department?")

db.ask("Who has lower than average salary in the same department as Daniel Faviet?")

print()

db.close()