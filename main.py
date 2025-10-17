from api.api_call import get_messages
from api.config import client
import asyncio
import tkinter as tk
from ui.portal import HRTeacherPortal



# group = "https://t.me/+HE4y8LhjrGFmYjI0"
# target_username = "ABDoooo_abdo"

# async def main():
#     await client.start()

#     await get_messages(group, target_username)

#     await client.disconnect()
    

# if __name__ == "__main__":
#     asyncio.run(main())



if __name__ == "__main__":
    root = tk.Tk()
    app = HRTeacherPortal(root)
    root.mainloop()
    app.cleanup() 