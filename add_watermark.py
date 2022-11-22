import os
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from collections.abc import Callable
from tkinter.filedialog import askopenfilename
from tk_ui_helper_functions import set_window_position

THEME_COLOR = "#375362"
DEFAULT_FONT = ("Ariel", 20, "normal")
MEDIUM_FONT = ("Ariel", 17, "italic")
SUCCESS_FONT = ("Ariel", 12, "normal")
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
BORDER_THICKNESS = 5
DEFAULT_TITLE = "Add Image Watermark"
DEFAULT_WINDOW_POSITION = "center"


class AddWatermark:
    abs = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, **kw):
        # BASE SET UP:
        self.win = tk.Tk()
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.title = DEFAULT_TITLE
        self.win_pos = kw["position"] if kw.get("position") else DEFAULT_WINDOW_POSITION
        self.pos = set_window_position(tk=self.win, width=self.width, height=self.height, position=self.win_pos)
        self.win.geometry(self.pos)
        self.win.title(self.title)
        self.win.config(bg=THEME_COLOR)
        self.win.resizable(False, False)
        # UI SET UP:
        self.head_height = self.height / 4 - (BORDER_THICKNESS / 2)
        self.content_height = (self.height / 4) * 3 - (BORDER_THICKNESS / 2)
        self.hr_height = BORDER_THICKNESS
        self.current_image_path = None
        self.images = {}
        self.success_label_text = ""
        self._set_frames()
        self._set_labels()
        self._set_buttons()
        self._set_entries()
        self._start_window(content=self._get_home_content)
        self.win.mainloop()

    # ------------------------- FUNCTIONALITY ------------------------- #

    def upload_img_handler(self):
        f_types = [("Jpg files", "*.jpg"), ("PNG files", "*.png")]
        filename = tk.filedialog.askopenfilename(filetypes=f_types)
        self.success_label_text = ""
        self.success_label.grid_forget()
        if filename:
            details = filename.split(".")
            name = details[0].split('/')[-1]
            file_type = details[1].lower()
            self.current_image_path = f"images/{name}_{random.randint(0,90)}_{random.randint(0,90)}.{file_type}"
            self.images[self.current_image_path] = os.path.join(self.abs, self.current_image_path)
            img = Image.open(filename)
            img = img.convert('RGB')
            img.save(self.images[self.current_image_path])
            img = Image.open(self.images[self.current_image_path])
            img = self._resize(img)
            self.upload_frame.grid_forget()
            self.edit_img_label.image = img
            self.edit_img_label['image'] = img
            self._start_window(content=self._get_uploaded_content)

    @staticmethod
    def _resize(img_to_resize):
        fixed_height = 200
        height_percentage = (fixed_height / float(img_to_resize.size[1]))
        width_size = int(float(img_to_resize.size[0]) * float(height_percentage))
        img_to_resize = img_to_resize.resize((width_size, fixed_height))
        return ImageTk.PhotoImage(img_to_resize)

    def add_watermark_handler(self):
        text = self.watermark_entry.get()
        if text.strip():
            img = Image.open(self.images[self.current_image_path])
            width, height = img.size
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("Verdana.ttf", 25)
            text_width, text_height = draw.textsize(text, font)
            margin = 10
            x = (width // 2) - (text_width // 2) - margin
            y = (height // 2) - text_height - margin
            draw.text((x, y), text, font=font)
            img.show()
            img.save(self.images[self.current_image_path])
            self.success_label_text = "Watermark Successfully Added."
            self.watermark_entry.delete(0, 'end')
            self.uploaded_frame.grid_forget()
            self._start_window(self._get_home_content)

    @staticmethod
    def on_enter(e):
        e.widget.config(highlightbackground='#3e8abc', fg='#111')

    @staticmethod
    def on_leave(e):
        e.widget.config(highlightbackground='yellow', fg='blue')

    def _start_window(self, content: Callable) -> None:
        # Page:
        self.head_frame.grid(row=0, column=0, columnspan=3)
        self.hr_frame_top.grid(row=1, column=0, columnspan=3)
        self.hr_frame_bottom.grid(row=3, column=0, columnspan=3)
        self.footer_frame.grid(row=4, column=0, columnspan=3)
        # Content:
        self.head_label_frame.grid(row=0, column=0, pady=20)
        self.head_label.grid(row=0, column=0, ipady=10, ipadx=20)
        self.home_content_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.home_content_frame.grid_rowconfigure(0, weight=1)
        self.home_content_frame.grid_columnconfigure(0, weight=1)
        content()

    def _get_home_content(self):
        self.upload_frame.grid(row=1, column=0, columnspan=3, sticky=tk.E+tk.W)
        self.upload_frame.grid_rowconfigure(0, weight=1)
        self.upload_frame.grid_columnconfigure(0, weight=1)
        self.upload_btn.grid(row=1, column=0, pady=200, ipadx=5, ipady=5)
        if self.success_label_text:
            self.success_label.config(text=self.success_label_text)
            self.success_label.grid(row=5, sticky="se", ipadx=5, ipady=5)

    def _get_uploaded_content(self):
        self.uploaded_frame.grid(row=1, pady=25)
        self.uploaded_frame.grid_rowconfigure(0, weight=1)
        self.uploaded_frame.grid_columnconfigure(0, weight=1)
        self.edit_img_label.grid(row=1, column=0, columnspan=2, pady=50)
        self.info_edit_label.grid(row=2, column=0, padx=10)
        self.watermark_entry.grid(row=2, column=1)
        self.add_wm_btn.grid(row=3, column=0, columnspan=2, pady=10, ipady=10, sticky=tk.E+tk.W)

    # ------------------------- TK UI ------------------------- #

    def _set_frames(self):
        self.head_frame = tk.Frame(self.win, bg=THEME_COLOR, width=self.width, height=self.head_height)
        self.head_label_frame = tk.Frame(self.head_frame, bg=THEME_COLOR)
        self.hr_frame_top = tk.Frame(self.win, bg="black", width=self.width, height=self.hr_height)
        self.home_content_frame = tk.Frame(self.win, bg="grey", width=self.width, height=self.height)
        self.upload_frame = tk.Frame(
            self.home_content_frame, bg="grey", width=self.width, height=self.content_height)
        self.uploaded_frame = tk.Frame(
            self.home_content_frame, bg="grey", height=self.content_height - (self.head_height / 2),
            width=self.width)
        self.hr_frame_bottom = tk.Frame(self.win, bg="black", width=self.width, height=self.hr_height)
        self.footer_frame = tk.Frame(self.win, bg=THEME_COLOR, width=self.width, height=50)

    def _set_labels(self) -> None:
        # CREATE:
        self.head_label = tk.Label(self.head_label_frame, text="Add Image Watermark", font=DEFAULT_FONT)
        self.edit_img_label = tk.Label(self.uploaded_frame)
        self.success_label = tk.Label(self.upload_frame, text="", bg="yellow", font=SUCCESS_FONT, fg="black", bd=4)
        self.info_edit_label = tk.Label(self.uploaded_frame, text="Enter watermark text:", font=MEDIUM_FONT)
        # CONFIGURE:
        self.head_label.config(bg=THEME_COLOR, fg="white", bd=4, relief=tk.RAISED)
        self.info_edit_label.config(bg="grey", fg="white", anchor="w")

    def _set_buttons(self) -> None:
        # CREATE:
        self.upload_btn = tk.Button(self.upload_frame, text="Upload Image", highlightbackground="yellow",
                                    fg="blue",
                                    command=self.upload_img_handler, width=20)
        self.add_wm_btn = tk.Button(self.uploaded_frame, text="Add Watermark", highlightbackground="yellow",
                                    fg="blue",
                                    command=self.add_watermark_handler, width=20)
        # CONFIGURE:
        self.upload_btn.bind("<Enter>", self.on_enter)
        self.upload_btn.bind("<Leave>", self.on_leave)
        self.add_wm_btn.bind("<Enter>", self.on_enter)
        self.add_wm_btn.bind("<Leave>", self.on_leave)

    def _set_entries(self) -> None:
        # CREATE:
        self.input_var = tk.StringVar()
        self.watermark_entry = tk.Entry(self.uploaded_frame, textvariable=self.input_var)
        # CONFIGURE:
        self.watermark_entry.focus()
