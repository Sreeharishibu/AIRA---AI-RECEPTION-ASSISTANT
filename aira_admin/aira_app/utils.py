# aira_app/utils.py
import os
import pandas as pd
from django.conf import settings
from datetime import datetime

def log_interaction_to_excel(user_query, matched_query, answer):
    file_path = os.path.join(settings.MEDIA_ROOT, "chatbot_logs.xlsx")

    data = {
        "Timestamp": [datetime.now()],
        "User Query": [user_query],
        "Matched Query": [matched_query],
        "Answer": [answer],
    }

    df_new = pd.DataFrame(data)

    if os.path.exists(file_path):
        df_existing = pd.read_excel(file_path)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_excel(file_path, index=False)
