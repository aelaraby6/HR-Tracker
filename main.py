
# from api.config import client
# from api.report_generator import export_user_messages, create_weekly_summary
# import pandas as pd


# async def main():
#     group = "https://t.me/+NdpMLsrN6YllZjk0"
#     target_username = "ABDoooo_abdo"

    # Export Excel
 #   filename, count = await export_user_messages(group, target_username, client)

   # df = pd.read_excel(filename)

    # Generate PDF Summary
 #   create_weekly_summary(df, target_username)

# if __name__ == "__main__":
#     with client:
#         client.loop.run_until_complete(main())


import tkinter as tk
from ui.portal import HRTeacherPortal

if __name__ == "__main__":
         root = tk.Tk()
         app = HRTeacherPortal(root)
         root.mainloop()
        