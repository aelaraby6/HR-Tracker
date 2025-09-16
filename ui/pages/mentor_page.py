import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter

def create_gradient_button(width, height, color1, color2, radius=40):
    """Create rounded rectangle button with gradient and shadow"""
    img = Image.new("RGBA", (width + 10, height + 10), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (width + 10, height + 10), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)

    # Shadow
    draw_shadow.rounded_rectangle(
        [(5, 5), (width, height)],
        radius=radius,
        fill=(0, 0, 0, 100)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    img.paste(shadow, (0, 0), shadow)

    # Gradient
    gradient = Image.new("RGB", (width, height), color1)
    top = Image.new("RGB", (width, height), color2)
    mask = Image.new("L", (width, height))
    mask_data = []
    for x in range(width):
        mask_data.extend([int(255 * (x / width))] * height)
    mask.putdata(mask_data)
    gradient.paste(top, (0, 0), mask)

    # Rounded mask
    mask_round = Image.new("L", (width, height), 0)
    draw_mask = ImageDraw.Draw(mask_round)
    draw_mask.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=255)

    gradient.putalpha(mask_round)
    img.paste(gradient, (5, 0), gradient)

    return img


def create_mentor_page(app):
    frame = tk.Frame(app.root, bg="#0b0b23")

    # Title
    title = tk.Label(
        frame,
        text="Select a Mentor",
        font=("Archivo Black", 40, "bold"),
        fg="#a9c7ff",
        bg="#0b0b23"
    )
    title.pack(pady=20)

    # Example mentors
    mentors = ["Ahmed", "Mona", "Sara", "Omar"]
    buttons = []

    button_frame = tk.Frame(frame, bg="#0b0b23")
    button_frame.pack(pady=20)

    for mentor in mentors:
        btn = tk.Label(button_frame, bd=0, bg="#0b0b23", cursor="hand2")
        btn.pack(pady=10)

        def make_handler(m=mentor):
            return lambda e: app.mentor_selected(m)

        btn.bind("<Button-1>", make_handler())
        buttons.append((btn, mentor))

    # Navigation buttons container (Back + Home in one row)
    nav_frame = tk.Frame(frame, bg="#0b0b23")
    nav_frame.pack(pady=20)

    back_btn = tk.Label(nav_frame, bd=0, bg="#0b0b23", cursor="hand2")
    back_btn.pack(side="left", padx=10)

    def back_to_groups(event):
        app.show_page("group")

    back_btn.bind("<Button-1>", back_to_groups)

    home_btn = tk.Label(nav_frame, bd=0, bg="#0b0b23", cursor="hand2")
    home_btn.pack(side="left", padx=10)

    def go_home(event):
        app.show_page("start")

    home_btn.bind("<Button-1>", go_home)

    # Logo placeholder
    logo_label = tk.Label(frame, bg="#0b0b23")
    logo_label.place(relx=1.0, anchor="ne")

    try:
        logo_img_orig = Image.open("assets/logo.png")
    except Exception as e:
        print("Logo not found:", e)
        logo_img_orig = None

    def resize_elements(event):
        w, h = event.width, event.height

        # Title resize
        title_font_size = max(20, w // 20)
        title.configure(font=("Archivo Black", title_font_size, "bold"))

        # Mentor buttons
        btn_w = int(w * 0.35)
        btn_h = int(h * 0.1)

        for btn, mentor in buttons:
            btn_img = create_gradient_button(btn_w, btn_h, "#a9c7ff", "#4A7BFF")
            btn_imgtk = ImageTk.PhotoImage(btn_img)

            btn.configure(
                image=btn_imgtk,
                text=mentor,
                font=("Archivo Black", max(14, btn_h // 4), "bold"),
                compound="center",
                fg="black"
            )
            btn.image = btn_imgtk

        # Back button resize
        nav_btn_w = int(w * 0.25)
        nav_btn_h = int(h * 0.08)

        back_img = create_gradient_button(nav_btn_w, nav_btn_h, "#0040AA", "#2E2EFF")
        back_imgtk = ImageTk.PhotoImage(back_img)

        back_btn.configure(
            image=back_imgtk,
            text="Back",
            font=("Archivo Black", max(14, nav_btn_h // 3), "bold"),
            compound="center",
            fg="white"
        )
        back_btn.image = back_imgtk

        # Home button resize
        home_img = create_gradient_button(nav_btn_w, nav_btn_h, "#4A7BFF", "#a9c7ff")
        home_imgtk = ImageTk.PhotoImage(home_img)

        home_btn.configure(
            image=home_imgtk,
            text="Home",
            font=("Archivo Black", max(14, nav_btn_h // 3), "bold"),
            compound="center",
            fg="black"
        )
        home_btn.image = home_imgtk

        # Logo resize
        if logo_img_orig:
            logo_size = int(min(w, h) * 0.15)
            logo_resized = logo_img_orig.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            logo_imgtk = ImageTk.PhotoImage(logo_resized)
            logo_label.configure(image=logo_imgtk)
            logo_label.image = logo_imgtk
            logo_label.place(relx=1.0, x=-w // 50, y=h // 40, anchor="ne")

    frame.bind("<Configure>", resize_elements)

    return frame
