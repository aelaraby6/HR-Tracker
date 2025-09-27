# ui/portal.py
# Handles main app setup and switching between pages.
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
import os

# Local imports (relative for package safety)
from ui.pages.start_page import create_start_page
from ui.pages.group_page import create_group_page
from ui.pages.mentor_page import create_mentor_page
from utils.styles import configure_styles
from mentor_bot.db import create_tables

import asyncio
from api.api_call import get_messages
from api.config import client



class HRTeacherPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg='#3533cd')

        # Initialize database tables
        try:
            create_tables()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Database initialization error: {e}")

        # Configure styles
        self.style = ttk.Style()
        try:
            configure_styles(self.style)
        except Exception as e:
            print(f"Style configuration error: {e}")

        # Colors
        self.primary_color = '#3533cd'
        self.secondary_color = '#4543dd'
        self.accent_color = '#2523bd'
        self.light_accent = '#6563ed'
        self.background_color = '#3533cd'
        self.text_color = 'white'

        # Store selected group and mentor
        self.selected_group = None
        self.selected_mentor = None

        # ---------- Logo for Title Bar ----------
        png_path = "assets/logo.png"
        ico_path = "assets/logo.ico"

        try:
            if not os.path.exists(ico_path) and os.path.exists(png_path):
                img = Image.open(png_path)
                img.save(ico_path, format="ICO")
                print("ICO file created from PNG")

            if os.path.exists(ico_path):
                self.root.iconbitmap(ico_path)
            else:
                print("Logo files not found, using default icon")
        except Exception as e:
            print("Logo icon error:", e)
        # ----------------------------------------

        # Create pages with error handling
        try:
            self.start_frame = create_start_page(self)
            self.group_frame = create_group_page(self)
            self.mentor_frame = create_mentor_page(self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create pages: {e}")
            return

        # Show start page
        self.show_page("start")

    def show_page(self, page_name):
        """Switch between different pages"""
        for frame in [self.start_frame, self.group_frame, self.mentor_frame]:
            if frame and frame.winfo_exists():
                frame.pack_forget()

        if page_name == "start" and self.start_frame:
            self.start_frame.pack(fill='both', expand=True)
        elif page_name == "group" and self.group_frame:
            self.group_frame.pack(fill='both', expand=True)
        elif page_name == "mentor" and self.mentor_frame:
            self.mentor_frame.pack(fill='both', expand=True)
        else:
            print(f"Unknown page: {page_name}")

    def group_selected(self, group):
        """Handle group selection"""
        print(f"Group selected: {group}")
        self.selected_group = group
        self.show_page("mentor")

    def mentor_selected(self, mentor):
        """Handle mentor selection"""
        print(f"Mentor selected: {mentor}")
        self.selected_mentor = mentor

    
        

    def refresh_mentor_page(self):
        """Refresh mentor page when navigating back"""
        try:
            if hasattr(self, 'mentor_frame') and self.mentor_frame.winfo_exists():
                self.mentor_frame.destroy()
            self.mentor_frame = create_mentor_page(self)
        except Exception as e:
            print(f"Error refreshing mentor page: {e}")

    def go_back(self):
        """Navigate back to previous page"""
        if self.selected_group and hasattr(self, 'mentor_frame'):
            self.show_page("group")
        else:
            self.show_page("start")

    def go_home(self):
        """Navigate to home page"""
        self.selected_group = None
        self.selected_mentor = None
        self.show_page("start")
