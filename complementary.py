import numpy as np
import pandas as pd

class clothingItem(object):
    def __init__(self, img, type, colors=[], percents=[], name=""):
        self.name = img.split('/')[-1] if img else name
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

#def possibleClosestCompliment(clothes, item, ):
    type=item.type
    df = pd.DataFrame([vars(obj) for obj in clothes])
    df=255-df["colors"]
    targetRGB=255-np.array(item.getColors())
    differences=df[df['type']!=type]-targetRGB
    
    
    
    
    
    
    return 

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
