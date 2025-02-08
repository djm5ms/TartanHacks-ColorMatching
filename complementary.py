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

def possibleClosestCompliment(clothes, item=clothingItem(img='',type='')):
    if item is None:
        return {}
    
    type=item.getType()
    
    df = pd.DataFrame([vars(obj) for obj in clothes])
    
    df=df["colors"]-255
    
    targetRGB=np.array(item.getColors())-255
    
    differences=abs(df[df['type']!=type]-targetRGB)
    
    output={}
    
    for type in unique(differences['type']):
        output[type]=clothingItem(type=type, colors=df[df[type]==type].iloc[differences[differences[type]==type].sum(axis=1).idxmin()]['colors'])
    return output


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

def weightedAverage(item):
    weighted = []
    for i in range(len(item.colors)):
        weighted.append(item.colors[i] * item.percents[i])
    return weighted
        
        
    

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
