import numpy as np
import pandas as pd
from numpy import unique
import math

class clothingItem(object):
    def __init__(self, img, type, colors=[], percents=[], name=""):
        if name == "":
            self.name = img.split('/')[-1] if img else name
        name=name
        self.img = img
        self.type = type
        self.colors = colors
        self.percents = percents
    def getImg(self):
        return self.img
    def getType(self):
        return self.type
    def getColors(self):
        return self.colors
    def getPercents(self):
        return self.percents
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name
    def setImg(self, img):
        self.img = img
    def setType(self, type):
        self.type = type
    def setColors(self, colors):
        self.colors = colors
    def setPercemnts(self, percemnts):
        self.percemnts = percemnts
    def toString(self):
        return f"Name: {self.name}, Type: {self.type}, Colors: {self.colors}, Percents: {self.percents}"

def getRGBList(clothes):
    rgbList = []
    for item in clothes:
        rgbList.append(item.colors)
    return rgbList

def makeRGBCompliments(clothes):
    compliments = []
    clothes = clothes
    for item in clothes:
        compliments.append(255-item.colors)
    return compliments

def possibleClosestCompliment(clothes, item):
    
    
    if item is None or not clothes:
        return {}
    
    type = item.getType()
    
    # Create DataFrame
    df = pd.DataFrame([{
        'type': obj.getType(),
        'colors': obj.getColors(),
        'percents': obj.getPercents(),
        'item': obj
    } for obj in clothes])
    

    
    # Calculate weighted average for target item
    targetRGB = np.array(weightedAverage(item)) - 255
    
    # Apply weightedAverage to each row and calculate difference
    df['difference'] = df.apply(lambda row: np.sum(np.abs(np.array(weightedAverage(row['item'])) - 255 - targetRGB)), axis=1)
    
    
    # Filter out items of the same type as the target
    differences = df[df['type'] != type]
    
    
    output = {}
    output[item.getType()] = item
    for unique_type in differences['type'].unique():
        type_subset = differences[differences['type'] == unique_type]
        closest_item = type_subset.loc[type_subset['difference'].idxmin()]['item']
        output[unique_type] = closest_item
    
    return output

# Helper function to calculate weighted average
def weightedAverage(item):
    return [color * percent for color, percent in zip(item.getColors(), item.getPercents())]



color_dict = {
    "red": [255, 0, 0],
    "orange": [255, 165, 0],
    "yellow": [255, 255, 0],
    "spring green": [0, 255, 127],
    "green": [0, 255, 0],
    "turquoise": [64, 224, 208],
    "cyan": [0, 255, 255],
    "ocean": [0, 119, 190],
    "blue": [0, 0, 255],
    "violet": [238, 130, 238],
    "magenta": [255, 0, 255],
    "raspberry": [135, 38, 87]
}

def closestToo(item):
    min_distance = 1000
    closest= None
    for rgb in color_dict.keys():
        temp = math.sqrt(sum([(a - b) ** 2 for a, b in zip(item.colors, color_dict[rgb])]))
        if temp < min_distance:
            min_distance = temp
            closest = rgb
    
    return closest
        
        
    

def closestCompliment(usingItem, compliments, clothes):
    lowest = 1000
    closestCompliment = None
    
    # Find index of using item's colors in rgbList
    usingItemIndex =  clothes.index(usingItem)
    
    # Calculate complement of using item
    chosenItemCompliment = [255 - c for c in usingItem.colors]
    
    for i in range(len(clothes)):
        if i != usingItemIndex and clothes[i].type != usingItem.type:
            # Calculate total RGB difference
            for j in range(len(chosenItemCompliment)):
                difference = sum(abs(chosenItemCompliment[j] - compliments[i][j]))
            
            if difference < lowest:
                lowest = difference
                closestCompliment = clothes[i]
    if (closestCompliment == None):
        return usingItem
    return closestCompliment

def findFromName(name, clothes):
    for clothing in clothes:
        if clothing.getImg() == name:
            return clothing
    return None
