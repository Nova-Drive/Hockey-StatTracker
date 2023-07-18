import sqlite3

# Important note: This was custom made for my stream and is not intended to be used by anyone else. If you want to use it, you will need to modify it to fit your needs. 

def update():
    db = sqlite3.connect("Sbeve.db")
    cur = db.cursor()
    file = open("Display.txt", "w")
    display_line = ""

    # career(saves,shots,svpct,season,tot_games,num_wins,num_loss,num_otl,winpct,pu)
    stats = cur.execute("SELECT * FROM career").fetchone()

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

def change_team(teams, db):
    cur = db.cursor()
    while True:
        league = input("Enter league, or MEM for memorial cup: ").upper()
        if not league in ["NHL", "AHL", "OHL", "QMJHL", "WHL", "MEM"]:
            input("League is invalid, please try again.")
            continue
        team = input("Enter the new team initials: ").upper().strip()
        if team in teams:
            cur.execute("UPDATE data SET league = ?, team = ? ", (league, team))
            break
        else:
            input("Invalid team name, please try again.")

    db.commit()

def nhl():
    db = sqlite3.connect("Sbeve.db")
    cur = db.cursor()
    try:
        update()
    except:
        pass
    nhl_abbreviations = ["ANA", "ARI", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL",
                     "NAS", "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SJS", "STL", "TBL", "TOR", "VAN", "VGK", "WPG", "WSH"]
    
    ahl_abbreviations = ['BAK', 'BEL', 'BNG', 'BRI', 'CHA', 'CHI', 'CLE', 'COL', 'GR', 'HER', 'HFD', 'IA', 'LAV', 'LV', 'MB', 'MIL',
                         'ONT', 'PRO', 'RFD', 'ROC', 'SA', 'SD', 'SJ', 'SPR', 'STK', 'SYR', 'TEX', 'TOR', 'TUC', 'UTI', 'WBS']
    
    ohl_abbreviations = ['BAR', 'ER', 'FLNT', 'GUE', 'HAM', 'KGN', 'KIT', 'LDN', 'MISS', 'NB', 'NIAG', 'OS', 'OSH', 'OTT', 'PBO', 'SAG', 'SAR', 'SBY', 'SOO', 'WSR']
    
    whl_abbreviations = ['BDN', 'CGY', 'EDM', 'EVT', 'KAM', 'KEL', 'LET', 'MH', 'MJ', 'PA', 'PG', 'POR', 'RD', 'REG', 'SAS', 'SC', 'SEA', 'SPO', 'TC', 'VAN', 'VIC', 'WPG']
    
    qmjhl_abbreviations = ['BAC', 'BAT', 'BLB', 'CAP', 'CHA', 'CHI', 'DRU', 'GAT', 'HAL', 'MON', 'QUE', 'RIM', 'ROU', 'SHA', 'SHE', 'SNB', 'VDO', 'VIC']
    
    all_abbreviations = nhl_abbreviations + ahl_abbreviations + ohl_abbreviations + whl_abbreviations + qmjhl_abbreviations
    abbreviations = {"NHL": nhl_abbreviations, "AHL": ahl_abbreviations, "OHL": ohl_abbreviations, "WHL": whl_abbreviations, "QMJHL": qmjhl_abbreviations, "MEM": all_abbreviations}
    
    while True:
        data = cur.execute("SELECT * FROM data").fetchone()
        print(data)
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
            change_team(nhl_abbreviations + ohl_abbreviations + qmjhl_abbreviations + ahl_abbreviations + whl_abbreviations, db)
        else:
            print("Input exit to exit.")
            result = None
            shots = None
            saves = None
            opp_team = None 
            pushups = None
            
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
            if result == None:
                continue
            
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
            if shots == None:
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
            if saves == None:
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
            if opp_team == None:
                continue
            
            
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
            if pushups == None:
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

                    cur.execute("INSERT INTO games VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (max_id+1, season, result, shots, saves, opp_team, curr_team, pushups))
                    db.commit()
                    input("Success! Press enter to continue.")
                    good = True
                    update()
                    break
                elif choice == "N":
                    break
                else:
                    input("Invalid input. Please try again.")
            if good:
                continue
            #end


if __name__ == "__main__":
    nhl()
    