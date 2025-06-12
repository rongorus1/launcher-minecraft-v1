from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

from components.button_delete_profile import ButtonDeleteProfile
from components.button_save_profile import ButtonSaveProfile
from services.profile_service import load_profiles, save_profiles
from services.settings_service import save_settings, load_settings


class SessionConfigurationWindow(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Configuración de RAM para Minecraft")
        self.geometry("400x400")
        self.attributes('-topmost', True)

        profiles = load_profiles()

        ctk.CTkLabel(self, text="Profile Management", font=("Arial", 20)).pack(pady=10)

        # Dropdown menu for existing profiles
        profile_names = [p['username'] for p in profiles['profiles']]
        selected_profile = ctk.StringVar(value=profile_names[0] if profile_names else "New Profile")
        ctk.CTkLabel(self, text="Select a Profile:").pack(pady=5)
        profile_dropdown = ctk.CTkOptionMenu(self, variable=selected_profile,
                                             values=profile_names + ["New Profile"])
        profile_dropdown.pack(pady=5, padx=20)

        # Username Entry
        username_entry = ctk.CTkEntry(self, placeholder_text="Enter username (for new profile)")
        username_entry.pack(pady=5, padx=20)

        def save_profile():
            selected = selected_profile.get()
            if selected == "New Profile":
                username = username_entry.get().strip()
                if not username:
                    messagebox.showwarning("Warning", "Username cannot be empty")
                    return
            else:
                username = selected

            # Check if profile already exists
            existing_profile = next((p for p in profiles['profiles'] if p['username'] == username), None)

            if existing_profile:
                # Update existing profile
                existing_profile['last_login'] = datetime.now().isoformat()
            else:
                # Create new profile
                new_profile = {
                    'username': username,
                    'last_login': datetime.now().isoformat()
                }
                profiles['profiles'].append(new_profile)

            # Save profiles
            save_profiles(profiles)

            # Update settings with last profile
            settings = load_settings()
            settings['last_profile'] = username
            save_settings(settings)

            messagebox.showinfo("Success", f"Profile saved for {username}")
            self.destroy()

        def delete_profile():
            selected = selected_profile.get()
            if selected == "New Profile":
                messagebox.showwarning("Warning", "Cannot delete 'New Profile'.")
                return

            # Remove selected profile
            profiles['profiles'] = [p for p in profiles['profiles'] if p['username'] != selected]
            save_profiles(profiles)

            # Update settings if the deleted profile was the last used
            settings = load_settings()
            if settings.get('last_profile') == selected:
                settings['last_profile'] = None
            save_settings(settings)

            messagebox.showinfo("Success", f"Profile '{selected}' deleted.")
            self.destroy()
            from controller.start_session_controller import run_session_controller
            run_session_controller()  # Reopen the login window to refresh the list

        button_save_profile = ButtonSaveProfile(self, save_profile)
        button_delete_profile = ButtonDeleteProfile(self, delete_profile)

        # Profile List
        ctk.CTkLabel(self, text="Existing Profiles:").pack(pady=5)
        profile_listbox = ctk.CTkTextbox(self, height=100, width=300)
        profile_listbox.pack(pady=5)

        # Populate profile list
        profile_text = "\n".join(
            [f"{p['username']} (Last Login: {p.get('last_login', 'Never')})" for p in profiles.get('profiles', [])])
        profile_listbox.insert("0.0", profile_text or "No profiles saved")
        profile_listbox.configure(state="disabled")