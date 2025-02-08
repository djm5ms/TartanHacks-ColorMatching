from transformers import pipeline
from PIL import Image
import numpy as np

# Initialize segmentation pipeline
segmenter = pipeline(model="mattmdjaga/segformer_b2_clothes")

def segment_clothing(filepath, clothes=["Hat", "Upper-clothes", "Skirt", "Pants", "Dress", "Belt", "Left-shoe", "Right-shoe", "Scarf"]):
    # Load image and ensure it's in RGB mode first
    img = Image.open(filepath).convert('RGB')
    
    # Segment image
    segments = segmenter(img)
    
    # Create list of masks
    mask_list = []
    for s in segments:
        if s['label'] in clothes:
            mask_list.append(s['mask'])
    
    if not mask_list:
        # Convert to RGBA before returning if no masks found
        return img.convert('RGBA')
        
    # Combine masks
    final_mask = np.zeros_like(np.array(mask_list[0]))
    for mask in mask_list:
        current_mask = np.array(mask)
        final_mask = np.maximum(final_mask, current_mask)
            
    # Convert to RGBA and apply mask
    img = img.convert('RGBA')
    
    # Convert mask to proper format for alpha channel
    final_mask = Image.fromarray((final_mask * 255).astype('uint8'))
    
    # Apply alpha mask
    img.putalpha(final_mask)
    
    return img
