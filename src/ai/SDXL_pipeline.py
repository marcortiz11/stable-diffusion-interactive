import argparse

import PIL
import torch
from diffusers import AutoPipelineForImage2Image

class SDXL:

    def __init__(self, model_id="runwayml/stable-diffusion-v1-5"):
        self.model_id = model_id
        self.pipe = AutoPipelineForImage2Image.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        )
        self.pipe.enable_model_cpu_offload()
        #self.pipe.enable_xformers_memory_efficient_attention()

    def run(self, init_image, prompt):
        """
        Runs the pipeline
        """
        image = self.pipe(prompt, image=init_image, strength=0.5).images[0]
        return image

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-image', type=str, default='./src/ai/inputs/input_stable_difussion.jpg', help='An input image')
    parser.add_argument('-output', type=str, required=True, help='The output path of the resulting image')
    parser.add_argument('-prompt', type=str, default='turn them into cartoons', help='The style to apply')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()

    # Inputs
    prompt = args.prompt
    image = PIL.Image.open(args.image)

    pipeline = SDXL()
    image_result = pipeline.run(image, prompt)

    # Save
    image_result.save(args.output)