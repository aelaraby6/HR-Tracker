from api.api_call import get_messages
from api.config import client
import asyncio
import tkinter as tk
from ui.portal import HRTeacherPortal

if __name__ == "__main__":
    root = tk.Tk()
    app = HRTeacherPortal(root)
    
    # Handle proper cleanup when window closes
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()