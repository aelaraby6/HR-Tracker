import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from api.telegram_utils import fetch_messages


# ----- PDF SUMMARY -----
from datetime import datetime

def create_summary(df: pd.DataFrame, username: str, start_date: datetime, end_date: datetime):
    if df.empty:
        print(f"[!] No messages found for @{username} in the given period.")
        return None

    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    df['date'] = pd.to_datetime(df['date'])
    df_range = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if df_range.empty:
        print(f"[!] No messages in range {start_date.date()} → {end_date.date()}")
        return None

    total_msgs = len(df_range)
    active_days = df_range['date'].dt.date.nunique()
    daily_counts = df_range.groupby(df_range['date'].dt.date).size()
    most_active_day = daily_counts.idxmax() if not daily_counts.empty else "N/A"

    # ----- Chart -----
    plt.figure(figsize=(6, 4))
    daily_counts.plot(kind="bar")
    plt.title(f"Messages per Day (@{username})\n{start_date.date()} → {end_date.date()}")
    plt.xlabel("Date")
    plt.ylabel("Messages")
    chart_path = os.path.join(reports_dir, f"chart_{username}.png")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    # ----- Unique filename with timestamp -----
    timestamp = datetime.now().strftime("%H%M%S")
    filename = os.path.join(
        reports_dir,
        f"summary_{username}_{start_date.date()}_{end_date.date()}_{timestamp}.pdf"
    )

    # ----- PDF -----
    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"Summary Report - @{username}")

    c.setFont("Helvetica", 12)
    c.drawString(50, 780, f"Period: {start_date.date()} → {end_date.date()}")
    c.drawString(50, 760, f"Total Messages: {total_msgs}")
    c.drawString(50, 740, f"Active Days: {active_days}")
    c.drawString(50, 720, f"Most Active Day: {most_active_day}")

    if os.path.exists(chart_path):
        c.drawImage(ImageReader(chart_path), 50, 450, width=500, height=250)

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 420, f"Generated on: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")

    c.save()
    os.remove(chart_path)

    print(f"[+] PDF Summary saved: {filename}")
    return filename


# ----- Excel Report -----
async def export_user_messages(group: str, target_username: str, client, start_date: datetime, end_date: datetime):
    count, messages_list = await fetch_messages(group, target_username, start_date, end_date)

    data = []
    for msg in messages_list:
        data.append({
            "date": msg.date.strftime("%Y-%m-%d %H:%M:%S") if msg.date else "",
            "sender": target_username,
            "message": msg.text if msg.text else "",
            "message_id": msg.id if msg.id else None
        })


    df = pd.DataFrame(data, columns=["date", "sender", "message", "message_id"])

    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    filename = os.path.join(
        reports_dir,
        f"messages_{target_username}_{start_date.date()}_{end_date.date()}.xlsx"
    )
    df.to_excel(filename, index=False)

    print(f"[+] Saved {count} messages for @{target_username} from {start_date.date()} to {end_date.date()} -> {filename}")
    return filename, count, df