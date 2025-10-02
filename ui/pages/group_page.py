import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from mentor_bot.db import get_all_groups

def create_gradient_button(width, height, color1, color2, radius=40):
    """Create rounded rectangle button with gradient and shadow"""
    try:
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
    except Exception as e:
        print(f"Error creating gradient button: {e}")
        # Return a simple colored rectangle as fallback
        fallback = Image.new("RGB", (width, height), color1)
        return fallback

def create_group_page(app):
    try:
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

        # Get groups from database with error handling
        try:
            groups_rows = get_all_groups()
            groups_map = {}
            for row in groups_rows:
                if len(row) >= 3:
                    display_name = row[1]
                    telegram_link = row[2]
                    groups_map[display_name] = telegram_link
                else:
                    for item in row:
                        if isinstance(item, str) and item.strip():
                            groups_map[item.strip()] = item.strip()
                            break
            
            # Use database groups if available, otherwise use defaults
            if groups_map:
                groups = []
                colors = ["#2E2EFF", "#0040AA", "#4A7BFF", "#89CFF0", "#1E90FF"]
                for i, (display_name, telegram_link) in enumerate(groups_map.items()):
                    color = colors[i % len(colors)] if i < len(colors) else "#4A7BFF"
                    groups.append((color, display_name, telegram_link))
            else:
                # Default groups if database is empty
                groups = [
                    ("#2E2EFF", "Technical Team", "https://t.me/+NdpMLsrN6YllZjk0"),
                    ("#0040AA", "Level 0 Training", "https://t.me/+level0_training"),
                    ("#4A7BFF", "Level 1 Training", "https://t.me/+level1_training"),
                    ("#89CFF0", "Level 2 Training", "https://t.me/+level2_training")
                ]
                
        except Exception as e:
            print(f"Database error: {e}")
            # Fallback groups - use exact groups from your design
            groups = [
                ("#2E2EFF", "Technical Team", "https://t.me/+NdpMLsrN6YllZjk0"),
                ("#0040AA", "Level 0 Training", "https://t.me/+level0_training"),
                ("#4A7BFF", "Level 1 Training", "https://t.me/+level1_training"),
                ("#89CFF0", "Level 2 Training", "https://t.me/+level2_training")
            ]

        buttons = []

        for circle_color, display_name, telegram_link in groups:
            btn_label = tk.Label(button_frame, bd=0, bg="#0b0b23", cursor="hand2")
            btn_label.pack(pady=12, anchor="w")

            # Save button info
            buttons.append((btn_label, circle_color, display_name, telegram_link))

            def make_handler(selected_display=display_name, selected_link=telegram_link):
                def handler(e=None):
                    try:
                        # Validate the Telegram link
                        if not selected_link or "t.me" not in selected_link:
                            messagebox.showwarning(
                                "Invalid Group Link",
                                f"The group '{selected_display}' has an invalid Telegram link.\n"
                                f"Please check the database configuration."
                            )
                            return
                        
                        # Store both display name and actual link
                        app.selected_group_display = selected_display
                        app.selected_group = selected_link
                        
                        print(f"Group selected: {selected_display}")
                        print(f"Telegram link: {selected_link}")
                        
                        # Navigate to mentor page
                        app.group_selected(selected_display)
                        
                    except Exception as e:
                        messagebox.showerror(
                            "Selection Error",
                            f"Failed to select group '{selected_display}': {str(e)}"
                        )
                return handler

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

        # Load logo with error handling
        logo_img_orig = None
        try:
            logo_img_orig = Image.open("assets/logo.png")
            print("Logo loaded successfully")
        except Exception as e:
            print(f"Logo not found: {e}")
            logo_img_orig = None

        def resize_elements(event=None):
            try:
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

                for btn_label, circle_color, display_name, telegram_link in buttons:
                    try:
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
                            text=display_name,
                            font=("Archivo Black", max(14, btn_h // 4), "bold"),
                            compound="center",
                            fg="black",
                            bd=0
                        )
                        btn_label.image = final_imgtk

                    except Exception as btn_error:
                        print(f"Error creating button for {display_name}: {btn_error}")
                        # Fallback: simple text button
                        btn_label.configure(
                            text=display_name,
                            bg=circle_color,
                            fg="white",
                            font=("Archivo Black", max(14, btn_h // 4), "bold"),
                            padx=20,
                            pady=10,
                            relief="raised",
                            bd=2
                        )

                # Logo resize
                if logo_img_orig:
                    try:
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
                    except Exception as logo_error:
                        print(f"Error resizing logo: {logo_error}")

                # Footer resize
                footer_font_size = max(10, w // 55)
                footer.configure(font=("Caveat", footer_font_size, "italic"))

            except Exception as resize_error:
                print(f"Error in resize_elements: {resize_error}")

        # Initial resize with error handling
        def safe_initial_resize():
            try:
                resize_elements()
            except Exception as e:
                print(f"Initial resize error: {e}")

        frame.after(100, safe_initial_resize)
        
        # Bind resize event with error handling
        def safe_resize(event):
            try:
                resize_elements(event)
            except Exception as e:
                print(f"Resize event error: {e}")

        frame.bind("<Configure>", safe_resize)

        return frame

    except Exception as e:
        # Critical error - create a simple fallback page
        print(f"Critical error creating group page: {e}")
        
        error_frame = tk.Frame(app.root, bg="#0b0b23")
        
        error_label = tk.Label(
            error_frame,
            text="Error Loading Groups",
            font=("Arial", 16, "bold"),
            fg="red",
            bg="#0b0b23"
        )
        error_label.pack(pady=50)
        
        message_label = tk.Label(
            error_frame,
            text=str(e),
            font=("Arial", 12),
            fg="white",
            bg="#0b0b23",
            wraplength=400
        )
        message_label.pack(pady=10)
        
        retry_btn = tk.Button(
            error_frame,
            text="Retry",
            command=lambda: app.show_page("group"),
            bg="#4A7BFF",
            fg="white",
            font=("Arial", 12, "bold")
        )
        retry_btn.pack(pady=20)
        
        home_btn = tk.Button(
            error_frame,
            text="Home",
            command=app.go_home,
            bg="#1f4068",
            fg="white"
        )
        home_btn.pack(pady=10)
        
        return error_frame