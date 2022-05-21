import tkinter as tk
from tkinter import Text, Canvas
from tkinter import filedialog
from PIL import Image, ImageTk


class PekoApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page").pack(
            side="top", fill="x", pady=10
        )
        self.uni_logo = Image.open("images/ala-too_logo.jpeg")
        self.uni_logo = ImageTk.PhotoImage(image=self.uni_logo)
        tk.Label(
            self,
            image=self.uni_logo,
        ).pack()
        tk.Button(
            self,
            text="Open page one",
            command=lambda: master.switch_frame(PageOne),
        ).pack()
        tk.Button(
            self,
            text="glasses filter",
            command=lambda: master.switch_frame(GlassFilterPage),
        ).pack()
        tk.Button(
            self,
            text="Copyright",
            command=lambda: master.switch_frame(CopyRightPage),
        ).pack()


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(
            side="top", fill="x", pady=10
        )
        tk.Button(
            self,
            text="Return to start page",
            command=lambda: master.switch_frame(HomePage),
        ).pack()


class GlassFilterPage(tk.Frame):
    """
    Applies shapchat glass filter to the given image
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Snapchat glasses filter").pack(
            side="top", fill="x", pady=20
        )
        self.configure()
        tk.Button(
            self,
            text="Return to Home page",
            command=lambda: master.switch_frame(HomePage),
        ).pack()

    def configure(self):
        self.canvas = Canvas(self, width=650, height=350)
        self.canvas.pack()

        self.open_image_button = tk.Button(
            self,
            text="open image",
            command=self.open_image_and_display_in_canvas,
        ).pack()

    def open_image_and_display_in_canvas(self):
        path = filedialog.askopenfilename()

        print(path)

        if path:
            self.image = Image.open(path)
            self.image = self.image.resize((500, 490), Image.LANCZOS)
            self.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.image, anchor="nw")

class CopyRightPage(tk.Frame):
    """
    Peko app copyright page.
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Copyright Page").pack(
            side="top", fill="x", pady=10
        )
        # copy text area
        text_box = Text(self, height=12, width=45)
        text_box.pack(expand=True)
        text_box.insert("end", self.copyright)
        # text_box.config(state="disabled")
        tk.Button(
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
