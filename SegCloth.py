from transformers import pipeline
from PIL import Image
import numpy as np


# Initialize segmentation pipeline
segmenter = pipeline(model="mattmdjaga/segformer_b2_clothes")


def segment_clothing(image, clothes=["Hat", "Upper-clothes", "Skirt", "Pants", "Dress", "Belt", "Left-shoe", "Right-shoe", "Scarf"]):
    # Convert image to RGBA if it's not already
    if isinstance(image, str):
        image = Image.open(image)
    image = image.convert('RGBA')
    
    # Segment image
    segments = segmenter(image)
    
    # Create list of masks
    mask_list = []
    for s in segments:
        if s['label'] in clothes:
            mask_list.append(s['mask'])
    
    if not mask_list:
        return image
        
    # Paste all masks on top of each other
    final_mask = np.array(mask_list[0])
    for mask in mask_list[1:]:
        current_mask = np.array(mask)
        final_mask = np.clip(final_mask + current_mask, 0, 255)
            
    # Convert final mask to PIL image
    final_mask = Image.fromarray(final_mask.astype(np.uint8), mode='L')
    
    # Apply mask to original image
    image.putalpha(final_mask)
    
    return image
