from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

def elbow_method(data, max_k=10):
    wcss = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)
    
    # Find the elbow point
    differences = np.diff(wcss)
    elbow_point = np.argmin(differences) + 1
    
    return elbow_point + 1

def detect_colors(image_path, num_colors=10):
    # Open the image
    img = Image.open(image_path)
    
    # Convert image to RGB mode if it's not already
    img = img.convert('RGB')
    
    # Get image data as a numpy array
    img_array = np.array(img)
    
    # Reshape the array to 2D (each row is a pixel)
    pixels = img_array.reshape(-1, 3)
    df = pd.DataFrame(pixels, columns=['R', 'G', 'B'])
    
    optimal_k = elbow_method(df, max_k=10)
    
    kmeans_new = KMeans(n_clusters=optimal_k, random_state=40)
    df['color'] = kmeans_new.fit_predict(df)

    percentForK = []
    for i in range(optimal_k):
        percentForK.append((df['color'] == i).sum() / len(df) * 100)

    
    
    
    
    return kmeans_new.cluster_centers_, percentForK
