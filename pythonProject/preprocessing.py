import re
import pandas as pd
def preprocess(data):
    pattern  = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}\s(?:AM|PM|am|pm))\s-\s([^\:]+):\s(.*)'
    matches = re.findall(pattern, data)
    df = pd.DataFrame(matches, columns=['Date','Time', 'Sender', 'Message'])
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    df["day"] = df['Date'].map(lambda x: x.day)
    df["month"] = df['Date'].map(lambda x: x.strftime('%b'))
    df["year"] = df['Date'].map(lambda x: x.year)
    df["day_name"] = df['Date'].map(lambda x: x.strftime('%A'))
    df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p')
    df['hour'] = df['Time'].dt.hour
    df['minute'] = df['Time'].dt.minute
    df.drop(columns=['Date', 'Time'], inplace=True)
    return df
