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


def create_start_page(app):
    frame = tk.Frame(app.root, bg="#0b0b23")

    # Title
    title = tk.Label(
        frame,
        text="HR Tracher",
        font=("Archivo Black", 40, "bold"),
        fg="#a9c7ff",
        bg="#0b0b23"
    )
    title.pack()

    # Button (placeholder first)
    start_btn = tk.Label(frame, bd=0, bg="#0b0b23", cursor="hand2")
    start_btn.place(relx=0.5, rely=0.5, anchor="center")

    def on_click(event):
        app.show_page("group")

    start_btn.bind("<Button-1>", on_click)

    # Footer
    footer = tk.Label(
        frame,
        text="ICPC Zagazig University",
        font=("Century Gothic", 14, "italic"),
        fg="white",
        bg="#0b0b23"
    )
    footer.pack(side="bottom")

    # Logo placeholder
    logo_label = tk.Label(frame, bg="#0b0b23")
    logo_label.place(relx=1.0, anchor="ne")

    # Load logo once (original)
    try:
        logo_img_orig = Image.open("assets/logo.png")
    except Exception as e:
        print("Logo not found:", e)
        logo_img_orig = None

    def resize_elements(event):
        w, h = event.width, event.height

        # Title size & padding
        title_font_size = max(20, w // 20)
        title.configure(font=("Archivo Black", title_font_size, "bold"))
        title.pack_configure(pady=(h // 12, h // 25))  

        # Button size
        btn_w = int(w * 0.28)
        btn_h = int(h * 0.12)
        btn_img = create_gradient_button(btn_w, btn_h, "#d6b6f5", "#5fa8f5")
        btn_imgtk = ImageTk.PhotoImage(btn_img)

        start_btn.configure(
            image=btn_imgtk,
            text="Start",
            font=("Archivo Black", max(18, btn_h // 3), "bold"),
            compound="center",
            fg="black"
        )
        start_btn.image = btn_imgtk
        start_btn.place(relx=0.5, rely=0.5, anchor="center")

                # Logo resize & position
        if logo_img_orig:
            orig_w, orig_h = logo_img_orig.size

            
            logo_w = int(w * 0.15)
            logo_h = int(h * 0.15)

           
            logo_w = max(50, min(logo_w, orig_w))   
            logo_h = max(50, min(logo_h, orig_h))  

            
            logo_resized = logo_img_orig.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
            logo_imgtk = ImageTk.PhotoImage(logo_resized)

            logo_label.configure(image=logo_imgtk)
            logo_label.image = logo_imgtk

        
            logo_label.place(
                relx=1.0,
                x=-w // 35,
                y=h // 45,
                anchor="ne"
            )

        # Footer size & padding
        new_font_size = max(12, w // 55)
        footer.configure(font=("Century Gothic", new_font_size, "italic"))
        footer.pack_configure(pady=h // 40)

    frame.bind("<Configure>", resize_elements)

    return frame
