import tkinter as tk
from tkinter import ttk

def create_start_page(app):
    frame = tk.Frame(app.root, bg=app.background_color)

    # Header
    header = tk.Frame(frame, bg=app.primary_color, height=120)
    header.pack(fill='x', pady=(0, 40))

    if app.logo_img:
        logo_label = tk.Label(header, image=app.logo_img, bg=app.primary_color)
        logo_label.place(x=20, y=10)

    title = ttk.Label(header, text="HR Teacher", style='Title.TLabel')
    title.pack(pady=(20, 5))

    subtitle = ttk.Label(header, text="ICPC ZAGAZIG COMMUNITY", style='Header.TLabel')
    subtitle.pack(pady=(0, 20))

    # Content
    content = tk.Frame(frame, bg=app.background_color)
    content.pack(expand=True, fill='both')

    welcome_text = ttk.Label(content, text="Welcome to ICPC Zagazig University", style='Header.TLabel')
    welcome_text.pack(pady=(0, 40))

    logo_canvas = tk.Canvas(content, width=140, height=140, bg=app.background_color, highlightthickness=0)
    logo_canvas.pack(pady=(0, 40))
    logo_canvas.create_oval(10, 10, 130, 130, fill='white', outline=app.accent_color, width=3)
    logo_canvas.create_text(70, 70, text="ICPC", fill=app.primary_color, font=('Arial', 18, 'bold'))

    start_btn = ttk.Button(content, text="Start", style='Button.TButton', command=lambda: app.show_page("group"))
    start_btn.pack(pady=20)

    # Footer
    footer = tk.Frame(frame, bg=app.accent_color, height=50)
    footer.pack(side='bottom', fill='x', pady=(20, 0))
    footer_text = ttk.Label(footer, text="ICPC Zagazig University", background=app.accent_color, foreground='white')
    footer_text.pack(pady=15)

    return frame
