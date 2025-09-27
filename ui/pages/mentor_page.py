# ui/pages/mentor_page.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading

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

    # Get mentors rows from DB
    mentors_rows = get_all_mentors()  # list of tuples/rows
    # Build list of display names (attempt to find a display column)
    mentors = []
    for row in mentors_rows:
        # row could be (id, telegram_username, display_name) or another order
        # Try to extract a human display name at possible positions
        display = None
        for idx in (2, 1, 0):
            if idx < len(row) and row[idx]:
                # prefer position 2 or 1 if it's a string longer than 1 char
                if isinstance(row[idx], str) and len(row[idx].strip()) > 0:
                    display = row[idx].strip()
                    break
        if display:
            mentors.append((display, row))
    # De-duplicate by display name
    seen = set()
    mentors_unique = []
    for display, row in mentors:
        if display not in seen:
            seen.add(display)
            mentors_unique.append((display, row))

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

    # Radiobuttons (single choice)
    if mentors_unique:
        for display, row in mentors_unique:
            rbtn = ttk.Radiobutton(
                scrollable_frame,
                text=display,
                variable=selected_mentor_var,
                value=display
            )
            rbtn.pack(anchor="w", pady=2, padx=10)
    else:
        tk.Label(frame, text="No mentors found", fg="white", bg="#0b0b23").pack(pady=20)

    # ---- Mentor detail window ----
    def open_mentor_window(selected_display):
        # Find the DB row corresponding to selected_display
        db_row = None
        for disp, row in mentors_unique:
            if disp == selected_display:
                db_row = row
                break

        win = tk.Toplevel(app.root)
        win.title(f"Mentor - {selected_display}")
        win.geometry("600x500")
        win.configure(bg="#1b2138")
        
        # Make window modal
        win.transient(app.root)
        win.grab_set()

        lbl_name = tk.Label(win, text=f"Name: {selected_display}", font=("Arial", 14, "bold"), fg="white", bg="#1b2138")
        lbl_name.pack(pady=(20, 10))

        # Display selected group info
        group_info = tk.Label(win, text=f"Group: {app.selected_group}", font=("Arial", 12), fg="#a9c7ff", bg="#1b2138")
        group_info.pack(pady=(0, 20))

        # Try to extract a telegram username from the row (common positions)
        suggested_username = ""
        if db_row:
            # look for a likely username: a string that starts with letter/number and maybe has @
            for val in db_row:
                if isinstance(val, str) and val.strip():
                    v = val.strip()
                    # a quick heuristic: username often without spaces and shorter than 64 chars
                    if " " not in v and len(v) < 64:
                        # ignore numeric id-looking values
                        if not v.isdigit():
                            suggested_username = v
                            break

        lbl_username = tk.Label(win, text="Telegram username (without @):", fg="white", bg="#1b2138", font=("Arial", 11))
        lbl_username.pack(pady=(10, 0))
        
        entry_frame = tk.Frame(win, bg="#1b2138")
        entry_frame.pack(pady=(5, 10))
        
        entry_username = tk.Entry(entry_frame, width=40, font=("Arial", 12))
        entry_username.pack(side="left", padx=(0, 10))
        entry_username.insert(0, suggested_username)
        
        # Auto-detect button
        def auto_detect_username():
            if suggested_username:
                entry_username.delete(0, tk.END)
                entry_username.insert(0, suggested_username)
                messagebox.showinfo("Auto-detected", f"Using username: {suggested_username}")
            else:
                messagebox.showinfo("No username found", "No username could be auto-detected from database.")
        
        auto_btn = tk.Button(entry_frame, text="Auto-detect", command=auto_detect_username,
                           bg="#6c757d", fg="white", font=("Arial", 10), padx=10)
        auto_btn.pack(side="left")

        # Progress / status label
        status_label = tk.Label(win, text="Ready", fg="lightgreen", bg="#1b2138", font=("Arial", 11, "bold"))
        status_label.pack(pady=(5, 5))

        # Result text area with scrollbar
        result_frame = tk.Frame(win, bg="#1b2138")
        result_frame.pack(pady=(10, 5), padx=10, fill="both", expand=True)
        
        result_text = tk.Text(result_frame, height=12, width=70, bg="#2a2f4c", fg="white", 
                            font=("Consolas", 10), wrap=tk.WORD)
        result_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_text.yview)
        result_text.configure(yscrollcommand=result_scrollbar.set)
        
        result_text.pack(side="left", fill="both", expand=True)
        result_scrollbar.pack(side="right", fill="y")
        
        result_text.insert("1.0", "=== HR Tracker - Report Generator ===\n")
        result_text.insert("2.0", "Select a mentor and click 'Fetch & Generate Reports' to begin.\n")
        result_text.config(state="disabled")

        # Button frame
        button_frame = tk.Frame(win, bg="#1b2138")
        button_frame.pack(pady=15)

        # Disable button while running
        def run_fetch():
            username = entry_username.get().strip()
            if username.startswith("@"):
                username = username[1:]

            if not username:
                messagebox.showwarning("Missing username", "Please provide the mentor's Telegram username.")
                return

            if not app.selected_group:
                messagebox.showwarning("Missing group", "No group selected. Please go back and select a group.")
                return

            # disable UI
            fetch_btn.config(state="disabled")
            auto_btn.config(state="disabled")
            status_label.config(text="Running... Please wait...", fg="yellow")
            result_text.config(state="normal")
            result_text.delete("1.0", tk.END)
            result_text.insert("1.0", "Starting fetch process...\n")
            result_text.see(tk.END)
            result_text.config(state="disabled")

            # Run the fetch in a separate thread to avoid blocking Tk mainloop
            def target_thread():
                try:
                    # Update status in UI thread
                    def update_status(message):
                        status_label.config(text=message)
                        result_text.config(state="normal")
                        result_text.insert(tk.END, f"{message}\n")
                        result_text.see(tk.END)
                        result_text.config(state="disabled")
                    
                    win.after(0, lambda: update_status("🔍 Connecting to Telegram..."))
                    
                    # Use the app's run_fetch_data method
                    if hasattr(app, 'run_fetch_data'):
                        win.after(0, lambda: update_status("📡 Fetching messages..."))
                        
                        # This will call the portal's run_fetch_data method
                        result = app.run_fetch_data(app.selected_group, username)
                        
                        # on success
                        win.after(0, lambda: update_status("✅ Fetch completed successfully!"))
                        win.after(0, lambda: update_status(f"📊 Group: {app.selected_group}"))
                        win.after(0, lambda: update_status(f"👤 Mentor: {username}"))
                        win.after(0, lambda: update_status("💾 Reports saved in 'reports' folder"))
                        
                        win.after(0, lambda: status_label.config(text="Done! Check 'reports' folder", fg="lightgreen"))
                        win.after(0, lambda: messagebox.showinfo("Done", "Reports generated successfully!\nCheck the 'reports' folder."))
                        
                    else:
                        raise Exception("Fetch functionality not available")

                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    win.after(0, lambda: status_label.config(text=error_msg, fg="red"))
                    win.after(0, lambda: result_text.config(state="normal"))
                    win.after(0, lambda: result_text.insert(tk.END, f"{error_msg}\n"))
                    win.after(0, lambda: result_text.see(tk.END))
                    win.after(0, lambda: result_text.config(state="disabled"))
                    win.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch/generate:\n{str(e)}"))
                    
                finally:
                    win.after(0, lambda: fetch_btn.config(state="normal"))
                    win.after(0, lambda: auto_btn.config(state="normal"))

            t = threading.Thread(target=target_thread, daemon=True)
            t.start()

        fetch_btn = tk.Button(button_frame, text="🚀 Fetch & Generate Reports", command=run_fetch, 
                             bg="#28a745", fg="white", font=("Arial", 12, "bold"), 
                             padx=20, pady=10)
        fetch_btn.pack(side="left", padx=10)

        # Clear results button
        def clear_results():
            result_text.config(state="normal")
            result_text.delete("1.0", tk.END)
            result_text.insert("1.0", "=== HR Tracker - Report Generator ===\n")
            result_text.insert("2.0", "Select a mentor and click 'Fetch & Generate Reports' to begin.\n")
            result_text.see(tk.END)
            result_text.config(state="disabled")
            status_label.config(text="Ready", fg="lightgreen")

        clear_btn = tk.Button(button_frame, text="🗑️ Clear Results", command=clear_results,
                             bg="#6c757d", fg="white", font=("Arial", 10), 
                             padx=15, pady=5)
        clear_btn.pack(side="left", padx=10)

        # Navigation buttons
        nav_frame = tk.Frame(win, bg="#1b2138")
        nav_frame.pack(side="bottom", pady=12, fill="x")

        def close_win():
            win.destroy()

        close_btn = tk.Button(nav_frame, text="❌ Close Window", command=close_win, 
                             bg="#dc3545", fg="white", font=("Arial", 10, "bold"), 
                             padx=15, pady=6)
        close_btn.pack(side="right", padx=10)
        
        def open_new_mentor():
            win.destroy()
            save_selection()

        new_mentor_btn = tk.Button(nav_frame, text="👥 Select Different Mentor", command=open_new_mentor,
                                  bg="#17a2b8", fg="white", font=("Arial", 10), 
                                  padx=10, pady=6)
        new_mentor_btn.pack(side="right", padx=10)

    def save_selection():
        selected = selected_mentor_var.get()
        app.selected_mentor = selected

        if not selected:
            print("⚠️ No mentor selected")
            messagebox.showwarning("No selection", "Please select a mentor first.")
            return

        if not app.selected_group:
            messagebox.showwarning("No group", "Please go back and select a group first.")
            return

        print(f"Group: {app.selected_group}")
        print(f"Mentor selected: {selected}")

        # Open detail window for the mentor
        open_mentor_window(selected)

    save_btn = tk.Button(
        frame,
        text="📋 Open Mentor Details",
        command=save_selection,
        bg="#4A7BFF",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=15,
        pady=8
    )
    save_btn.pack(pady=20)

    # Navigation
    nav_frame = tk.Frame(frame, bg="#0b0b23")
    nav_frame.pack(side="bottom", pady=20)

    back_btn = tk.Button(
        nav_frame,
        text="⬅️ Back to Groups",
        command=lambda: app.show_page("group"),
        bg="#1f4068",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=15,
        pady=5
    )
    back_btn.pack(side="left", padx=20)

    home_btn = tk.Button(
        nav_frame,
        text="🏠 Home",
        command=lambda: app.show_page("start"),
        bg="#1f4068",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=15,
        pady=5
    )
    home_btn.pack(side="left", padx=20)

    return frame