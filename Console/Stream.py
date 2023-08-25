import sqlite3
from Character import Character
nhl_abbreviations = ["ANA", "ARI", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL",
                     "NAS", "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SJS", "STL", "TBL", "TOR", "VAN", "VGK", "WPG", "WSH"]
    
ahl_abbreviations = ['BAK', 'BEL', 'BNG', 'BRI', 'CHA', 'CHI', 'CLE', 'COL', 'GR', 'HER', 'HFD', 'IA', 'LAV', 'LV', 'MB', 'MIL',
                        'ONT', 'PRO', 'RFD', 'ROC', 'SA', 'SD', 'SJ', 'SPR', 'STK', 'SYR', 'TEX', 'TOR', 'TUC', 'UTI', 'WBS']

ohl_abbreviations = ['BAR', 'ER', 'FLNT', 'GUE', 'HAM', 'KGN', 'KIT', 'LDN', 'MISS', 'NB', 'NIAG', 'OS', 'OSH', 'OTT', 'PBO', 'SAG', 'SAR', 'SBY', 'SOO', 'WSR']

whl_abbreviations = ['BDN', 'CGY', 'EDM', 'EVT', 'KAM', 'KEL', 'LET', 'MH', 'MJ', 'PA', 'PG', 'POR', 'RD', 'REG', 'SAS', 'SC', 'SEA', 'SPO', 'TC', 'VAN', 'VIC', 'WPG']

qmjhl_abbreviations = ['BAC', 'BAT', 'BLB', 'CAP', 'CHA', 'CHI', 'DRU', 'GAT', 'HAL', 'MON', 'QUE', 'RIM', 'ROU', 'SHA', 'SHE', 'SNB', 'VDO', 'VIC']

all_abbreviations = nhl_abbreviations + ahl_abbreviations + ohl_abbreviations + whl_abbreviations + qmjhl_abbreviations
abbreviations = {"NHL": nhl_abbreviations, "AHL": ahl_abbreviations, "OHL": ohl_abbreviations, "WHL": whl_abbreviations, "QMJHL": qmjhl_abbreviations, "MEM": all_abbreviations}


def update():
    db = sqlite3.connect("Sbeve.db")
    cur = db.cursor()
    file = open("Display.txt", "w")
    display_line = ""

    # career(saves,shots,svpct,season,tot_games,num_wins,num_loss,num_otl,winpct,pu)
    stats = cur.execute("SELECT * FROM career").fetchone()
    if type(stats) == type(None):
        stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    display_line += "Saves: {}                          ".format(stats[0])
    display_line += "Shots: {}                          ".format(stats[1])
    display_line += "Save %: {:0.3f}                          ".format(stats[2])
    display_line += "Seasons: {}                          ".format([3])
    display_line += "Total Games: {}                          ".format(stats[4])
    display_line += "Record: {}/{}/{}                          ".format(stats[5], stats[6], stats[7])
    display_line += "Win %: {:.3f}                          ".format(stats[8])
    display_line += "Pushups: {}                          ".format(stats[9])
    display_line += "GOAL: Save % >= 0.880, Win % >= 0.5.                          "
    display_line += "Each goal is 2 pushups, a loss is an extra 5, and every follow is an extra 5.                          "
    prev_game = cur.execute(
        "SELECT result, shots, saves, pushups, opp_team FROM games WHERE id = (SELECT MAX(id) FROM games)").fetchone()
    display_line += "Last Game: {} against {}, {} shots, {} saves, {:.3f} SV%, {} pushups                     ".format(
        prev_game[0], prev_game[4], prev_game[1], prev_game[2], (float(prev_game[2]) / float(prev_game[1])), prev_game[3])

    file = open("Display.txt", "w")
    file.write(display_line)
    file.close()

def change_team(mode, db):
    cur = db.cursor()
    while True:
        league = input("Enter league, or MEM for memorial cup: ").upper()
        if not league in ["NHL", "AHL", "OHL", "QMJHL", "WHL", "MEM"]:
            input("League is invalid, please try again.")
            continue
        team = input("Enter the new team initials: ").upper().strip()
        if team in all_abbreviations:
            if mode == "add":
                cur.execute("INSERT INTO data VALUES (?, ?, ?, ?)", (league, team, ))
            elif mode == "change":
                cur.execute("UPDATE data SET league = ?, team = ? ", (league, team))
            break
        else:
            input("Invalid team name, please try again.")

    db.commit()
    return [league, team]

def add_game(db, character, curr_team, season, league):
    cur = db.cursor()
    print("Input exit to exit.")
    
    #result
    while True:
        print("WIN/LOSS/OTL")
        choice = input("Enter result of game: ").upper()
        if choice in ["WIN", "LOSS", "OTL"]:
            result = choice
            break
        elif choice == "EXIT":
            break
        else:
            input("Invalid, please try again.")

    
    #shots
    while True:
        try:
            choice = input("Enter shots faced: ")
            if choice == "EXIT":
                break
            shots = int(choice)
            break
        except:
            input("Error, try again.")
            continue
    
    #saves
    while True:
        try:
            choice = input("Enter saves made: ")
            if choice == "EXIT":
                break
            saves = int(choice)
            break
        except:
            input("Error, try again.")
            continue
    
    #opp_team
    while True:
        choice = input("Enter opposing team: ").upper()
        if choice in abbreviations[league]:
            opp_team = choice
            break
        elif choice == "EXIT":
            break
        else:
            input("Invalid, please try again.")
    
    
    #Pushups
    while True:
        try:
            choice = input("Enter pushups done: ")
            if choice == "EXIT":
                break
            pushups = int(choice)
            break
        except:
            input("Error, try again.")
            continue

    #Confirming everything
    good = False
    while True:
        print("______________________________________________________________________________")
        print("Result: {}\nSaves: {}\nShots: {}\nOpposing team: {}\nCurrent Team: {}\nPushups: {}".format(result, saves, shots, opp_team, curr_team, pushups))
        choice = input("Is this correct? Y/N: ").upper().strip()
        if choice == "Y":
            #insert
            max_id = cur.execute("SELECT MAX(id) FROM games").fetchone()
            if max_id[0] is None:
                max_id = 0
            else:
                max_id = max_id[0]

            cur.execute("INSERT INTO games VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (max_id+1, character.get_name(), season, result, shots, saves, league, opp_team, curr_team, pushups))
            db.commit()
            input("Success! Press enter to continue.")
            good = True
            update()
            break
        elif choice == "N":
            break
        else:
            input("Invalid input. Please try again.")

def add_character(db):
    cur = db.cursor()
    while True:
        name = input("Enter name: ")
        if name == "EXIT":
            break
        position = input("Enter position: ")
        if position == "EXIT":
            break
        number = int(input("Enter number: "))
        if number == "EXIT":
            break
        elif number > 99 or number < 1:
            input("Invalid number, please try again.")
            continue
        done = input("Is this correct? Y/N: ").upper().strip()
        if (done == "Y"):
            cur.execute("INSERT INTO characters VALUES (?, ?, ?)", (name, position, number))
            db.commit()
            break
        elif (done == "N"):
            continue
        elif (done == "EXIT"):
            break
        else:
            input("Invalid input, please try again.")
            continue

def choose_character(db):
    print("Welcome! Choose your character, or type 'new' to create a new one. Type 'exit' to exit.")
    cur = db.cursor()
    while True:
        characters = cur.execute("SELECT * FROM characters").fetchall()
        for i in range(len(characters)):
            print("{}: {}".format(i+1, characters[i][0]))
        choice = input("Enter your choice: ").upper().strip()
        if choice == "EXIT":
            exit()
        elif choice == "NEW":
            add_character(db)
            continue   
        
        choice = int(choice)
        if choice > len(characters) or choice < 1:
            input("Invalid choice, please try again.")
            continue
        else:
            chara = cur.execute("SELECT * FROM characters WHERE name = ?", (characters[i][0],)).fetchone()
            return Character(chara[0], chara[1], chara[2])

    




def nhl(db, character):
    
    cur = db.cursor()
    try:
        update()
    except:
        pass
    
    while True:
        print (character)

        data = cur.execute("SELECT * FROM data WHERE character = ?", (character.get_name(),)).fetchone()
        print(data)
        if type(data) == type(None):
            print("No data found, please enter your starting team and league.")
            new_data = change_team("add", db)
            curr_team = new_data[1]
            league = new_data[0]
            season = 1
        else:
            league = data[0]
            curr_team = data[1]
            print(curr_team)
            season = data[2]
        print("_________________________________________")
        prev_game = cur.execute("SELECT result, shots, saves, pushups, opp_team FROM games WHERE id = (SELECT MAX(id) FROM games)").fetchone()
        try:
            print("Last Game: {} against {}, {} shots, {} saves, {:.3f} SV%, {} pushups".format(prev_game[0], prev_game[4], prev_game[1], prev_game[2], (float(prev_game[2]) / float(prev_game[1])), prev_game[3]))
        except:
            print("Last game: N/A")
        choice = input("Press enter to add new game, input 1 to update banner, input 2 to change team, or exit to return to game menu: ")
        if choice.lower().strip() == "exit":
            break
        elif choice.strip() == "1":
            update()
        elif choice.strip() == "2":
            change_team("change", db)
        else:
            add_game(db, character, curr_team, season, league)
            


if __name__ == "__main__":
    db = sqlite3.connect("Sbeve.db")
    while True:
        character = choose_character(db)
        nhl(db, character)
    