# Image style change with Stable diffusion

This repository contains code to run a stable diffusion model that generates new images, given an existing image and a promp text.
The software can be interacted via GUI or terminal, as shown in the picture below:

![Alt text](./example_interface.png)

The model not only changes the style of the input image, but is also to interpret what you request in the prompt and add it to the final image.


## Installation
`pip install -r requirements.txt` \

Then just add to the PYTHONPATH variable the location of the project folder: \
`export PYTHONPATH=$PYTHONPATH/path/to/project/folder`

## Usage
#### Step 1: Run the interface
Execute the script you'll find in `./gui/gui.py`. It will take a bit of time to open since it's loading the model. \
![Alt text](./step1.png)

#### Step 2: Click on the left side of the panel to load an image
![Alt text](./steep2.png)

#### Step 3: Write a prompt and click button to run  inference
![Alt text](./step4.png)

## Information
**Author**: Marc Ortiz Torres \
**email**: ortiztorresmarc@gmail.com