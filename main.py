# from api.api_call import get_messages
# from api.config import client
# import asyncio
# import tkinter as tk
# from ui.portal import HRTeacherPortal


# group = "https://t.me/+NdpMLsrN6YllZjk0"
# target_username = "ABDoooo_abdo"

# async def main():
#     await client.start()

#     await get_messages(group, target_username)

#     await client.disconnect()
    

# if __name__ == "__main__":
#     asyncio.run(main())
#     root = tk.Tk()
#     app = HRTeacherPortal(root)
#     root.mainloop()

from api.api_call import get_messages
from api.config import client
import asyncio
import tkinter as tk
from ui.portal import HRTeacherPortal


# These variables are now handled by the GUI selection
# group = "https://t.me/+NdpMLsrN6YllZjk0"
# target_username = "ABDoooo_abdo"

# The async main function is no longer needed here as the GUI manages the client
# async def main():
#     await client.start()
#     await get_messages(group, target_username)
#     await client.disconnect()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = HRTeacherPortal(root)
    root.mainloop()
    # The app.cleanup() is now called via the on_closing protocol
    # app.cleanup() 