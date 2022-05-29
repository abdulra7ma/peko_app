import tkinter as tk
from tkinter import Canvas, Text, filedialog, messagebox

import customtkinter as ctk
from PIL import Image, ImageTk
from image_processor import black_and_white

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
            text="Open page one",
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
            self, text="This is page one", text_font=("Bahnschrift", 28)
        ).pack(side="top", fill="x", pady=10)
        ctk.CTkButton(
            self,
            text="Return to start page",
            command=lambda: master.switch_frame(HomePage),
        ).pack()


class GlassFilterPage(ctk.CTkFrame):
    """
    Applies shapchat glass filter to the given image
    """

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        ctk.CTkLabel(
            self, text="Snapchat glasses filter", text_font=("Bahnschrift", 28)
        ).pack(side=tk.TOP, fill="x", pady=20)
        self.configure()
        ctk.CTkButton(
            self,
            text="Return to Home page",
            command=lambda: master.switch_frame(HomePage),
        ).pack(padx=5, pady=15, side=tk.BOTTOM)
        self.image = None
        self.filter_image = None

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
            command=self.apply_snapchap_filter,
        ).pack(padx=50, pady=10, side=tk.TOP)

    def open_image_and_display_in_canvas(self):
        MAX_SIZE = (590, 350)
        self.path = filedialog.askopenfilename()

        if self.path:
            self.image = Image.open(self.path)
            self.image.thumbnail(MAX_SIZE)
            self.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(
                self.image.width() / 2,
                self.image.height() / 2,
                image=self.image,
                anchor=tk.CENTER,
            )

    def apply_snapchap_filter(self):
        from image_processor import glasses_filter

        if not self.image:
            messagebox.showerror("Alrt", "Please open image first.")
        else:
            self.filter_image = glasses_filter(self.path)


class BlackAndWhitePage(ctk.CTkFrame):
    """
    Applies black & white filter to the given image
    """

    MAX_SIZE = (650, 350)

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        ctk.CTkLabel(self, text="Black & White filter").pack(
            side="top", fill="x", pady=20
        )
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
        self.canvas.pack()

        self.open_image_button = ctk.CTkButton(
            self,
            text="open image",
            command=self.open_image_and_display_in_canvas,
        ).pack()
        self.apply_filter_button = ctk.CTkButton(
            self,
            text="apply filter",
            command=self.apply_filter,
        ).pack()

    def open_image_and_display_in_canvas(self):
        self.path = filedialog.askopenfilename()

        if self.path:
            self.image = Image.open(self.path)
            self.image.thumbnail(self.MAX_SIZE)
            self.set_canvas_photo(self.image)

    def set_canvas_photo(self, image):
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 1, image=self.tk_image, anchor="nw")

    def update_canvas_photo(self, image):
        w, h = image.size

        # if the image exceeds the max size
        # than we gonna resize it
        if w > self.MAX_SIZE[0] or h > self.MAX_SIZE[1]:
            image.thumbnail(self.MAX_SIZE)

        self.set_canvas_photo(image)

    def apply_filter(self):
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
