#Implimentation-Borshon Debnath
import json
from inventory_management import InventoryItem
class InventoryItem:
    def __init__(self,itemId,itemName,quantity,unit,minimumStock):
        self.itemId=itemId
        self.itemName=itemName
        self.quantity=quantity
        self.unit=unit
        self.minimumStock=minimumStock

    #load data into json
    def to_inventory_json(self):
        return{
        "itemId":self.itemId,
        "itemName":self.itemName,
        "quantity":self.quantity,
        "unit":self.unit,
        "minimumStock":self.minimumStock 
        }    
