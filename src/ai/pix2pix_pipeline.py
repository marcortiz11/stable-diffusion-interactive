"""
    Author: Marc Ortiz Torres
    Date: 17 Feb 2024
"""

import argparse

import PIL
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler


class Pix2Pix:

    def __init__(self, model_id="timbrooks/instruct-pix2pix"):
        self.model_id = model_id
        self.pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, safety_checker=None)
        self.pipe.to("cuda")
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)

    def run(self, image, prompt):
        """
        Runs the pipeline
        """
        return self.pipe(prompt, image=image, num_inference_steps=50, image_guidance_scale=1).images[0]

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-image', type=str, default='./inputs/input_stable_difussion.jpg', help='An input image')
    parser.add_argument('-output', type=str, required=True, help='The output path of the resulting image')
    parser.add_argument('-prompt', type=str, default='turn them into cartoons', help='The style to apply')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()

    # Inputs
    prompt = args.prompt
    image = PIL.Image.open(args.image)

    pipeline = Pix2Pix()
    image_result = pipeline.run(image, prompt)

    # Save
    image_result.save(args.output)