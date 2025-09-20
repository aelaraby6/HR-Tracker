# Handles main app setup and switching between pages.
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from ui.pages.start_page import create_start_page
from ui.pages.group_page import create_group_page
from ui.pages.mentor_page import create_mentor_page
from utils.styles import configure_styles


class HRTeacherPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg='#3533cd')

        # Configure styles
        self.style = ttk.Style()
        configure_styles(self.style)

        # Colors
        self.primary_color = '#3533cd'
        self.secondary_color = '#4543dd'
        self.accent_color = '#2523bd'
        self.light_accent = '#6563ed'
        self.background_color = '#3533cd'
        self.text_color = 'white'

        # Logo
        self.logo_img = None
        try:
            self.logo_img = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((80, 80)))
        except:
            print("Logo image not found. Using placeholder.")

        # Create pages
        self.start_frame = create_start_page(self)
        self.group_frame = create_group_page(self)
        self.mentor_frame = create_mentor_page(self)

        # Show start page
        self.show_page("start")

    def show_page(self, page_name):
        # Hide all pages
        self.start_frame.pack_forget()
        self.group_frame.pack_forget()
        self.mentor_frame.pack_forget()

        if page_name == "start":
            self.start_frame.pack(fill='both', expand=True)
        elif page_name == "group":
            self.group_frame.pack(fill='both', expand=True)
        elif page_name == "mentor":
            self.mentor_frame.pack(fill='both', expand=True)

    def group_selected(self, group):
        messagebox.showinfo("Group Selected", f"You selected: {group}")
        self.selected_group = group
        self.show_page("mentor")

    def mentor_selected(self, mentor):
        messagebox.showinfo("Mentor Selected", f"You selected: {mentor}")
        self.selected_mentor = mentor
        

