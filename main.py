import tkinter as tk


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
            side="top", fill="x", pady=10
        )
        tk.Button(
            self,
            text="Return to Home page",
            command=lambda: master.switch_frame(HomePage),
        ).pack()


if __name__ == "__main__":
    app = PekoApp()
    app.mainloop()
