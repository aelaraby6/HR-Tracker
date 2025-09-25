import tkinter as tk
from tkinter import ttk
from mentor_bot.db import get_all_mentors


def create_mentor_page(app):
    frame = tk.Frame(app.root, bg="#0b0b23")

    # Title
    title = tk.Label(
        frame,
        text="Select Mentor",
        font=("Archivo Black", 40, "bold"),
        fg="#a9c7ff",
        bg="#0b0b23"
    )
    title.pack(pady=(50, 20))

    mentors = [row[2] for row in get_all_mentors()]

    # Scrollable container
    container = tk.Frame(frame, bg="#0b0b23")
    canvas = tk.Canvas(container, bg="#0b0b23", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#0b0b23")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    container.pack_forget()

    # Show/Hide checklist
    def toggle_checklist():
        if container.winfo_ismapped():
            container.pack_forget()
            toggle_btn.config(text="Show Mentors")
        else:
            container.pack(fill="both", expand=True, padx=20, pady=10)
            toggle_btn.config(text="Hide Mentors")

    toggle_btn = tk.Button(
        frame,
        text="Show Mentors",
        command=toggle_checklist,
        bg="#4A7BFF",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=10,
        pady=5
    )
    toggle_btn.pack(pady=10)

    # Single selection variable
    selected_mentor_var = tk.StringVar(value="")  

    # Label to show selected mentor
    selected_label = tk.Label(
        frame,
        text="No mentor selected",
        font=("Arial", 14, "bold"),
        fg="white",   # default color
        bg="#0b0b23"
    )
    selected_label.pack(pady=10)

    def update_label(*args):
        value = selected_mentor_var.get()
        if value:
            selected_label.config(text=f"Selected: {value}", fg="lightgreen")
        else:
            selected_label.config(text="No mentor selected", fg="white")

    selected_mentor_var.trace_add("write", update_label)

    # Radiobuttons
    if mentors:
        for mentor in mentors:
            rbtn = ttk.Radiobutton(
                scrollable_frame,
                text=mentor,
                variable=selected_mentor_var,
                value=mentor
            )
            rbtn.pack(anchor="w", pady=2, padx=10)
    else:
        tk.Label(frame, text="No mentors found", fg="white", bg="#0b0b23").pack(pady=20)

    # Save + prepare for API call
    def save_selection():
        selected = selected_mentor_var.get()
        app.selected_mentor = selected
        app.selected_group = getattr(app, "selected_group", None)

        if not selected:
            print("⚠️ No mentor selected")
            return

        print(f"Group: {app.selected_group}")
        print(f"Mentor selected: {selected}")

        # Placeholder for API call
        print(f"Fetching messages for group={app.selected_group}, mentor={selected}")

    save_btn = tk.Button(
        frame,
        text="Save & Fetch",
        command=save_selection,
        bg="#4A7BFF",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=10,
        pady=5
    )
    save_btn.pack(pady=20)

    # Navigation
    nav_frame = tk.Frame(frame, bg="#0b0b23")
    nav_frame.pack(side="bottom", pady=20)

    back_btn = tk.Button(
        nav_frame,
        text="Back",
        command=lambda: app.show_page("group"),
        bg="#1f4068",
        fg="white",
        padx=15,
        pady=5
    )
    back_btn.pack(side="left", padx=20)

    home_btn = tk.Button(
        nav_frame,
        text="Home",
        command=lambda: app.show_page("start"),
        bg="#1f4068",
        fg="white",
        padx=15,
        pady=5
    )
    home_btn.pack(side="left", padx=20)

    return frame
