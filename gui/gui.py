from ai.inference import StableDiffusion

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog as fd

class Window:

    def __init__(self):
        self.engine = StableDiffusion()

        self.window = tk.Tk()
        self.window.geometry("900x400")
        self.window.title('Marc Ortiz interview test')

        # Controls line 1
        self.control_frame_1 = tk.Frame(self.window)
        self.control_frame_1.grid(row=0, columnspan=2, pady=2)
        self.window.grid_columnconfigure(0, weight=1)

        self.prompt_text_description = tk.Label(self.control_frame_1, text='Prompt: ')
        self.prompt_text_description.pack(side=tk.LEFT)
        self.prompt_text = tk.Entry(self.control_frame_1)
        self.prompt_text.pack(side=tk.LEFT, expand=True)

        self.inference_button = tk.Button(self.control_frame_1, text='Run inference')
        self.inference_button.pack(side=tk.LEFT, expand=True)
        self.inference_button.bind('<Button-1>', self.do_inference)

        self.save_button = tk.Button(self.control_frame_1, text='Save image')
        self.save_button.pack(side=tk.LEFT)
        self.save_button.bind('<Button-1>', self.save_file)

        # Input image
        self.input_frame = tk.Frame(self.window, width=350, height=300)
        self.input_frame.grid(row=1, column=0, sticky="nsew")

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.input_image_label = tk.Label(self.input_frame,
                                          text='Click here to load an image',
                                          borderwidth=2,
                                          relief="groove")
        self.input_image_label.pack(fill=tk.BOTH, expand=True)
        self.input_image_label.bind('<Button-1>', self.load_input_image)

        # Output image
        self.output_frame = tk.Frame(self.window, width=350, height=300)
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
        pilimage = Image.open(self.filename)
        self.tkimage_input = ImageTk.PhotoImage(pilimage)
        self.input_image_label.config(image=self.tkimage_input)

    def do_inference(self, event):
        prompt = self.prompt_text.get()
        if prompt.isascii() and len(prompt):
            image = Image.open(self.filename)
            self.output = self.engine.run(image, prompt)[0]
            self.tkimage_output = ImageTk.PhotoImage(self.output)
            self.output_image_label.config(image=self.tkimage_output)
        else:
            print('Prompt is not valid')

    def save_file(self, engine):
        file = fd.asksaveasfile(mode='w', defaultextension=".png")
        if file:
            self.output.save(file)

    def run(self):
        self.window.mainloop()

    def close(self):
        self.window.quit()


if __name__ == "__main__":
    window = Window()
    window.run()