import os
import pandas as pd
from api.telegram_utils import fetch_messages
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ----- PDF SUMMARY -----
def create_weekly_summary(df: pd.DataFrame, username: str):
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    today = datetime.today()
    start_date = today - timedelta(days=7)

    df['date'] = pd.to_datetime(df['date'])
    df_week = df[(df['date'] >= start_date) & (df['date'] <= today)]

    total_msgs = len(df_week)
    active_days = df_week['date'].dt.date.nunique()
    daily_counts = df_week.groupby(df_week['date'].dt.date).size()
    most_active_day = daily_counts.idxmax() if not daily_counts.empty else "N/A"

    # ----- Chart -----
    plt.figure(figsize=(6, 4))
    daily_counts.plot(kind="bar")
    plt.title(f"Messages per Day (@{username}) - Last 7 Days")
    plt.xlabel("Date")
    plt.ylabel("Messages")
    chart_path = os.path.join(reports_dir, f"chart_{username}.png")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    # ----- PDF -----
    filename = os.path.join(reports_dir, f"summary_{username}_{today.strftime('%Y-%m-%d')}.pdf")
    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"Weekly Summary Report - @{username}")

    c.setFont("Helvetica", 12)
    c.drawString(50, 780, f"Period: {start_date.date()} → {today.date()}")
    c.drawString(50, 760, f"Total Messages: {total_msgs}")
    c.drawString(50, 740, f"Active Days: {active_days}")
    c.drawString(50, 720, f"Most Active Day: {most_active_day}")

    if os.path.exists(chart_path):
        c.drawImage(ImageReader(chart_path), 50, 450, width=500, height=250)

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 420, f"Generated on: {today.strftime('%Y-%m-%d %H:%M:%S')}")

    c.save()
    os.remove(chart_path) 

    print(f" PDF Summary saved: {filename}")
    return filename


# Excel Report
async def export_user_messages(group: str, target_username: str, client):
    count, messages_list = await fetch_messages(group, target_username)

    data = []
    for msg in messages_list:
        data.append({
            "date": msg.date.strftime("%Y-%m-%d %H:%M:%S"),
            "sender": target_username,
            "message": msg.text if msg.text else "",
            "message_id": msg.id
        })

    df = pd.DataFrame(data)

    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True) 

    filename = os.path.join(reports_dir, f"messages_{target_username}.xlsx")
    df.to_excel(filename, index=False)

    print(f"Saved {count} messages for @{target_username} -> {filename}")
    return filename, count
