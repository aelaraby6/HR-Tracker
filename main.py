from api.api_call import get_messages
from api.config import client
import asyncio
import tkinter as tk
from ui.portal import HRTeacherPortal


group = "https://t.me/+NdpMLsrN6YllZjk0"
target_username = "ABDoooo_abdo"

async def main():
    await client.start()

    await get_messages(group, target_username)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
    root = tk.Tk()
    app = HRTeacherPortal(root)
    root.mainloop()



