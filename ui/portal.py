# ui/portal.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
import os
import asyncio
import threading

# Local imports
from ui.pages.start_page import create_start_page
from ui.pages.group_page import create_group_page
from ui.pages.mentor_page import create_mentor_page
from utils.styles import configure_styles
from mentor_bot.db import create_tables

from api.api_call import get_messages
from api.config import client

class HRTeacherPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg='#3533cd')
        
        # Event loop management
        self.loop = None
        self.client_started = False
        
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
        
        # Start event loop in background thread
        self.start_event_loop()

    def start_event_loop(self):
        """Start asyncio event loop in a separate thread"""
        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()
        
        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()

    async def async_get_messages(self, group, username):
        """Async method to get messages with proper client management"""
        try:
            if not self.client_started:
                await client.start()
                self.client_started = True
                
            result = await get_messages(group, username)
            return result
        except Exception as e:
            # If there's an error, reset client state
            self.client_started = False
            try:
                await client.disconnect()
            except:
                pass
            raise e

    def run_fetch_data(self, group_url, username):
        """Run the fetch data function with proper async handling"""
        try:
            # Run the async function in the event loop thread
            future = asyncio.run_coroutine_threadsafe(
                self.async_get_messages(group_url, username), 
                self.loop
            )
            result = future.result(timeout=300)  # 5 minute timeout
            return result
        except Exception as e:
            # Reset client state on error
            self.client_started = False
            # Try to disconnect in the event loop
            if self.loop and self.loop.is_running():
                disconnect_future = asyncio.run_coroutine_threadsafe(
                    self.safe_disconnect(), 
                    self.loop
                )
                try:
                    disconnect_future.result(timeout=10)
                except:
                    pass
            raise e

    async def safe_disconnect(self):
        """Safely disconnect the client"""
        try:
            await client.disconnect()
            self.client_started = False
        except:
            pass

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

    def group_selected(self, group_display_name):
        """Handle group selection - group_display_name is the display name"""
        print(f"Group selected (display): {group_display_name}")
        print(f"Group link (actual): {self.selected_group}")
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
        
    def cleanup(self):
        """Cleanup resources when app closes"""
        if self.loop and self.loop.is_running():
            # Schedule disconnect and stop loop
            if self.client_started:
                asyncio.run_coroutine_threadsafe(
                    self.safe_disconnect(), 
                    self.loop
                )
            self.loop.call_soon_threadsafe(self.loop.stop)