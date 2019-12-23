#!/usr/local/bin/python3
"""



all data of the game can be added through both json files.


"""


#import all the neccessary files
import json
import time
import gui
import character
import battle
import math
import random
import inventory

battles = 0
wins = 0
kills = 0
exps = 0
level = 1
map_level = 1
playerPosX = 1
playerPosY = 1


app = gui.simpleapp_tk(None)

def doNothing():
    return True


app.title('RPG Battle')
# generate random sentence when prevent the player to enter the higher map_level
random_sentence = ['A rock blocks your way', 
                    'Find another way to pass through this gate', 
                    'The door has been locked, maybe you need to find the key for it?', 
                    'I cannot let you enter the next map, it is too dangerous.', 
                    'Make sure to have some good equipments!']

app.write('''
 _    _      _                             _         
| |  | |    | |                           | |        
| |  | | ___| | ___  ___  _ __ ___   ___  | |_  ___  
| |/\| |/ _ \ |/ __|/ _ \| '_ ` _ \ / _ \ | __|/ _ \ 
\  /\  /  __/ | (__| (_) | | | | | |  __/ | |_| (_) |
 \/  \/ \___|_|\___|\___/|_| |_| |_|\___|  \__|\___/

____________ _____  ______       _   _   _      _ 
| ___ \ ___ \  __ \ | ___ \     | | | | | |    | |
| |_/ / |_/ / |  \/ | |_/ / __ _| |_| |_| | ___| |
|    /|  __/| | __  | ___ \/ _` | __| __| |/ _ \ |
| |\ \| |   | |_\ \ | |_/ / (_| | |_| |_| |  __/_|
\_| \_\_|    \____/ \____/ \__,_|\__|\__|_|\___(_)

''')
app.write("You can exit the game at any time by typing in 'quit'")
app.write("")

def set_mode():
    """ Select the game mode """
    # This is an error checking version of reading user input
    # This will be explained in class - pay attention!!
    # Understanding try/except cases is important for
    # verifying user input
    # handle game crashing
    try:
        app.write("Please select a side:")
        app.write("1. Good")
        app.write("2. Evil")
        app.write("")
        app.wait_variable(app.inputVariable)
        mode = app.inputVariable.get()

        if mode == 'quit':
            app.quit()

        mode = int(mode)
        if mode not in range(1, 3):
            raise ValueError # if error occurs, the game will not crash

    except ValueError:
        app.write("You must enter a valid choice")
        app.write("")
        mode = set_mode()

    return mode

def show_stats():
    """Display stats of the character"""
    app.showinfo("Player name: " + player.name + " \n Max health: " + str(player.max_health) + " \n Max mana: " + str(player.max_mana) + " \n ATK: " + str(player.attack) + " \n MATK: " + str(player.magic) + "\n DEF: " + str(player.defense) + "\n EVA: " + str(player.evasion))
    return menu()


def set_race(mode):
    """ Set the player's race """
    if mode == 2:  # Evil Mode
        app.write("Coming soon")
        time.sleep(2)
        return set_mode()
        """
        app.write("Playing as the Forces of Sauron.")
        app.write("")

        # race selection - evil
        try:
            app.write("Please select your race:")
            app.write("1. Goblin")
            app.write("2. Orc")
            app.write("3. Uruk")
            app.write("4. Wizard")
            app.write("")
            app.wait_variable(app.inputVariable)
            race = app.inputVariable.get()

            if race == 'quit':
                app.quit()

            race = int(race)
            if race not in range(1, 5):
                raise ValueError

        except ValueError:
            app.write("You must enter a valid choice")
            app.write("")
            race = set_race(mode)"""

    else:  # Good Mode
        app.write("Playing as the Free Peoples of Middle Earth.")
        app.write("")

        # race selection - good
        try:
            app.write("Please select your race:")
            #app.write("1. Elf")
            #app.write("2. Dwarf")
            app.write("1. Human")
            #app.write("4. Hobbit")
            app.write("2. Wizard")
            app.write("3. Warrior")
            app.write("")
            app.wait_variable(app.inputVariable)
            race = app.inputVariable.get()

            if race == 'quit':
                app.quit()
            race = int(race)

            if race not in range(1, 4):
                raise ValueError

        except ValueError:
            app.write("You must enter a valid choice")
            app.write("")
            race = set_race(mode)

    return race


def set_name():
    """ Set the player's name """
    try:
        app.write("Please enter your Character Name:")
        app.write("")
        app.wait_variable(app.inputVariable)
        char_name = app.inputVariable.get()

        if char_name == 'quit':
            app.quit()

        if char_name == '':
            raise ValueError

    except ValueError:
        app.write("")
        app.write("Your name cannot be blank")
        char_name = set_name()

    return char_name


def create_player(mode, race, char_name):
    """ Create the player's character """
    # Evil
    if mode == 2:
        if race == 1:
            player = character.Goblin(char_name, 1, app)
        elif race == 2:
            player = character.Orc(char_name, 1, app)
        elif race == 3:
            player = character.Uruk(char_name, 1, app)
        else:
            player = character.Wizard(char_name, 1, app)
    # Good
    else:
        if race == 1:
            player = character.Human(char_name, 1, app)
        elif race == 2:
            player = character.Wizard(char_name, 1, app)
        elif race == 3:
            player = character.Warrior(char_name, 1, app)
        """elif race == 4:
            player = character.Hobbit(char_name, 1,  app)
        elif race == 6:
            player = character.Bishop(char_name, 1, app)
        else:
            player = character.Wizard(char_name, 1, app)"""
    return player

def getinventory():
    """Return items in player's bag"""
    bag.viewInventory(player, app)
    app.write("")
    return menu()

def buy(item): 
    "Buy item from shop"
    #this looks ugly.    
    # load data.json file
    # find the map_level and display the available item to buy from that location         
    with open('data.json', 'r') as f:
            data = json.load(f)
            for i in data['shop']:
                if i['map'] == map_level:
                    itemname = i['item'][item]
                    for j in data['collectibles']:
                        if j['name'] == itemname:
                            price = j['price']
                            if player.coin > price and len(bag.bag) < 300:
                                player.coin = player.coin - price
                                bag.inputItem(itemname, app)
                                app.write("Purchased item: " + itemname)
                            else:
                                app.write("Looks like you don't have enough coin to perform this action or your bag might be full")
                                app.write("Please come again later")
                                app.write("")
                                time.sleep(1)

    """
    if item == 1:
        with open('data.json', 'r') as f:
            data = json.load(f)
            for i in data['collectibles']:
                if i['name'] == 'Potions':
                    price = i['price']
            if player.coin > price and len(bag.bag) < 300:
                player.coin = player.coin - price
                bag.inputItem("Potions", app)
                app.write("Purchased item: Potions")
            else:
                app.write("Looks like you don't have enough coin to perform this action or your bag might be full")
                app.write("Please come again later")
                app.write("")
                time.sleep()"""
    return shop()

def buy_menu():
    """Buying items here"""
    global map_level
    try:
        j = 0
        #open data.json file, find the map_level and return the available items from that map
        with open('data.json', 'r') as f:
            data = json.load(f)
            for i in data['shop']:
                if i['map'] == map_level:
                    while j < len(i['item']):
                        app.write(str(j) + ". " + i['item'][j])
                        j += 1
                else:
                    app.write("We have nothing to sell, please come back later")
                    app.write("")
                    return menu()
                        
        app.write("")
        app.wait_variable(app.inputVariable)
        options = app.inputVariable.get()

        if options == 'quit':
            app.quit()
        options = int(options)

        if options not in range(0, 5) or options == "":
            raise ValueError
    except ValueError:
        app.write("Invalid value")
        app.write()
    return buy(options)

def purchase_skill(choice):
    """Check if the player meets the requirement to buy skills"""
    app.write("Coming soon")

def buy_skill_menu():
    """Buy skills, only if the character meet the requirements"""
    try:
        app.write("Please select skill you would like to buy")
        app.write("0. Nemesis 2")
        app.write("")
        app.wait_variable(app.inputVariable)
        choice = app.inputVariable.get()

        if options == "quit":
            app.quit()
        choice = int(choice)
    except:
        app.write("Please enter a valid value")
        app.write("")
        buy_skill_menu()
    return purchase_skill(choice)

def show_shop_menu(option):
    """Accept player input return function"""
    if option == 1:
        buy_menu()
    elif option == 2:
        sell_menu()
    elif option == 3:
        buy_skill_menu()

def sell_menu():
    """Sell item menu"""
    #load data.json file
    # find the item name then find the price
    with open("data.json", "r") as f:
        data = json.load(f)
        j = 0
        if len(bag.bag) == 0:
            app.write("You have no item to sell...")
            app.write("Please come back later")
            app.write("")
            time.sleep(1)
        while j < len(bag.bag):
            if len(bag.bag) > 0:
                app.write(str(j) + ". " + bag.bag[j])
            j += 1
        app.wait_variable(app.inputVariable)
        item = app.inputVariable.get()
        if item == "quit":
            app.quit()

        item = int(item)
        itemname = bag.bag[item]
        for i in data['collectibles']:
            if i['name'] == itemname:
                price = i['price']
        bag.bag.remove(itemname)
        player.coin += price
        app.write(" You have sold item: " + itemname)
        app.write(" You have recieved: " + str(price) + " coins")
        app.write(" Total coins available: " + str(player.coin) + " coins")
        time.sleep(1)
        app.write("Thank you, please come back later")
        app.write("")
        time.sleep(1)
        
            

    return menu()


def shop():
    """Shop menu"""
    try:
        app.write("Please select an action you want to do")
        app.write('1. Buy')
        app.write('2. Sell')
        app.write('3. I need skills')
        app.write("")
        app.wait_variable(app.inputVariable)
        options = app.inputVariable.get()

        if options == 'quit':
            app.quit()
        options = int(options)
        if options not in range(0, 5) or options == "":
            raise ValueError
    except ValueError:
        app.write("Invalid value")
        shop()
    return show_shop_menu(options)


def set_movement():
    """Player movement menu"""
    try:
        app.write('Please select what to want to do')
        app.write('W. West')
        app.write('E. East')
        app.write('N. North')
        app.write('S. South')
        app.write('B. Go back')
        app.write("")
        app.wait_variable(app.inputVariable)
        options = app.inputVariable.get()
        options.lower()
        if options == "quit":
            app.quit()
        if options not in ['w', 's', 'e', 'n', 'b'] or options == "":
            raise ValueError
    except ValueError:
        app.write("Please enter a valid value")
        app.write("")
        options = set_movement()
    return set_player_movement(options)

def file_save():
    """Save gameplay data"""
    #write gameplay data to text file.
    file = app.save_file()
    if file is None:
        return
    try:
        file.write("Level: " + str(player.level) + " \n" + "Name: " + str(player.name) + " \n" + "Job: " + str(player.__class__.__name__) + " \n" + "Battles: " + str(battles) + " \n" + "Items: " + str(bag.bag) + " \n" + "Exp: " + str(player.exp))
        file.close()
    except:
        app.showinfo("An error has occurs, this maybe because you have not finish creating your character")

def file_load():
    """Load selected file"""
    # load the file from the folder and create the player. 
    file = app.load_file()
    try:
        with open(file, 'r') as f:
            dict = {}
            for line in f.readlines():
                key, value = line.rstrip("\n").split(":")
                dict[key] = value
            global player
            global bag
            global battles
            global char_name
            battles = int(dict['Battles'])
            char_name = dict['Name'].rstrip()
            if dict['Job'] == " Bishop ":
            #print('True')
                player = character.Bishop(dict['Name'], int(dict['Level']), app)
                player.exp = int(dict['Exp'])
                app.write("You are now playing as " + player.name)
                return menu()
            elif dict['Job'] == " Wizard ":
                player = character.Wizard(dict['Name'], int(dict['Level']), app)
                app.write("You are now playing as " + player.name)
                player.exp = int(dict['Exp'])
                return menu()
            elif dict['Job'] == " Warrior ":
                player = character.Warrior(dict['Name'], int(dict['Level']), app)
                app.write("You are now playing as " + player.name)
                player.exp = int(dict['Exp'])
            elif dict['Job'] == " Paladin ":
                player = character.Paladin(dict['Name'].rstrip(), int(dict['Level']), app)
                app.write("You are now playing as " + player.name)
                player.exp = int(dict['Exp'])
            elif dict['Job'] == " Human ":
                player = character.Human(dict['Name'].rstrip(), int(dict['Level']), app)
                app.write("You are now playing as " + player.name)
                player.exp = int(dict['Exp'])
        return menu()

    except:
        app.write("File cannot be loaded, please try again")

def display_map_name():
    """display map name"""
    # open map.json to find the map's name that matches map_level
    global map_level
    with open('map.json', 'r') as f:
        data = json.load(f)
        for i in data[str(map_level)]:
            app.write(i["name"])
            app.write("")

def goLeft(posX, posY, map):
    """Move left"""
    # move the player to the left
    # idecrease the x coordinate by 1
    # update the map, repeat for other directions
    global playerPosX
    global map_level
    global playerPosY
    if map[posY][posX - 1] == 0:
        app.write('You can\'t go that way.')
        for i in map:
            app.write(i)
        return set_movement()
    elif map[posY][posX - 1] == 3:
        map_level += 1
        playerPosX = 1
        playerPosY = 1
        display_map_name()
        return set_movement()
    elif map[posY][posX - 1] == 4:
        map_level -= 1
        playerPosX = 1
        playerPosY = 1
        display_map_name()
        return set_movement()
    else:
        map[posY][posX] = 1
        posX -= 1
        map[posY][posX] = 2
        for i in map:
            app.write(i)
        app.write("")
        playerPosX = posX
        rate = random.randint(1, 10)
        #the enemies are spawn randomly on the map
        app.write("You moved 1 step")
        if rate <= 7:
            app.write("Looks like there is nothing here")
            return set_movement()
        elif rate >= 8:
            app.write("Something blocks your way....")
            with open('map.json', 'r') as f:
                data = json.load(f)
                for i in data[str(map_level)]:
                    mobs1 = i['common']
                    mobs2 = i['uncommon']
                chance = [mobs1, mobs1, mobs1, mobs1, mobs2, mobs2]
                rate = random.sample(chance, 2)
                #levelChance = random.randint(1, 5)
                enemies = character.Mobs(rate[0], map_level + random.randint(1, 5), app ), character.Mobs(rate[1], map_level + random.randint(1, 5), app)
                start_battle(enemies)
                return posX
        else:
            return set_movement()

    return posX

def goRight(posX, posY, map):
    """Move right"""
    global playerPosX
    global map_level
    global playerPosY
    if map[posY][posX + 1] == 0:
        app.write('You can\'t go that way')
        for i in map:
            app.write(i)
        app.write("")
        return set_movement()
    elif map[posY][posX + 1] == 3:
        map_level += 1
        playerPosX = 1
        playerPosY = 1
        display_map_name()
        return set_movement()
    elif map[posY][posX + 1] == 4:
        map_level -= 1
        playerPosX = 1
        playerPosY = 1
        display_map_name()
        return set_movement()
    else:
        map[posY][posX] = 1
        posX += 1 
        map[posY][posX] = 2
        for i in map:
          app.write(i)
        playerPosX = posX
        rate = random.randint(1, 10)
        app.write("You moved 1 step")
        if rate <= 6:
            app.write("Looks like there is nothing here")
            return set_movement()
        elif rate >= 7:
            app.write("Something blocks your way....")
            with open('map.json', 'r') as f:
                data = json.load(f)
                for i in data[str(map_level)]:
                    mobs1 = i['common']
                    mobs2 = i['uncommon']
                chance = [mobs1, mobs1, mobs1, mobs1, mobs2, mobs2]
                rate = random.sample(chance, 2)
                #levelChance = random.randint(1, 5)
                enemies = character.Mobs(rate[0], map_level + random.randint(1, 5), app ), character.Mobs(rate[1], map_level + random.randint(1, 5), app)
                start_battle(enemies)
                return posX
        else:
            return set_movement()
        
    return posX

def goDown(posX, posY, map):
    """Move the player down"""
    global playerPosY
    global playerPosX
    global map_level
    if map[posY + 1][posX] == 0:
        app.write('You can\'t go that way.')
        for i in map:
            app.write(i)
    elif map[posY + 1][posX] == 3:
        map_level += 1
        playerPosX = 1
        playerPosY = 1
        display_map_name()
        return set_movement()
    elif map[posY + 1][posX] == 4:
        map_level -= 1
        playerPosX = 1
        playerPosY = 1
        display_map_name()
        return set_movement()
    else:
        map[posY][posX] = 1
        posY += 1
        map[posY][posX] = 2
        for i in map:
          app.write(i)
        playerPosY = posY
        rate = random.randint(1, 10)
        app.write("You moved 1 step")
        if rate <= 6:
            app.write("Looks like there is nothing here")
            return set_movement()
        elif rate >= 7:
            app.write("Something blocks your way....")
            with open('map.json', 'r') as f:
                data = json.load(f)
                for i in data[str(map_level)]:
                    mobs1 = i['common']
                    mobs2 = i['uncommon']
                chance = [mobs1, mobs1, mobs1, mobs1, mobs2, mobs2]
                rate = random.sample(chance, 2)
                #levelChance = random.randint(1, 5)
                enemies = character.Mobs(rate[0], map_level + random.randint(1, 5), app ), character.Mobs(rate[1], map_level + random.randint(1, 5), app)
                start_battle(enemies)
                return posY
        else:
            return set_movement()
        
    return posY
def goUp(posX, posY, map):
    """Move the player up"""
    global playerPosY
    global map_level
    global playerPosX
    if map[posY - 1][posX] == 0:
        app.write('You can\'t go that way')
        for i in map:
            print(i)
    elif map[posY - 1][posX] == 3:
        map_level += 1
        playerPosX = 1
        playerPosY = 1
        display_map_name()
        return set_movement()
    elif map[posY - 1][posX] == 4:
        map_level -= 1
        playerPosX = 1
        playerPosY = 1
        display_map_name()
        return set_movement()
    else:
        map[posY][posX] = 1
        posY -= 1
        map[posY][posX] = 2
        for i in map:
          app.write(i)
        playerPosY = posY
        rate = random. randint(1, 10)
        app.write("You moved 1 step")
        if rate <= 6:
            app.write("Looks like there is nothing here")
            return set_movement()
        elif rate >= 7:
            app.write("Something blocks your way....")
            with open('map.json', 'r') as f:
                data = json.load(f)
                for i in data[str(map_level)]:
                    mobs1 = i['common']
                    mobs2 = i['uncommon']
                chance = [mobs1, mobs1, mobs1, mobs1, mobs2, mobs2]
                rate = random.sample(chance, 2)
                #levelChance = random.randint(1, 5)
                enemies = character.Mobs(rate[0], map_level + random.randint(1, 5), app ), character.Mobs(rate[1], map_level + random.randint(1, 5), app)
                start_battle(enemies)
                return posY
        else:
            return set_movement()
    return posY

def set_player_movement(option):
    """Move player, with the probabilty of being spotted by monsters"""
    global playerPosX
    global playerPosY
    # 0 in map represent obstacles, 1 is where the player can move and 2 is the player current location, 3 is the next location and 4 is the previous location
    # load the map's grid from data.json file      
    # in this way we can dynamically update the game without writing more code. 
    with open('data.json', 'r') as f:
        data = json.load(f)
        for i in data['map']:
            if i['mapLevel'] == map_level:
                map = i['grid']
    if option == 'w':
        playerPosX = goLeft(playerPosX, playerPosY, map)
    elif option == 'e':
        playerPosX = goRight(playerPosX, playerPosY, map)
    elif option == 'n':
        playerPosY = goUp(playerPosX, plauerPosY, map)
    elif option == 's':
        playerPosY = goDown(playerPosX, playerPosY, map)

    elif option == "b":
        return menu()

def menu():
    """Main menu for player action"""
    try:
        app.write('Please select action you want to do')
        app.write('1. View player info')
        app.write('2. Move')
        app.write('3. Fight')
        app.write('4. Shop ')
        app.write('5. Change Profession')
        app.write('6. View your inventory')
        app.write('7. View stats')
        app.write('8. Move to the next map')
        app.write('9. Move to the previous map')
        app.write('10. Quest ')
        app.write("")
        app.wait_variable(app.inputVariable)
        options = app.inputVariable.get()
        

        if options == "quit":
            app.quit()
        options = int(options)
        if options not in range(0, 11) or options == '':
            raise ValueError
    except ValueError:
        app.write('You must enter a valid value')
        app.write("")
        options = menu()
    return options

def changeJob(value):
    """Player can change their job to a higher tier if they meet certain requirements"""
    global player
    if value == 1:
        new_value = value
        if player.level < 20:
            app.write("Requirement: lvl 20")
            app.write("Look like you have not met this requirement yet \n Come back later")
            app.write("")
        else:
            try:
                app.write("You will lose all the current skills, continue to change?")
                app.write("0. Make me a Bishop")
                app.write("1. Let me think again")
                app.write("")
                app.wait_variable(app.inputVariable)
                choice = app.inputVariable.get()
                if choice == 'quit':
                    app.quit()
                choice = int(choice)
                if choice not in range(2) or choice == '':
                    raise ValueError
                player = character.Bishop(char_name, player.level, app)
                app.write("You have learnt new skills")
                app.write("")
            except ValueError:
                app.write("Please input a valid value")
                app.write("")
                changeJob(new_value)   
    if value == 2:
        new_value = value
        if player.level < 20:
            app.write("Requirement: lvl 20")
            app.write("Look like you have not met this requirement yet \n Come back later")
            app.write("")
        else:
            try:
                app.write("You will lose all the current skills, continue to change?")
                app.write("0. Make me a Paladin")
                app.write("1. Let me think again")
                app.write("")
                app.wait_variable(app.inputVariable)
                choice = app.inputVariable.get()
                if choice == 'quit':
                    app.quit()
                choice = int(choice)
                if choice not in range(2) or choice == '':
                    raise ValueError
                player = character.Paladin(char_name, player.level, app)
                app.write("You have learnt new skills")
                app.write("")
            except ValueError:
                app.write("Please input a valid value")
                app.write("")
                changeJob(new_value)      
    return player
    
def menuJob():
    """Menu for job selection"""
    try:
        app.write("Please select class you want to become")
        app.write("1. Bishop")
        app.write("2. Paladin")
        app.write("")
        app.wait_variable(app.inputVariable)
        options = app.inputVariable.get()
        if options == "quit":
            app.quit()
        options = int(options)
        if options not in range(0, 4) or options == '':
            raise ValueError
    except ValueError:
        app.write('You must enter a valid value')
        app.write("")
        menuJob()
    return changeJob(options)

def questName(choice):
    """Player can get exp and coins by completing the quests"""
    if choice == 0:
        newList = []
        for i in bag.bag:
           if i  == "Black fragment":
               newList.append(i)
        if len(newList) < 10:
            app.write("Sorry, I cannot give you the rewards, you need to collect 10 black fragments")
            app.write("")
        else:
            app.write("Here is your rewards")
            app.write("")
            for i in range(10):
                bag.bag.remove('Black fragment')
            player.coin += 3000
            player.exp += 250
            level_up_notice()
            app.write("You recieved 2500 coins")
            app.write("You recieved 310 experiences")
            app.write("Total coin: " + str(player.coin))
            app.write("")
            return menu()

    if choice == 1:
        newList = []
        for i in bag.bag:
            if i == "Flower nectar":
                newList.append(i)
        if len(newList) < 10:
            app.write("Sorry, I cannot give you the rewards, you need to collect 10 Flower nectar")
        else:
            app.write("Here is your rewards")
            for i in range(10):
                bag.bag.remove("Flower nectar")
            player.coin += 2500
            player.exp += 310
            level_up_notice()
            app.write("You recieved 2500 coins")
            app.write("You recieved 310 experiences")
            app.write("Total coin: " + str(player.coin))
            app.write("")
            return menu()
    else:
        app.write("Coming soon")
        app.write("")
        return menu()

def level_up_notice():
    """Notice when player level up"""
    global level
    currentLevel = math.floor(0.1 * math.sqrt(player.exp))
    if currentLevel > level:
        player.level += 1
        level += 1
        app.write("You have leveled up, your level now is " + str(player.level))

def select(type, name, optional):
    """Select data from data.json file"""
    with open('data.json', 'r') as f:
        data = json.load(f)
        for i in data[type]:
           if i == data[name]:
               return data[optional]


def quest_guide():
    """Take the quest"""
    try:
        app.write("Please select the quest you would like to do, rewards will be given")
        app.write("0. Black fragment x 10")
        app.write("1. Flower nectar x 10")
        app.write("2. Green leaf x 10")
        app.write("")
        app.wait_variable(app.inputVariable)
        choice = app.inputVariable.get()
        if choice == "quit":
            app.quit()
        choice = int(choice)
        if choice not in range(0, 3) or choice == "":
            raise ValueError
    except ValueError:
        app.write("You must enter a valid value")
        app.write("")
        quest_guide()
    return questName(choice)


def choose_menu(option):
    """Menu to choose"""
    if option == 1:
        app.showinfo("You are " + player.name +"\n Your level: " + str(player.level) + " \n Experiences: " + str(player.exp) + "\n Battle: " + str(battles) + " \n Wins: " + str(wins) + " \n Coins: " + str(player.coin) + " \n Job: " + str(player.__class__.__name__))
        time.sleep(1)
        return menu()
    elif option == 2:
        set_movement()
    elif option == 3:
        return game()
    elif option == 4:
        return shop()
    elif option == 5:
        return menuJob()
    elif option == 6:
        return getinventory()
    elif option == 7:
        return show_stats()
    elif option == 8 or option == 9:
        return move_map()
    elif option == 10:
        return quest_guide()

def move_map():
    """Move player to the new map"""
    #check if the player level equal to the map level.
    global map_level
    global random_sentence
    newMap = map_level + 1
    if newMap <= player.level:
        map_level += 1
        app.write("Moved to the new map")
        app.write("")
    else:
        time.sleep(1)
        #generate random sentence
        app.write(random_sentence[math.floor(random.random() * len(random_sentence))])
        time.sleep(2)
        app.write("")

def set_difficulty():
    """ Set the difficulty of the game """
    try:
        app.write("Please select a difficulty level:")
        app.write("e - Easy")
        app.write("m - Medium")
        app.write("h - Hard")
        app.write("l - Legendary")
        app.write("s - Supreme")
        app.write("b - Go back")
        app.write("")
        app.wait_variable(app.inputVariable)
        difficulty = app.inputVariable.get()

        if difficulty == 'quit':
            app.quit()

        if difficulty not in ['e', 'm', 'h', 'l', 's', 'b'] or difficulty == '':
            raise ValueError

    except ValueError:
        app.write("You must enter a valid choice")
        app.write("")
        difficulty = set_difficulty()

    return difficulty

def read_map_level():
    """open map.json file to read data"""
    with open('map.json', 'r') as f:
                data = json.load(f)
                for i in data[str(map_level)]:
                    mobs1 = i['common']
                    mobs2 = i['uncommon']
                    mobs3 = i['rare']
                    mobs4 = i['boss']
                    return mobs1, mobs2, mobs3, mobs4

def create_enemies(mode, difficulty):
    """ Create the enemies """
    #Whaterver side player is choosing, they still end up facing the same types of monsters
    global map_level
    if mode == 2:  # Evil Mode - good enemies
        if difficulty == 'm':
            enemies = [character.Hobbit("Peregrin", 1, app), character.Hobbit("Meriadoc", 1, app),
                       character.Human("Eowyn", 1,  app)]
        elif difficulty == 'h':
            enemies = [character.Dwarf("Gimli", 1, app), character.Elf("Legolas", 1, app), character.Human("Boromir", 1, app)]
        elif difficulty == 'l':
            enemies = [character.Human("Sianas", 1, app), character.Human("Altern", 1,  app),
                       character.Wizard("Niapa", 1, app)]
        elif difficulty == "b":
            return menu()
        else:
            enemies = [character.Hobbit("Frodo",  1, app), character.Hobbit("Sam", 1, app)]

    else:  # Good Mode - evil enemies
        common, uncommon, rare, boss = read_map_level()
        if difficulty == 'm':
            enemies = [character.Mobs(common, map_level + random.randint(0, 5), app), character.Mobs(common, map_level + random.randint(0, 5), app), character.Mobs(uncommon, 1, app)]
        elif difficulty == 'h':
            enemies = [character.Mobs(uncommon, map_level + random.randint(1, 6), app), character.Mobs(uncommon, map_level + map_level + random.randint(1, 6), app), character.Mobs(uncommon, map_level + map_level + random.randint(0, 4), app)]
        elif difficulty == 'l':
            enemies = [character.Mega(rare, map_level + map_level + random.randint(0, 5), app), character.Mega(rare, map_level + random.randint(0, 5), app), character.Mega(rare, map_level + map_level + random.randint(0, 4) , app)]
        elif difficulty == 's':
            enemies = [character.Dragon(boss, map_level + 1, app), character.Dragon(boss, map_level + 1,  app)]
        elif difficulty == 'b':
            return menu()
        else:
            enemies = [character.Mobs(common, map_level,  app), character.Mobs(common, map_level, app)]

    return enemies

def generate_dragon_name():
    name = random.choice(['Leviam', 'Eisen', 'Kaiser', 'Kagan', 'Blazaird'])
    return name

def quit_game():
    """ Quits the game """
    try:
        app.write("Play Again? (y/n)")
        app.write("")
        app.wait_variable(app.inputVariable)
        quit_choice = app.inputVariable.get()

        if quit_choice == 'quit':
            app.quit()

        if quit_choice not in 'yn' or quit_choice == '':
            raise ValueError


    except ValueError:
        app.write("You must enter a valid choice")
        app.write("")
        quit_choice = quit_game()

    return quit_choice

def start_battle(enemies):
    """Start battle, the player cannot """
    encounter = battle.Battle(player, enemies, bag, app)
    battle_wins, battle_kills, battle_exps = encounter.play()
    global battles
    global wins
    global kills
    global exps
    global level
    global currentLevel
    battles += 1
    wins += battle_wins
    kills += battle_kills
    exps += battle_exps
    #print(battle_exps)
    player.exp += battle_exps
    #print(player.exp)
    print(player.exp)
    currentLevel = math.floor(0.1 * math.sqrt(player.exp))
    if level < currentLevel:
        level += currentLevel
        app.write('Congratulation, you have leveled up to level ' + str(level))
        player.level += 1
    print_results()
    player.reset()
    for enemy in enemies:
        enemy.reset()
    return set_movement()

def print_results():
    """Print the result of the game"""
    app.write("Game Over!")
    app.write("No. Battles: {0}".format(str(battles)))
    app.write("No. Wins: {0}".format(wins))
    app.write("No. Kills: {0}".format(kills))
    app.write("Success Rate (%): {0:.2f}%".format(float(wins * 100 / battles)))
    app.write("Avg. kills per battle: {0:.2f}".format(float(kills) / battles))
    app.write("")

"""
Create menubar to save and load data gameplay, in order to prevent any problem that might occurs
it is suggested to finish creating the character first before saving or loading data gameplay
"""
menubar = app.createMenu()
filemenu = app.Menu(menubar)
filemenu.add_command(label="New", command=doNothing())
filemenu.add_command(label="Save", command=file_save)
filemenu.add_command(label="Load", command=file_load)
filemenu.add_command(label="Close", command=doNothing())
filemenu.add_separator()
menubar.add_cascade(label="File", menu=filemenu)
app.config(menu=menubar)



mode = set_mode()
race = set_race(mode)
char_name = set_name()
player = create_player(mode, race, char_name)
app.write(player)
app.write("")
#difficulty = set_difficulty()
level = 1
bag = inventory.Inventory(player, app)


def game():
    """Player might want to choose this option to level up fast"""
    difficulty = set_difficulty()
    enemies = create_enemies(mode, difficulty)
    encounter = battle.Battle(player, enemies, bag, app)
    battle_wins, battle_kills, battle_exps = encounter.play()
    global battles
    global wins
    global kills
    global exps
    global level
    global currentLevel
    battles += 1
    wins += battle_wins
    kills += battle_kills
    exps += battle_exps
    player.exp += battle_exps
    #this will return player level based on their experience points
    currentLevel = math.floor(0.1 * math.sqrt(player.exp))
    if level < currentLevel:
        level += currentLevel
        app.write('Congratulation, you have leveled up to level ' + str(level))
        player.level += 1
    print_results()

    quit = quit_game()
    
    if quit == "n":
        app.write('Are you sure you want to quit the game')
        app.write('you character data will not be saved y/n')
        app.write("")
        app.wait_variable(app.inputVariable)
        choice = app.inputVariable.get()
        if choice == 'yes' or 'y':
            app.write("Thank you for playing RPG Battle.")
            time.sleep(2)
            app.quit()
        else: 
            raise ValueError
        

    else:
        player.reset()
        for enemy in enemies:
            enemy.reset()
        return game()


while True:
    player_option = menu()
    choose_menu(player_option)

        # Playing again - reset all enemies and players



