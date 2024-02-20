"""
    Author: Marc Ortiz Torres
    Date: 19 Feb 2024
"""

from src.ai.inference import StableDiffusion
from src.utils import euclidean_distance

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageOps
from tkinter import filedialog as fd

class Window:

    def __init__(self):
        self.engine = StableDiffusion()
        self.polygon_coords = []
        self.polygon_closed = False

        self.window = tk.Tk()
        self.window.geometry("900x400")
        self.window.title('Marc Ortiz interview test')

        # Controls line 1
        self.control_frame_1 = tk.Frame(self.window)
        self.control_frame_1.grid(row=0, columnspan=2, sticky='ew')

        self.prompt_text_description = tk.Label(self.control_frame_1, text='Prompt: ')
        self.prompt_text_description.pack(side=tk.LEFT)
        self.prompt_text = tk.Entry(self.control_frame_1, width=60)
        self.prompt_text.pack(side=tk.LEFT, expand=True)

        self.inference_button = tk.Button(self.control_frame_1, text='Run inference')
        self.inference_button.pack(side=tk.LEFT, expand=True)
        self.inference_button.bind('<Button-1>', self.do_inference)

        self.save_button = tk.Button(self.control_frame_1, text='Load image')
        self.save_button.pack(side=tk.LEFT, expand=True)
        self.save_button.bind('<Button-1>', self.load_input_image)

        self.save_button = tk.Button(self.control_frame_1, text='Save image')
        self.save_button.pack(side=tk.LEFT, expand=True)
        self.save_button.bind('<Button-1>', self.save_file)

        # Input image
        self.input_frame = tk.Frame(self.window, width=450, height=400)
        self.input_frame.grid(row=1, column=0, sticky="nsew")

        self.input_image_label = tk.Canvas(self.input_frame,
                                           borderwidth=2,
                                           relief="groove",
                                           height=400,
                                           width=450)
        self.input_image_label.pack(fill=tk.BOTH, expand=True)
        self.input_image_label.bind('<Button-1>', self.draw_polygon)
        self.input_image_label.bind('<Button-3>', self.draw_polygon)

        self.image_canvas = self.input_image_label.create_image(self.input_image_label.winfo_width()/10,
                                                                self.input_image_label.winfo_height()/10,
                                                                anchor=tk.NW)

        # Output image
        self.output_frame = tk.Frame(self.window, width=450, height=400)
        self.output_frame.grid(row=1, column=1, sticky="nsew")

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.output_image_label = tk.Label(self.output_frame,
                                           text='Output image',
                                           borderwidth=2,
                                           relief="groove")
        self.output_image_label.pack(fill=tk.BOTH, expand=True)

    def load_input_image(self, event):
        self.filename = fd.askopenfilename()
        pilimage = Image.open(self.filename).resize((self.input_image_label.winfo_width(),
                                                     self.input_image_label.winfo_height()))
        self.tkimage_input = ImageTk.PhotoImage(pilimage)
        self.input_image_label.itemconfig(self.image_canvas, image=self.tkimage_input)

    def do_inference(self, event):
        prompt = self.prompt_text.get()
        if self.polygon_closed:
            mask = Image.fromarray(self.make_mask_from_polygon())
        else:
            mask = None

        if prompt.isascii() and len(prompt):
            image = Image.open(self.filename).resize((self.output_frame.winfo_width(), self.output_image_label.winfo_height()))
            output = self.engine.run(image, prompt)[0].resize((self.output_frame.winfo_width(), self.output_image_label.winfo_height()))
            if mask is not None:
                self.final_image = Image.composite(image, output, mask)
            else:
                self.final_image = output
            self.tkimage_output = ImageTk.PhotoImage(self.final_image)
            self.output_image_label.config(image=self.tkimage_output)
        else:
            print('Prompt is not valid')

    def save_file(self, engine):
        file = fd.asksaveasfile(mode='w', defaultextension=".png")
        if file:
            self.final_image.save(file)

    def make_mask_from_polygon(self):
        img = Image.new('L', (self.output_frame.winfo_width(),  self.output_image_label.winfo_height()), 0)
        ImageDraw.Draw(img).polygon(self.polygon_coords, outline=255, fill=255)
        inverted_img = ImageOps.invert(img)
        mask = np.array(inverted_img)
        return mask

    def draw_polygon(self, event):
        if not self.polygon_closed:
            self.polygon_coords.append((event.x, event.y))
            first_point = self.polygon_coords[0]
            last_point = self.polygon_coords[-1]

            if len(self.polygon_coords) > 3 and euclidean_distance(first_point, last_point) < 8:
                self.polygon_coords.pop(-1)
                self.polygon_coords.append(first_point)
                self.polygon_closed = True

            if len(self.polygon_coords) > 1:
                self.input_image_label.create_line(*self.polygon_coords[-1], *self.polygon_coords[-2], tags='polygon')
        else:
            print("Polygon is closed, run inference or right-click with mouse to clear it.")

        if event.num == 3:
            self.rectangle = []
            self.input_image_label.delete('polygon')
            self.polygon_closed = False

    def run(self):
        self.window.mainloop()

    def close(self):
        self.window.quit()


if __name__ == "__main__":
    window = Window()
    window.run()