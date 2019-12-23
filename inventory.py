
import random

class Inventory:
    def __init__(self, player, app):
        self.player = player
        self.bag = ['Potions', 'Postions']
        self.size = 300
        self.app = app

    def viewInventory(self, player, app):
        """View Inventory"""
        if len(self.bag) < 1:
            self.app.write("There is nothing to view here")
        else:
            for i in self.bag:
                self.app.write(i)
            self.app.write("Inventory space available " + str(len(self.bag)) + "/300")
    
    def dispose(self, item, app):
        """Dispose an item, param item_name"""
        try: 
            for i in self.bag:
                if i == item:
                    self.bag.remove(item)
                    self.app.write('Successfully removed' + i)
                else:
                    raise ValueError
        except ValueError:
            self.app.write("")

    def inputItem(self, item, app):
        """Collect item after battle"""
        #check if the bag is full
        if len(self.bag) > self.size:
            self.app.write("Your bag is full, this item cannot be inserted")
            self.app.write("Disposing the item...")
        else:    
            self.bag.append(item)      
    
