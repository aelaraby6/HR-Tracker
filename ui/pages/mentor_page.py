import tkinter as tk
from tkinter import ttk

def create_mentor_page(app):
    frame = tk.Frame(app.root, bg=app.background_color)

    header = tk.Frame(frame, bg=app.primary_color, height=120)
    header.pack(fill='x', pady=(0, 40))

    if app.logo_img:
        logo_label = tk.Label(header, image=app.logo_img, bg=app.primary_color)
        logo_label.place(x=20, y=10)

    title = ttk.Label(header, text="HR Teacher", style='Title.TLabel')
    title.pack(pady=(20, 5))

    subtitle = ttk.Label(header, text="Please Select Mentor ID", style='Header.TLabel')
    subtitle.pack(pady=(0, 20))

    mentors = [
        "Mentor #001 - Ahmed Ali",
        "Mentor #002 - Mohamed Hassan",
        "Mentor #003 - Sara Mahmoud",
        "Mentor #004 - Rana Elsayed",
        "Mentor #005 - Omar Ibrahim",
        "Mentor #006 - Hana Mohamed",
        "Mentor #007 - Khaled Farouk",
        "Mentor #008 - Amira Taha"
    ]

    content = tk.Frame(frame, bg=app.background_color)
    content.pack(expand=True, fill='both')

    mentor_buttons = tk.Frame(content, bg=app.background_color)
    mentor_buttons.pack(pady=20)

    left_frame = tk.Frame(mentor_buttons, bg=app.background_color)
    left_frame.pack(side='left', padx=20)

    right_frame = tk.Frame(mentor_buttons, bg=app.background_color)
    right_frame.pack(side='right', padx=20)

    for i, mentor in enumerate(mentors):
        frame_target = left_frame if i < 4 else right_frame
        btn = ttk.Button(frame_target, text=mentor, style='Mentor.TButton', command=lambda m=mentor: app.mentor_selected(m))
        btn.pack(pady=10)

    nav_frame = tk.Frame(content, bg=app.background_color)
    nav_frame.pack(side='bottom', pady=20)

    back_btn = ttk.Button(nav_frame, text="Back", style='Button.TButton', command=lambda: app.show_page("group"))
    back_btn.pack(padx=20)

    footer = tk.Frame(frame, bg=app.accent_color, height=50)
    footer.pack(side='bottom', fill='x')
    footer_text = ttk.Label(footer, text="ICPC Zagazig University", background=app.accent_color, foreground='white')
    footer_text.pack(pady=15)

    return frame
