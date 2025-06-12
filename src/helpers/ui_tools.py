import customtkinter as ctk

def configurer_button(button: ctk.CTkButton):
    button.configure(
        fg_color="black",
        text_color="white",
        font=("Arial", 12, "bold"),
        border_width=1,
        border_color="white"
    )
