from api.config import client
from api.report_generator import export_user_messages, create_summary
import pandas as pd
from datetime import datetime, timedelta
import asyncio


async def get_messages(group,target_username):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Export Excel
    filename, count, df = await export_user_messages(
        group, target_username, client, start_date, end_date
    )

    # Generate PDF Summary
    create_summary(df, target_username, start_date, end_date)


# if __name__ == "__main__":
#     with client:
#         client.loop.run_until_complete(main())
