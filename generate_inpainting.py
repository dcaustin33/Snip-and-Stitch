import inspect
from typing import List, Optional, Union
import os

import argparse
import numpy as np
import torch
import PIL
import gradio as gr
from diffusers import StableDiffusionInpaintPipelineLegacy
import requests
from io import BytesIO


def predict(
    image_path: str, 
    mask_path: str,
    prompt: str, 
    num_inference_steps: int = 100,
    guidance_scale: float = 12.5
) -> List[PIL.Image.Image]:
    """Generate an image conditioned on a prompt.
    
    Args:
        image_path: The path to the image to condition on.
        mask_path: The path to the mask to condition on.
        prompt: The prompt to condition on.
        args: The arguments to use for generation.
        
    Returns:
        10 generated images.
    """
    image = PIL.Image.open(image_path).resize((512, 512))
    mask_image = PIL.Image.open(mask_path).convert("RGB").resize((512, 512))
    # save the image with the mask applied on top
    images = pipe(prompt=prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    image=image,
                    mask_image=mask_image,
                    num_images_per_prompt = 6).images
    return(i for i in images)

def run_for_one_path(
    num_images_to_generate: int,
    image_path: str,
    mask_path: str,
    prompt: str,
    num_inference_steps: int,
    guidance_scale: float,
    output_path: str
) -> None:
    global global_counter
    local_counter = 0
    while local_counter < num_images_to_generate:
        images = predict(image_path, mask_path, prompt, num_inference_steps, guidance_scale)
        for image in images:
            if local_counter >= num_images_to_generate:
                break
            image.save(output_path + str(global_counter) + ".png")
            local_counter += 1
            global_counter += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', type=str, default='A painting of a coral reef', help='prompt to condition on')
    parser.add_argument('--num_inference_steps', type=int, default=100, help='number of inference steps')
    parser.add_argument('--guidance_scale', type=float, default=12.5, help='scale of guidance')
    parser.add_argument('--model_path', type=str, default='outputs_solo_texture_model', help='path to model')
    parser.add_argument('--image_paths', type=str, nargs='+', help='different paths to images')
    parser.add_argument('--mask_paths', type=str, nargs='+', help='different paths to images')
    parser.add_argument('--output_path', type=str, help='path to output')
    parser.add_argument('--num_images_to_generate', type=int, default=1, help='number of images to generate for each path')
    parser.add_argument('--device', type=str, default='cuda', help='device to run on')
    
    args = parser.parse_args()

    device = "cuda"
    model_path = args.model_path

    print('loading model')
    pipe = StableDiffusionInpaintPipelineLegacy.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        safety_checker=None
    ).to(args.device)
    print
    
    global_counter = 0
    
    current_path = ''
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
    with torch.no_grad():
        for index in range(len(args.image_paths)):
            image_path = args.image_paths[index]
            mask_path = args.mask_paths[index]
            output_path = args.output_path
            run_for_one_path(
                args.num_images_to_generate, 
                image_path, mask_path, 
                args.prompt, 
                args.num_inference_steps, 
                args.guidance_scale, 
                output_path
            )