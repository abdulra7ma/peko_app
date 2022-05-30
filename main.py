from re import L
import tkinter as tk
from tkinter import Canvas, Text, filedialog, messagebox
from tkinter.filedialog import asksaveasfile

import customtkinter as ctk
from PIL import Image, ImageTk, UnidentifiedImageError
from PIL.ExifTags import TAGS

from image_processor import black_and_white, image_meta_data_extractor

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme(
    "green"
)  # Themes: blue (default), dark-blue, green


class PekoApp(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        ctk.CTk.geometry(self, "650x610")
        ctk.CTk.minsize(self, width=650, height=560)
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        """
        Destroys current frame and replaces it with a new one.
        """

        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        ctk.CTkLabel(
            self, text="Peko app", text_font=("Bahnschrift", 28)
        ).pack(padx=5, pady=15, side=tk.TOP)
        self.uni_logo = Image.open("images/ala-too_logo.jpeg")
        self.uni_logo = ImageTk.PhotoImage(image=self.uni_logo)
        ctk.CTkLabel(
            self,
            image=self.uni_logo,
        ).pack(padx=5, pady=15, side=tk.TOP)
        ctk.CTkButton(
            self,
            text="Image Meta extactor",
            command=lambda: master.switch_frame(PageOne),
        ).pack(padx=5, pady=15, side=tk.TOP)
        ctk.CTkButton(
            self,
            text="glasses filter",
            command=lambda: master.switch_frame(GlassFilterPage),
        ).pack(padx=5, pady=15, side=tk.TOP)
        ctk.CTkButton(
            self,
            text="black&white filter",
            command=lambda: master.switch_frame(BlackAndWhitePage),
        ).pack(padx=5, pady=15, side=tk.TOP)

        ctk.CTkButton(
            self,
            text="Copyright",
            command=lambda: master.switch_frame(CopyRightPage),
        ).pack(padx=5, pady=15, side=tk.BOTTOM)


class PageOne(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        ctk.CTkLabel(
            self, text="Image Meta Extractor", text_font=("Bahnschrift", 28)
        ).pack(side="top", fill="x", pady=10)
        self.canvas_configure()
        ctk.CTkButton(
            self, text="Select image", command=self._open_image
        ).pack(padx=50, pady=10, side=tk.TOP)
        ctk.CTkButton(
            self, text="Download image data", command=self._save_file
        ).pack(padx=50, pady=10, side=tk.TOP)
        ctk.CTkButton(
            self,
            text="Return to start page",
            command=lambda: master.switch_frame(HomePage),
        ).pack(padx=50, pady=10, side=tk.TOP)

    def canvas_configure(self) -> None:
        self.canvas = Canvas(self, width=650, height=350)
        self.canvas.pack(padx=5, pady=10, side=tk.TOP)

    def draw_meta_info(self, meta_dict: dict) -> None:
        x = 250
        y = 60
        for k, v in meta_dict.items():
            self.canvas.create_text(
                x,
                y,
                text=k + " >>>  " + str(v) + "\n",
                font=("Helvetica 15 bold"),
            )
            y += 30

    def _open_image(self):
        self.path = filedialog.askopenfilename()

        if self.path:
            try:
                self.image = Image.open(self.path)
                self.image_meta_data = image_meta_data_extractor(self.image)
                self.draw_meta_info(self.image_meta_data)
            except UnidentifiedImageError:
                messagebox.showerror(
                    "Image Not Identified",
                    "Sorry, we can not identify the image format. Please open another one",
                )

    def _save_file(self):
        allowed_files = [
            ("Text Document", "*.txt"),
        ]
        if not self.image:
            messagebox.showerror("Alrt", "Selet an image first")
        else:
            file = asksaveasfile(
                filetypes=allowed_files, defaultextension=allowed_files
            )

            for k, v in self.image_meta_data.items():
                try:
                    file.write(k + " >>> " + str(v) + "\n")
                except AttributeError:
                    pass

            file.close()


class FliterPageBase(ctk.CTkFrame):
    """
    Fliter Page Base class that implements basic functionality
    """

    MAX_SIZE = (650, 350)

    def __init__(self, master, frame_label="Peko Frame"):
        ctk.CTkFrame.__init__(self, master)
        ctk.CTkLabel(
            self, text=frame_label, text_font=("Bahnschrift", 28)
        ).pack(side="top", fill="x", pady=20)
        self.configure()
        ctk.CTkButton(
            self,
            text="Return to Home page",
            command=lambda: master.switch_frame(HomePage),
        ).pack()
        self.image = None
        self.filtered_image = None

    def configure(self):
        self.canvas = Canvas(self, width=650, height=350)
        self.canvas.pack(padx=5, pady=10, side=tk.TOP)

        self.open_image_button = ctk.CTkButton(
            self,
            text="open image",
            command=self.open_image_and_display_in_canvas,
        ).pack(padx=5, pady=10, side=tk.TOP)
        self.apply_filter_button = ctk.CTkButton(
            self,
            text="apply filter",
            command=self.apply_filter,
        ).pack(padx=50, pady=10, side=tk.TOP)

    def open_image_and_display_in_canvas(self):
        self.path = filedialog.askopenfilename()

        if self.path:
            self.image = Image.open(self.path)
            self.image.thumbnail(self.MAX_SIZE)
            self.set_canvas_photo(self.image)

    def set_canvas_photo(self, image):
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(
            self.tk_image.width() / 2,
            self.tk_image.height() / 2,
            image=self.tk_image,
            anchor=tk.CENTER,
        )

    def update_canvas_photo(self, image):
        w, h = image.size

        # if the image exceeds the max size
        # than we gonna resize it
        if w > self.MAX_SIZE[0] or h > self.MAX_SIZE[1]:
            image.thumbnail(self.MAX_SIZE)

        self.set_canvas_photo(image)

    def apply_filter(self):
        """
        This method must be overwritten
        """
        if not self.image:
            self.raise_alert_message()

        raise NotImplementedError("Overwrite this function on your class")

    def raise_alert_message(self, msg=None):
        msg = msg if msg is not None else "Please open image first."
        messagebox.showerror("Alrt", msg)


class GlassFilterPage(FliterPageBase):
    """
    Applies shapchat glass filter to the given image
    """

    def apply_filter(self):
        from image_processor import glasses_filter

        if not self.image:
            self.raise_alert_message()
        else:
            self.filter_image = glasses_filter(self.image)
            self.update_canvas_photo(self.filtered_image)


class BlackAndWhitePage(FliterPageBase):
    """
    Applies black & white filter to the given image
    """

    def __init__(self, master, frame_label="Peko Frame"):
        super().__init__(master, "Black & White")

    def apply_filter(self):
        if not self.image:
            self.raise_alert_message()
        else:
            self.filtered_image = black_and_white(self.image)
            self.update_canvas_photo(self.filtered_image)


class CopyRightPage(ctk.CTkFrame):
    """
    Peko app copyright page.
    """

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        ctk.CTkLabel(self, text="Copyright Page").pack(
            side="top", fill="x", pady=10
        )
        # copy text area
        text_box = Text(self, height=12, width=45)
        text_box.pack(expand=True)
        text_box.insert("end", self.copyright)
        ctk.CTkButton(
            self,
            text="Return to Home page",
            command=lambda: master.switch_frame(HomePage),
        ).pack()

    @property
    def copyright(self):
        copyright_symbol = "\u00A9"

        return f"""
        {copyright_symbol} Dear Reader,
        Thank you for giving your
        Love and Support to PythonGuides.
        PythonGuides is now available on 
        YouTube with the same name.

        Thanks & Regards,
        Team PythonGuides
        """


if __name__ == "__main__":
    app = PekoApp()
    app.mainloop()
