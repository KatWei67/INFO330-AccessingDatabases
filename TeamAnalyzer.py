import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug", "dark", "dragon", "electric", "fairy", "fight",
    "fire", "flying", "ghost", "grass", "ground", "ice", "normal",
    "poison", "psychic", "rock", "steel", "water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg" 
    pokedex_number = arg
    print("Analyzing", pokedex_number)
    
    # You will need to write the SQL, extract the results, and compare
    # Remember t o look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    
    # Connect to pokemon.sqlite
    conn = sqlite3.connect("pokemon.sqlite")
    c = conn.cursor()

    # Execute the Pokemon's types_id from the database
    c.execute("SELECT type_id FROM pokemon_type WHERE pokemon_id = ? AND which = 1", (arg,))
    type1_id = c.fetchone()[0]
    c.execute("SELECT type_id FROM pokemon_type WHERE pokemon_id = ? AND which = 2", (arg,))
    type2_result = c.fetchone()
    if type2_result is None:
        type2_id = None
    else:
        type2_id = type2_result[0]

    # Execute the Pokemon's name and type names from the database
    c.execute("SELECT name FROM pokemon WHERE id = ?", (arg,))
    pokemon_name = c.fetchone()[0]
    c.execute("SELECT name FROM type WHERE id = ?", (type1_id,))
    type1_name = c.fetchone()[0]
    if type2_id is None:
        type2_name = ""
    else:
        c.execute("SELECT name FROM type WHERE id = ?", (type2_id,))
        type2_name = c.fetchone()[0]

    # Query the database to determine the Pokemon's strengths and weaknesses
    if type2_id is None:
        c.execute("SELECT * FROM against WHERE type_source_id1 = ? AND type_source_id2 IS NULL", (type1_id,))
    else:
        c.execute("SELECT * FROM against WHERE type_source_id1 = ? AND type_source_id2 = ?", (type1_id, type2_id))
    against = c.fetchone()[2:]

    strength = []
    weakness = []
    for i, data in enumerate(against):
        if data > 1:
            strength.append(types[i])
        elif data < 1:
            weakness.append(types[i])

    # Print the results
    print(pokemon_name, "(" + type1_name + " " + type2_name + ")" + " is strong against", strength, "but weak against", weakness)

    conn.close()


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table    
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

