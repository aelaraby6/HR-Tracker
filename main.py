# from datetime import datetime, timedelta
# import pandas as pd

# from api.config import client
# from api.report_generator import export_user_messages, create_summary


# async def main():
#     group = "https://t.me/+NdpMLsrN6YllZjk0"
#     target_username = "ABDoooo_abdo"

#     end_date = datetime.today()
#     start_date = end_date - timedelta(days=7)

#     filename, count, df = await export_user_messages(group, target_username, client, start_date, end_date)

#     # Generate PDF Summary
#     create_summary(df, target_username, start_date, end_date)


# if __name__ == "__main__":
#     with client:
#         client.loop.run_until_complete(main())


import tkinter as tk
from ui.portal import HRTeacherPortal

if __name__ == "__main__":
         root = tk.Tk()
         app = HRTeacherPortal(root)
         root.mainloop()
