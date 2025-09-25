import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter


def create_gradient_button(width, height, color1, color2, radius=40):
    """Create rounded rectangle button with gradient and shadow"""
    img = Image.new("RGBA", (width + 10, height + 10), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (width + 10, height + 10), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)

    # Shadow
    draw_shadow.rounded_rectangle(
        [(5, 5), (width + 5, height + 5)],  # Fixed coordinates
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
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (x / width)))
    mask.putdata(mask_data)
    gradient.paste(top, (0, 0), mask)

    # Rounded mask
    mask_round = Image.new("L", (width, height), 0)
    draw_mask = ImageDraw.Draw(mask_round)
    draw_mask.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=255)

    gradient.putalpha(mask_round)
    img.paste(gradient, (5, 5), gradient)  # Fixed positioning

    return img


def create_group_page(app):
    frame = tk.Frame(app.root, bg="#0b0b23")

    # Title
    title = tk.Label(
        frame,
        text="HR Tracker",
        font=("Archivo Black", 40, "bold"),
        fg="#a9c7ff",
        bg="#0b0b23"
    )
    title.pack(pady=(50, 20))

    # Subtitle
    subtitle = tk.Label(
        frame,
        text="Please Select a Group",
        font=("Arial", 18, "bold"),
        fg="cyan",
        bg="#0b0b23"
    )
    subtitle.pack(anchor="w", padx=40, pady=10)

    # Container for buttons
    button_frame = tk.Frame(frame, bg="#0b0b23")
    button_frame.pack(anchor="w", padx=40, pady=20)

    groups = [
        ("#2E2EFF", "Technical Team"),
        ("#0040AA", "Level 0 Training"),
        ("#4A7BFF", "Level 1 Training"),
        ("#89CFF0", "Level 2 Training")
    ]

    buttons = []

    for circle_color, text in groups:
        btn_label = tk.Label(button_frame, bd=0, bg="#0b0b23", cursor="hand2")
        btn_label.pack(pady=12, anchor="w")

        # Save button info
        buttons.append((btn_label, circle_color, text))

        def make_handler(selected_group=text):
            return lambda e: app.group_selected(selected_group)

        btn_label.bind("<Button-1>", make_handler())

    # Footer
    footer = tk.Label(
        frame,
        text="ICPC Zagazig University",
        font=("Caveat", 14, "italic"),
        fg="white",
        bg="#0b0b23"
    )
    footer.pack(side="bottom", pady=20)

    # Logo placeholder
    logo_label = tk.Label(frame, bg="#0b0b23")
    logo_label.place(relx=1.0, rely=0.0, anchor="ne")

    # Load logo once (original)
    try:
        logo_img_orig = Image.open("assets/logo.png")
    except Exception as e:
        print("Logo not found:", e)
        logo_img_orig = None

    def resize_elements(event=None):
        if not event:
            # Initial resize
            w, h = 1000, 700  # Default size
        else:
            w, h = event.width, event.height

        # Title resize
        title_font_size = max(20, w // 20)
        title.configure(font=("Archivo Black", title_font_size, "bold"))
        title.pack_configure(pady=(h // 12, h // 50))

        # Subtitle resize
        subtitle_font_size = max(12, w // 45)
        subtitle.configure(font=("Arial", subtitle_font_size, "bold"))

        # Buttons resize
        btn_w = max(300, int(w * 0.35))  # Minimum width
        btn_h = max(60, int(h * 0.1))    # Minimum height

        for btn_label, circle_color, text in buttons:
            # Create gradient button
            btn_img = create_gradient_button(btn_w, btn_h, "#ffffff", "#f0f0f0")
            btn_imgtk = ImageTk.PhotoImage(btn_img)

            # Create circle
            circle_size = btn_h - 20
            circle = Image.new("RGBA", (circle_size, circle_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(circle)
            draw.ellipse([0, 0, circle_size, circle_size], fill=circle_color)

            # Combine button and circle
            combined_img = Image.new("RGBA", (btn_img.width, btn_img.height), (0, 0, 0, 0))
            combined_img.paste(btn_img, (0, 0))
            
            # Paste circle onto the button
            circle_x = 15
            circle_y = (btn_img.height - circle_size) // 2
            combined_img.paste(circle, (circle_x, circle_y), circle)

            final_imgtk = ImageTk.PhotoImage(combined_img)

            btn_label.configure(
                image=final_imgtk,
                text=text,
                font=("Archivo Black", max(14, btn_h // 4), "bold"),
                compound="center",
                fg="black",
                bd=0
            )
            btn_label.image = final_imgtk

        # Logo resize
        if logo_img_orig:
            logo_size = min(int(w * 0.15), int(h * 0.15))
            logo_size = max(50, logo_size)  # Minimum size
            
            logo_resized = logo_img_orig.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            logo_imgtk = ImageTk.PhotoImage(logo_resized)

            logo_label.configure(image=logo_imgtk)
            logo_label.image = logo_imgtk

            logo_label.place(
                relx=1.0,
                rely=0.0,
                x=-20,
                y=20,
                anchor="ne"
            )

        # Footer resize
        footer_font_size = max(10, w // 55)
        footer.configure(font=("Century Gothic", footer_font_size, "italic"))

    # Initial resize
    frame.after(100, resize_elements)
    frame.bind("<Configure>", resize_elements)

    return frame