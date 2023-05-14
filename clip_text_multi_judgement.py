import os
from typing import List

import argparse
from PIL import Image
import requests
from matplotlib import pyplot as plt
from transformers import CLIPProcessor, CLIPModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from torchvision.transforms import functional as F

def CLIP_text_similarity(images: List[Image.Image],
                          model: CLIPModel,
                          processor: CLIPProcessor,
                          prompt: str,
                          device: str) -> torch.Tensor:
    """gets the clip similarity score between the images and the prompt"""
    similarity = []
    for i in range(round(len(images)/10)):
        current_ims = images[i*10:(i+1)*10]
        inputs = processor(text=[prompt]*len(current_ims), images=current_ims, return_tensors="pt", padding=True)
        for inp in inputs:
            inputs[inp] = inputs[inp].to(device)
        outputs = model(**inputs)
        similarity.extend(outputs['logits_per_image'].detach().cpu().numpy()[:, 0])
    return similarity


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default='solo_texture_model', help='name of the comparison')
    parser.add_argument('--prompt', type=str,)
    parser.add_argument('--generated_image_paths', nargs='+', type=str, help='List of generated image paths')
    parser.add_argument('--output_path', type=str)
    parser.add_argument('--device', type=str, default='cuda')
    args = parser.parse_args()
    
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16").to(args.device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
        
    generated_images = []
    generated_im_name = []
    generated_im_index = []
    print(args.generated_image_paths)
    for i, directory in enumerate(args.generated_image_paths):
        print('length pf directory', len(os.listdir(directory)))
        for im_dir in os.listdir(directory):
            # skip the ranked and generations folder
            if im_dir.split('/')[-1] in ['ranked', 'generations']: continue
            generated_images.append(Image.open(os.path.join(directory, im_dir)))
            generated_im_name.append(os.path.join(directory, im_dir))
            generated_im_index.append(i)
        
    similarity = CLIP_text_similarity(generated_images, model, processor, args.prompt, args.device)
    
    # zip the similarity and generated_im_name together and sort by similarity
    zipped = []
    for i in range(len(similarity)):
        zipped.append((similarity[i], generated_im_name[i], generated_im_index[i]))
    zipped = sorted(zipped, key=lambda x: x[0], reverse=True)
    
    # get the stats of how many in the top 20, 40, 60, 80, 100 where from each generated_im_index
    top_k = [20, 40, 60, 80, 100]
    stats = {i: 0 for i in range(len(args.generated_image_paths))}
    for i in range(min(top_k[-1] + 1, len(zipped))):
        _, _, index = zipped[i]
        if index in stats:
            stats[index] += 1
            
        # reports stats for the top k if i is in top_k
        if i + 1 in top_k:
            # Output the stats
            for ranked_index in range(len(args.generated_image_paths)):
                percentage = (stats[ranked_index] / (i + 1)) * 100 if i > 0 else 0
                print(f"Top {i + 1}: {stats[ranked_index]} images ({percentage:.2f}%)")
    

    # Calculate average ranking of images
    average_ranking = {i: [] for i in range(len(args.generated_image_paths))}

    for i, (_, _, index) in enumerate(zipped):
        average_ranking[index].append(i + 1)
        
    print("Average Rankings:")
    for index, average_rank in average_ranking.items():
        print(f"Generated Image Path {index + 1}: {np.mean(np.array(average_rank))}")

    if not os.path.exists(args.output_path):
        os.mkdir(args.output_path)
        
    for i, (sim, image_path, _) in enumerate(zipped):
        # save to generated image path with the name output 1 for the top ranked
        image = Image.open(image_path)
        image.save(os.path.join(args.output_path, 'output_{}.png'.format(i)))
        
    print(f'For {args.name} the average similarity was {np.mean(similarity)}')
        
    