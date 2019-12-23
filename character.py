

# import required Python modules
import time
import random


######
### Define the attributes and methods available to all characters in the Character
### Superclass. All characters will be able to access these abilities.
### Note: All classes should inherit the 'object' class.
######

class Character:
    """ Defines the attributes and methods of the base Character class """

    def __init__(self, char_name, app):
        """ Parent constructor - called before child constructors """
        self.attack_mod = 1.0
        self.defense_mod = 1.0
        self.name = char_name
        self.shield = 0
        self.max_shield = 50
        self.app = app

    def __str__(self):
        """ string representation of character """
        return str("You are " + self.name + " the " + self.__class__.__name__)

    def move(self, player):
        """
        Defines any actions that will be attempted before individual
        character AI kicks in - applies to all children
        """
        move_complete = False
        if self.health < 50 and self.potions > 0:
            self.set_stance('d')
            self.use_potion()
            move_complete = True
        return move_complete

    #### Character Attacking Actions ####

    def set_stance(self, stance_choice):
        """ sets the fighting stance based on given parameter """

        if stance_choice == "a":
            self.attack_mod = 1.3 
            self.defense_mod = 0.6
            self.app.write(self.name + " chose aggressive stance.")

        elif stance_choice == "d":
            self.attack_mod = 0.6
            self.defense_mod = 1.3
            self.app.write(self.name + " chose defensive stance.")

        else:
            self.attack_mod = 1.0
            self.defense_mod = 1.0
            self.app.write(self.name + " chose balanced stance.")
        self.app.write("")

    def attack_enemy(self, target):
        ''' Attacks the targeted enemy. Accepts a Character object as the parameter (enemy
        to be targeted). Returns True if target killed, False if still alive.'''

        roll = random.randint(0, 20)
        hit = int(roll * self.attack_mod * self.attack)
        self.app.write(self.name + " attacks " + target.name + ".")
        time.sleep(1)

        crit_roll = random.randint(1, 10)
        if crit_roll == 10:
            hit = hit * 2
            self.app.write(self.name + " scores a critical hit! Double damage inflicted!!")
            time.sleep(1)
        kill = self.defend_attack(hit)
        time.sleep(1)

        if kill:
            self.app.write(self.name + " has killed " + target.name + ".")
            self.app.write("")
            time.sleep(1)
            return True
        else:
            return False

    def tempest(self, target):
        """An attack that has a probability of dealing an earthquake"""
        hit = int(self.attack * 2 - target.resistance - target.defense)
        if hit < 1:
            hit = 1
        self.app.write(self.name + "'s tempest blow!!")
        time.sleep(1)
        choice = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3])
        # earthquake occurs here
        if choice == 2: 
            hit = target.max_health * 90 / 100
        elif choice == 3:
            hit = target.max_health * 80 / 100  
        target.health = target.health - hit
        self.app.write(self.name + " dealt " + str(hit) + " damages on " + target.name )
        print(hit) #debug
        print(target.health)
        
        if target.health < 1:
            target.heatlh = 0
            self.app.write(self.name + " has killed " + target.name + ".")
            self.app.write("")
            time.sleep(1)
            return True
        else:
            self.app.write(target.name + " has " + str(target.health) + " hp left")
            return False

    def quick_attack(self, target):
        """A special atack that guarantee double hit"""
        choice = random.choice([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.5, 2.7, 2.8, 3])
        hit = int(self.attack * 2 * choice - (target.defense_mod / 100 ))
        if target.ratecut > 1:
            if hit > target.max_health:
                hit = hit - target.max_health * target.ratecut / 150     
        self.app.write(self.name + " dealt " + str(hit) + " critical damages on " + target.name )
        time.sleep(1)
        target.health = target.health - hit
        if target.health <= 0:
            self.app.write(self.name + " has killed " + target.name + ".")
            self.app.write("")
            time.sleep(1)
            return True
        else:
            self.app.write(target.name + " has " + str(target.health) + " hp left")
            return False


    def defend_attack(self, att_damage):
        ''' Defends an attack from the enemy. Accepts the "hit" score of the attacking enemy as
        a parameter. Returns True is character dies, False if still alive.'''

        # defend roll
        roll = random.randint(1, 20)
        block = int(roll * self.defense_mod * self.defense)

        # Roll for block - must roll a 10 (10% chance)
        block_roll = random.randint(1, 10)
        if block_roll == 10:
            self.app.write(self.name + " successfully blocks the attack!")
            block = att_damage
            time.sleep(1)

        # Calculate damage from attack
        damage = att_damage - block
        if damage < 0:
            damage = 0

        # If character has a shield, shield is depleted, not health
        if self.shield > 0:
            # Shield absorbs all damage if shield is greater than damage
            if damage <= self.shield:
                self.app.write(self.name + "'s shield absorbs " + str(damage) + " damage.")
                time.sleep(1)
                self.shield = self.shield - damage
                damage = 0
            # Otherwise some damage will be sustained and shield will be depleted
            elif damage != 0:
                self.app.write(self.name + "'s shield absorbs " + str(self.shield) + " damage.")
                time.sleep(1)
                damage = damage - self.shield
                self.shield = 0

        # Reduce health
        self.app.write(self.name + " suffers " + str(damage) + " damage!")
        self.health = self.health - damage
        time.sleep(1)

        # Check to see if dead or not
        if self.health <= 0:
            self.health = 0
            self.app.write(self.name + " is dead!")
            self.app.write("")
            time.sleep(1)
            return True
        else:
            self.app.write(self.name + " has " + str(self.health) + " hit points left")
            self.app.write("")
            time.sleep(1)
            return False


    def attack_target(self, target):
        """A new normal attack calculation"""
        rate = random.randint(1, 3)
        hit = self.attack + int(rate * target.defense_mod * target.defense - target.resistance)
        if hit <= 1:
            hit = 0
        evasion = target.evasion
        evasionRate = random.randint(0, 1500) # chance to dodge the attack depend on player eveasion stat
        self.app.write(self.name + " dealt " + str(hit) + " damages to " + target.name)
        if evasionRate <= evasion:
            self.app.write(target.name + " dodged the attack")
            time.sleep(1)
            return False
        if target.ratecut > 1:
            damagecut = int(target.max_health * target.ratecut / 100)
            hit -= damagecut
        
        target.health = target.health - hit
        self.app.write(target.name + " suffers " + str(hit) + " damages")
        time.sleep(1)

        if target.health <= 0:
            target.health = 0
            self.app.write(self.name + " has killed " + target.name)
            self.app.write("")
            time.sleep(1)
            return True
        else:
            self.app.write(target.name + " has " + str(target.health) + " hp left")
            return False
        
    #### Character Magic Actions ####
    def heal(self):
        """Heal your hp, comsumes 10 mana"""
        option = random.choice([2, 2.1, 2.2, 2.3, 2.4, 2.5])
        hp = int(self.magic * option + self.level)
        self.mana -= 10
        self.app.write(self.name + "'s heals!! Recovered " + str(hp) + " hp")
        self.app.write("")
        if hp <= 0:
            hp = 1
        hpToHeal = hp + self.health
        if hpToHeal > self.max_health:
            self.health = self.max_health
        else:
            self.health += hp

    def valid_spell(self, choice):
        ''' Checks to see if the spell being cast is a valid spell i.e. can be cast by
        that race and the character has enough mana '''

        valid = False

        # Determine this character's race
        # This is a built-in property we can use to work out the
        # class name of the object (i.e. their race)
        race = self.__class__.__name__

        if choice == 1:
            if race == "Wizard" and self.mana >= 10:
                valid = True
        elif choice == 2 and self.mana >= 20:
            valid = True
        elif choice == 3:
            if race == "Wizard":
                valid = True
        elif choice == 4 and self.mana >= 10:
            if race == "Bishop":
                valid = True
        elif choice == 6 and self.mana >= 25:
            if race == "Bishop":
                valid = True
        elif choice == 7:
            if race == "Paladin":
                valid = True
        return valid

    def cast_spell(self, choice, target=False):
        ''' Casts the spell chosen by the character. Requires 2 parameters - the spell
        being cast and the target of the spell. '''

        kill = False;

        if choice == 1:
            kill = self.cast_fireball(target)
        elif choice == 2:
            self.cast_shield()
        elif choice == 3:
            self.cast_mana_drain(target)
        elif choice == 4:
            self.heal()
        elif choice == 6:
            self.nemesis(target)
        elif choice == 7:
            self.guardian(target)
        else:
            self.app.write("Invalid spell choice. Spell failed!")
            self.app.write("")

        return kill

    def nemesis(self, target):
        """An attack that has a probability to reduce target max_health"""
        self.mana -= 25
        self.app.write(self.name + ' uses nemesis!!')
        time.sleep(1)
        choice = random.choice([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2])
        attack = int(self.magic * 2 * choice - (target.defense_mod * target.defense - target.resistance) * self.nemesis_level)
        reduce_health = random.choice([1, 1, 1, 1, 2]) # chance to inflict blind on the enemy
        if reduce_health == 2:
            self.app.write(target.name + " is blinded")
            target.max_health -= 20
        self.app.write(self.name + ' dealt ' +  str(attack) + ' damages on ' + target.name)
        target.health = target.health - attack

        if target.health <= 0:
            target.health = 0
            self.app.write(target.name + " is dead!")
            self.app.write("")
            time.sleep(1)
            return True
        else:
            self.app.write(self.name + " has " + str(self.health) + " hit points left")
            self.app.write(target.name + " has " + str(target.health) + " hit points left")
            self.app.write("")
            time.sleep(1)
            return False


    def thunder_bolt(self, target):
        """Magic skill can reduces target attack, affects on both melee classes and magic classes"""
        self.mana -= 20
        self.app.write(self.name + 'uses thunder bolt!!')
        time.sleep(1)

        choice = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3]) #probability of dealing double damage on target
        damage = int(self.magic * choice ** 1.25)
        if damage < 0:
            damage = 1
        if choice == 2:
            self.app.write('Spell burst!!!' + self.name + 'dealt ' + str(damage) + ' on ' + target.name)
        elif choice == 1:
            self.app.write(self.name + 'dealt ' + str(damage) + ' on ' + target.name)
        elif choice == 3:
            self.app.write(target.name + " is paralyzed")
            target.attack -= 5
            target.magic -= 3
        self.app.write("")
        target.health = target.health - damage

        kill = target.defend_attack(damage)
        if kill:
            self.app.write(self.name + " has killed " + target.name + ".")
            self.app.write("")
            time.sleep(1)
            return True
        else:
            return False

    def guardian(self, target):
        """Physical attack for paladin"""
        self.app.write(self.name + " 's guardian!!")
        magnitude = random.randint(1, 3)
        hit = self.attack * 2 * magnitude - target.defense - target.resistance
        if hit < 0:
            hit = 1
        self.app.write(self.name + " dealt " + str(hit) + " damages to " + target.name)
        self.app.write("")

        target.health = target.health - hit
        if target.health <= 0:
            target.health = 0
            self.app.write(target.name + " is dead!")
            self.app.write("")
            time.sleep(1)
            return True

        else:
            self.app.write(target.name + " has " + str(target.health) + " hit points left")
            self.app.write("")
            time.sleep(1)
            return False

    def cast_fireball(self, target):
        """Cast fire ball skill, consumes 10 mana"""
        self.mana -= 10
        self.app.write(self.name + " casts Fireball on " + target.name + "!")
        time.sleep(1)

        roll = random.randint(1, 10)
        defense_roll = random.randint(1, 10)
        damage = int(roll * self.magic) - int(defense_roll * target.resistance)
        if damage < 0:
            damage = 0
        """ Aborbing damages """
        if target.shield > 0:
            if damage <= target.shield:
                self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
                time.sleep(1)
                target.shield = target.shield - damage
                damage = 0
            elif damage != 0:
                self.app.write(target.name + "'s shield absorbs " + str(target.shield) + " damage.")
                time.sleep(1)
                damage = damage - target.shield
                target.shield = 0

        self.app.write(target.name + " takes " + str(damage) + " damage.")
        self.app.write("")
        time.sleep(1)
        target.health = target.health - damage

        if target.health <= 0:
            target.health = 0
            self.app.write(target.name + " is dead!")
            self.app.write("")
            time.sleep(1)
            return True

        else:
            self.app.write(target.name + " has " + str(target.health) + " hit points left")
            self.app.write("")
            time.sleep(1)
            return False

    def blizzard(self, target):
        """An magic attack which can causes massive amount of damages"""
        point = random.choice([1, 1, 1, 2, 2, 3, 3, 4, 5, 6])
        matk = self.magic * 2 
        self.app.write(self.name + " 's blizzard")
        self.mana -= 20
        time.sleep(1)
        attack = int(matk * 1.414 * point)
        target.defense -= 2
        kill = target.defend_attack(attack)
        if kill:
            self.app.write(self.name + " has killed " + target.name + ".")
            self.app.write("")
            time.sleep(1)
            return True
        else:
            return False

    
    def backstab(self, target):
        """
        an attack which can inflict a huge amount of damage on target. 
        
        """
        point = random.choice([1, 1, 1, 1, 1, 1, 1, 2, 2, 2]) #30% rate to do double backstab
        score = random.choice([2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8])
        self.app.write(self.name + " 's backstab!!")
        self.mana -= 50
        time.sleep(1)
        attack = round(((self.attack * score * 100) / (target.resistance)) * point)
        if attack < 0:
            attack = 1
        time.sleep(1)
        self.app.write(self.name + ' dealt ' + str(attack) + ' critical damages' )
        self.app.write("")
        target.health = target.health - attack

        if target.health <= 0:
            self.health = 0
            self.app.write(target.name + " is dead!")
            self.app.write("")
            time.sleep(1)
            return True
        else:
            self.app.write(self.name + " has " + str(self.health) + " hit points left")
            self.app.write(target.name + " has " + str(target.health) + " hit points left")
            self.app.write("")
            time.sleep(1)
            return False

    def crossfire(self, target):
        self.mana -= 12
        self.app.write(self.name + " uses crossfire!!")

    def cast_shield(self):
        """Cast sheld, increase defense for the next attack"""
        self.mana -= 20
        self.app.write(self.name + " casts Shield!")
        time.sleep(1)
        if self.shield <= self.max_shield:
            self.shield = self.max_shield
        self.app.write(self.name + " is shielded from the next " + str(self.shield) + " damage.")
        self.app.write("")
        time.sleep(1)

    def cast_mana_drain(self, target):
        """Drain player's mana"""
        self.app.write(self.name + " casts Mana Drain on " + target.name + "!")
        time.sleep(1)

        if target.mana >= 20:
            drain = 20
        else:
            drain = target.mana
        self.app.write(self.name + " drains " + str(drain) + " mana from " + target.name + ".")
        time.sleep(1)

        target.mana -= drain
        self.mana += drain
        if target.mana <= 0:
            target.mana = 0
            self.app.write(target.name + "'s mana has been exhausted!")
        else:
            self.app.write(target.name + " has " + str(target.mana) + " mana left")
        self.app.write("")

    #### Character Item Actions ####
    def use_mana(self):
        """use mana potions """
        if self.mana_potions_update >= 1:
            self.mana_potions_update -= 1
            self.mana += 20
            if self.mana > self.max_mana:
                self.mana = self.max_mana
            self.app.write(self.name + " uses mana potion")
            self.app.write("")
            self.app.write(self.name + " has " + str(self.mana) + " mana.")
            return True
        else:
            self.app.write("You have no potion to use")
            self.app.write("")
            return False
        
    def use_potion(self):
        """
        Uses a health potion if the player has one. Returns True if has potion,
        false if hasn't
        """
        if self.potions >= 1:
            self.potions -= 1
            self.health += 250
            if self.health > self.max_health:
                self.health = self.max_health
            self.app.write(self.name + " uses a potion!")
            time.sleep(1)
            self.app.write(self.name + " has " + str(self.health) + " hit points.")
            self.app.write("")
            time.sleep(1)
            return True
        else:
            self.app.write("You have no potions left!")
            self.app.write("")
            return False

    #### Miscellaneous Character Actions ####

    def reset(self):
        ''' Resets the character to its initial state '''

        self.health = self.max_health;
        self.mana = self.max_mana;
        self.potions = self.starting_potions;
        self.shield = 0

    def print_status(self):
        ''' Prints the current status of the character '''
        self.app.write(self.name + "'s Status:")
        time.sleep(0.5)

        health_bar = "Health: "
        health_bar += "|"
        i = 0
        while i <= self.max_health:
            if i <= self.health:
                health_bar += "#"
            else:
                health_bar += " "
            i += 25
        health_bar += "| " + str(self.health) + " hp (" + str(int(self.health * 100 / self.max_health)) + "%)"
        self.app.write(health_bar)
        time.sleep(0.5)

        if self.max_mana > 0:
            mana_bar = "Mana: "
            mana_bar += "|"
            i = 0
            while i <= self.max_mana:
                if i <= self.mana:
                    mana_bar += "*"
                else:
                    mana_bar += " "
                i += 10
            mana_bar += "| " + str(self.mana) + " mp (" + str(int(self.mana * 100 / self.max_mana)) + "%)"
            self.app.write(mana_bar)
            time.sleep(0.5)

        if self.shield > 0:
            shield_bar = "Shield: "
            shield_bar += "|"
            i = 0
            while i <= 100:
                if i <= self.shield:
                    shield_bar += "o"
                else:
                    shield_bar += " "
                i += 10
            shield_bar += "| " + str(self.shield) + " sp (" + str(int(self.shield * 100 / self.max_shield)) + "%)"
            self.app.write(shield_bar)
            time.sleep(0.5)

        self.app.write("Potions remaining: " + str(self.potions))
        self.app.write("")
        time.sleep(0.5)


######
### Define the attributes specific to each of the Character Subclasses.
### This identifies the differences between each race.
######

class Dwarf(Character):
    '''Defines the attributes of a Dwarf in the game. Inherits the constructor and methods
    of the Character class '''

    # Constructor for Dwarf class
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Dwarf"
        self.level = level
        self.max_health = 300;
        self.max_mana = 30;
        self.starting_potions = 1;
        self.attack = 10;
        self.ratecut = 1
        self.defense = 6;
        self.magic = 4;
        self.evasion = self.level
        self.resistance = 5;
        self.health = self.max_health;
        self.mana = self.max_mana;
        self.potions = self.starting_potions;
        self.exp = 0
        self.coin = 0

    def move(self, player):
        """ Defines the AI for the Dwarf class """
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('a')
            return self.attack_enemy(player)
        return False


class Elf(Character):
    '''Defines the attributes of an Elf in the game. Inherits the constructor and methods
    of the Character class '''

    # Constructor for Elf class
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Elf"
        self.max_health = 300;
        self.max_mana = 60;
        self.starting_potions = 1;
        self.attack = 6;
        self.level = level
        self.evasion = self.level
        self.defense = 8;
        self.magic = 8;
        self.resistance = 8;
        self.health = self.max_health;
        self.mana = self.max_mana;
        self.ratecut = 1
        self.potions = self.starting_potions;
        self.exp = 1
        self.coin = 0

    def move(self, player):
        """ Defines the AI for the Elf class """
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('d')
            if self.shield == 0 and self.mana >= 20:
                self.cast_spell(2)
            else:
                return self.attack_enemy(player)
        return False


class Goblin(Character):
    '''Defines the attributes of a Goblin in the game. Inherits the constructor and methods
    of the Character class '''

    # Constructor for Goblin class
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Goblin"
        self.level = level
        self.max_health = 250;
        self.max_mana = 10;
        self.starting_potions = 0;
        self.attack = 3;
        self.defense = 3;
        self.magic = 0;
        self.resistance = 0;
        self.health = self.max_health;
        self.mana = self.max_mana;
        self.potions = self.starting_potions;
        self.ratecut = 1
        self.exp = 1
        self.coin = 0

    def move(self, player):
        """ Defines the AI for the Goblin class """
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('d')
            return self.quick_attack(player)
        return False


class Hobbit(Character):
    '''Defines the attributes of a Hobbit in the game. Inherits the constructor and methods
    of the Character class '''

    # Constructor for Hobbit class
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Hobbit"
        self.max_health = 250
        self.max_mana = 40
        self.starting_potions = 2
        self.level = level
        self.evasion = self.level
        self.attack = 7
        self.defense = 9
        self.magic = 6
        self.evasion = self.level
        self.resistance = 10
        self.health = self.max_health
        self.mana = self.max_mana
        self.potions = self.starting_potions
        self.exp = 1
        self.coin = 0
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        """ Defines the AI for the Hobbit class """
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('d')
            # Hobbits shield if they don't have one
            if self.shield == 0 and self.mana >= 20:
                self.cast_spell(2)
            else:
                return self.attack_enemy(player)
        return False


class Human(Character):
    '''Defines the attributes of a Human in the game. Inherits the constructor and methods
    of the Character class '''

    # Constructor for Human class
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Human"
        self.level = level
        self.max_health = 250
        self.max_mana = 40
        self.starting_potions = 1
        self.attack = 13
        self.defense = 9
        self.evasion = self.level
        self.magic = 6
        self.ratecut = 1
        self.resistance = 5
        self.health = self.max_health;
        self.mana = self.max_mana;
        self.potions = self.starting_potions;
        self.exp = 1
        self.coin = 0
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        """ Defines the AI for the Human class """
        move_complete = Character.move(self, player)
        if not move_complete:
            if self.health * 100 / self.max_health > 75:
                self.set_stance('a')
            elif self.health * 100 / self.max_health > 30:
                self.set_stance('b')
            else:
                self.set_stance('d')
            if self.shield == 0 and self.mana >= 20:
                self.cast_spell(2)
            else:
                return self.attack_enemy(player)
        return False


class Orc(Character):
    '''Defines the attributes of an Orc in the game. Inherits the constructor and methods
    of the Character class '''

    # Constructor for Orc class
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Orc"
        self.max_health = 250
        self.max_mana = 10
        self.starting_potions = 0
        self.level = level
        self.attack = 11
        self.defense = 6
        self.magic = 3
        self.evasion = self.level
        self.resistance = 5
        self.health = self.max_health;
        self.mana = self.max_mana;
        self.ratecut = 1
        self.potions = self.starting_potions;
        self.exp = 1
        self.coin = 0
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        """ Defines the AI for the Orc class """
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('b')
            return self.quick_attack(player)
        return False


class Uruk(Character):
    '''Defines the attributes of an Uruk in the game. Inherits the constructor and methods
    of the Character class '''

    # Constructor for Uruk class
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name,  app)
        self.job = "Uruk"
        self.max_health = 400;
        self.max_mana = 20;
        self.starting_potions = 1;
        self.level = level
        self.evasion = self.level
        self.attack = 12;
        self.defense = 7;
        self.ratecut = 1
        self.magic = 4;
        self.resistance = 7;
        self.health = self.max_health;
        self.mana = self.max_mana;
        self.potions = self.starting_potions;
        self.exp = 1
        self.coin = 0
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        """ Defines the AI for the Uruk class """
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('a')
            return self.attack_enemy(player)
        return False


class Wizard(Character):
    '''Defines the attributes of a Wizard in the game. Inherits the constructor and methods
    of the Character class '''

    # Constructor for Wizard class
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Wizard"
        self.level = level
        self.max_health = 150 + int(self.level / 1.2);
        self.max_mana = 100 + int(self.level / 2);
        self.starting_potions = 2;
        self.attack = 5 + int(self.level / 2);
        self.defense = 3 + self.level
        self.evasion = self.level
        self.magic = 10;
        self.ratecut = 1
        self.resistance = 10;
        self.health = self.max_health;
        self.mana = self.max_mana;
        self.potions = self.starting_potions;
        self.exp = 1
        self.coin = 0
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        """ Defines the AI for the Wizard class """
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('d')
            if self.mana < 10 and player.mana > 0:
                self.cast_spell(3, player)
            elif self.shield == 0 and self.mana >= 20:
                self.cast_spell(2)
            elif self.mana >= 10:
                return self.cast_spell(1, player)
            else:
                return self.attack_enemy(player)
        return False

"""
Another class, cannot be chosen. 

"""


class Dragon(Character):
    """Boss"""
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = 'Dragon'
        self.level = level
        self.max_health = 500 * self.level
        self.max_mana = 150 + self.level + 20
        self.starting_potions = 2
        self.attack = 20
        self.defense = 20
        self.evasion = self.level
        self.ratecut = 1
        self.magic = 20
        self.resistance = 30
        self.health = self.max_health
        self.mana = self.max_mana
        self.potions = self.starting_potions
        self.exp = 1
        self.coin = 0
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('a')
            if self.health < 50:
                self.cast_shield()
                self.resistance += 10
            elif self.mana > 50:
                return self.backstab(player)
            else:
                return self.attack_enemy(player)
        return False



class Bishop(Character):

    ''' class Bishop, great support '''
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Bishop"
        self.level = level
        self.max_health = 190 + self.level * 2
        self.max_mana = 150 + self.level * 2
        self.starting_potions = 2
        self.attack = 10
        self.evasion = self.level
        self.defense = 20 + self.level
        self.magic = 25 + int(self.level * 1.5)
        self.resistance = 23 + self.level
        self.ratecut = 1
        self.health = self.max_health
        self.mana = self.max_mana
        self.potions = self.starting_potions
        self.exp = 1
        self.coin = 0
        self.nemesis_level = 1
        self.heal_level = 1
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('d')
            if self.mana < 10 and player.mana > 0:
                self.cast_spell(3, player)
            elif self.shield == 0 and self.mana >= 20:
                self.cast_spell(2)
            elif self.mana >= 10:
                return self.cast_spell(1, player)
            else:
                return self.attack_enemy(player)
        return False


class Mega(Character):
    '''Mega class, high hp, high defense but low attack'''
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Mega"
        self.level = level 
        self.max_health = 1000 * (self.level / 2)
        self.max_mana = 150 + int(self.level * 1.2)
        self.starting_potions = 0
        self.attack = 8 + self.level
        self.evasion = self.level
        self.defense = 50 + self.level + self.attack
        self.magic = 12 + self.level + 2
        self.resistance = 48 + self.level
        self.ratecut = 1
        self.health = self.max_health
        self.mana = self.max_mana
        self.potions = self.starting_potions
        self.exp = 1
        self.coin = 0
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('d')
            if player.health > 0:
                self.tempest(player)
            else:
                return self.tempest(player)
        return False


class Assassin(Character):
    ''' A class that has highest DPS but low defense, low health and low mana'''
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.level = level
        self.max_health = 150 + int(self.level * 2)
        self.max_mana = 50
        self.starting_potions = 0
        self.attack = 13 + int(self.level * 1.3)
        self.evasion = self.level * 1.5
        self.defense = 2
        self.magic = 3 + self.level
        self.resistance = 5
        self.health = self.max_health
        self.mana = self.max_mana
        self.potions = self.starting_potions
        self.exp = 1
        self.coin = 0
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('a')
            if self.mana > 0:
                self.backstab(player)
            else: 
                return self.attack(player)
        return False

class Mobs(Character):
    """This class will replace pretty much all the current classes"""
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Mobs"
        self.level = level
        self.coin = 0
        self.ratecut = 1
        self.max_health = 170 + self.level * 2
        self.max_mana = 50 + int(self.level * 1.5)
        self.starting_potions = 0
        self.attack = 10 + int(self.level * 1.3)
        self.evasion = self.level
        self.defense = 5 + self.level * 2
        self.magic = 3 + self.level 
        self.resistance = 5 + self.level + 3
        self.health = self.max_health
        self.mana = self.max_mana
        self.potions = self.starting_potions
        self.exp = 1
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions
        
    def move(self, player):
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('b')
            if self.health > 0:
               return self.attack_target(player)
        return False

class Warrior(Character):
    """Starter class"""
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Warrior"
        self.level = level
        self.coin = 0
        self.ratecut = 1
        self.max_health = 170 + self.level
        self.max_mana = 50 + self.level
        self.starting_potions = 0
        self.attack = 10 + self.level + 1
        self.evasion = self.level
        self.defense = 5 + self.level + 1
        self.magic = 3 + self.level 
        self.resistance = 5 + self.level + 1
        self.health = self.max_health
        self.mana = self.max_mana
        self.potions = self.starting_potions
        self.exp = 1
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('b')
            if self.health > 0:
               return self.attack_target(player)
        return False
        
class Paladin(Character):
    """This class has high health, greate defense but low in damage"""
    def __init__(self, char_name, level, app):
        Character.__init__(self, char_name, app)
        self.job = "Paladin"
        self.level = level
        self.coin = 0
        self.ratecut = 1
        self.max_health = 210 + self.level * 2
        self.max_mana = 50 + int(self.level * 1.5)
        self.starting_potions = 0
        self.attack = 10 + int(self.level * 1.3)
        self.evasion = self.level
        self.defense = 5 + self.level * 2
        self.magic = 3 + self.level 
        self.resistance = 5 + self.level + 3
        self.health = self.max_health
        self.mana = self.max_mana
        self.potions = self.starting_potions
        self.exp = 1
        self.mana_potions = 1
        self.mana_potions_update = self.mana_potions

    def move(self, player):
        move_complete = Character.move(self, player)
        if not move_complete:
            self.set_stance('b')
            if self.health > 0:
               return self.attack_target(player)
        return False