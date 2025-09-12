import tkinter as tk
from tkinter import ttk

def create_group_page(app):
    frame = tk.Frame(app.root, bg=app.background_color)

    header = tk.Frame(frame, bg=app.primary_color, height=120)
    header.pack(fill='x', pady=(0, 40))

    if app.logo_img:
        logo_label = tk.Label(header, image=app.logo_img, bg=app.primary_color)
        logo_label.place(x=20, y=10)

    title = ttk.Label(header, text="HR Teacher", style='Title.TLabel')
    title.pack(pady=(20, 5))

    subtitle = ttk.Label(header, text="Please Select a Group", style='Header.TLabel')
    subtitle.pack(pady=(0, 20))

    groups = [
        "HR Team",
        "ICPC ZAGAZIG COMMUNITY",
        "Technical Team",
        "Level 0 Training",
        "Level 1 Training"
    ]

    content = tk.Frame(frame, bg=app.background_color)
    content.pack(expand=True, fill='both')

    group_buttons = tk.Frame(content, bg=app.background_color)
    group_buttons.pack(pady=20)

    for group in groups:
        btn = ttk.Button(group_buttons, text=group, style='Group.TButton', command=lambda g=group: app.group_selected(g))
        btn.pack(pady=10)

    nav_frame = tk.Frame(content, bg=app.background_color)
    nav_frame.pack(side='bottom', pady=20)

    back_btn = ttk.Button(nav_frame, text="Back", style='Button.TButton', command=lambda: app.show_page("start"))
    back_btn.pack(side='left', padx=20)

    next_btn = ttk.Button(nav_frame, text="Next", style='Button.TButton', command=lambda: app.show_page("mentor"))
    next_btn.pack(side='right', padx=20)

    footer = tk.Frame(frame, bg=app.accent_color, height=50)
    footer.pack(side='bottom', fill='x')
    footer_text = ttk.Label(footer, text="ICPC Zagazig University", background=app.accent_color, foreground='white')
    footer_text.pack(pady=15)

    return frame
