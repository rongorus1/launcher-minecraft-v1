from customtkinter import CTkProgressBar

class ProgressBarGeneric(CTkProgressBar):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.is_hidden = True
        self.set(0)
        self.configure(
            fg_color = ("black", "black"),
            width=1200
        )

    def show_element(self):
        self.place(
            relx=0.5,
            rely=0.00,
            anchor="center"
        )
        self.is_hidden = False

    def hidde_element(self):
        self.place_forget()
        self.is_hidden = True