from wordcloud import WordCloud
import pandas as pd
import emoji
import os
from collections import Counter
def fetch_stats(user,df):
    if user != 'overall':
        df = df[df['Sender']==user]
    num_msges = df.shape[0]
    words=[]
    for msg in df['Message']:
        words.extend(msg.split())
    media = df[df['Message']== '<Media omitted>']
    links=[]
    from urlextract import URLExtract
    extractor = URLExtract()
    for msg in df['Message']:
        links.extend(extractor.find_urls(msg))
    return num_msges,len(words),media.shape[0],len(links)

def fetch_most_active_users(df):
    x = df['Sender'].value_counts().head()
    pc = round((df['Sender'].value_counts()/df.shape[0])*100,2).reset_index()
    pc.columns = ['name', 'percent']
    return x,pc

def create_word_cloud(user,df):
    
    file_path = os.path.join(os.path.dirname(__file__), "stop_hinglish.txt")
    f = open(file_path, "r")
    stop_words = f.read()
    if user != 'overall':
        df = df[df['Sender']==user]
    temp = df[df['Message']!='<Media omitted>']
    def remove_stop_words(msg):
        y=[]
        for word in msg.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc

def most_common_words(user,df):
    file_path = os.path.join(os.path.dirname(__file__), "stop_hinglish.txt")
    f = open(file_path,'r')
    stop_words = f.read()
    if user != 'overall':
        df = df[df['Sender']==user]
    temp = df[df['Sender']!='group_notificatiion']
    temp = temp[temp['Message']!='<Media omitted>']
    words=[]
    for msg in temp['Message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    most_common_df.columns = ['Word', 'Frequency']
    return most_common_df

def most_commmon_emoji(user,df):
    if user != 'overall':
        df = df[df['Sender']==user]
    emojis = []
    for msg in df['Message']:
        emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])
    emojidf= pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emojidf.columns = ['Emoji','Frequency']
    return emojidf

def monthly_time_lime(user,df):
    if user != 'overall':
        df = df[df['Sender']==user]
    timeline = df.groupby(['year', 'month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_time_line(user,df):
    if user != 'overall':
        df = df[df['Sender']==user]
    return df['day_name'].value_counts()


def activity_heat_map(user,df):
    if user != 'overall':
        df = df[df['Sender']==user]
    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour)+ "-" + str(hour+1))
    df['period'] = period

    activity = df.pivot_table(index='day_name',columns='period',values='Message',aggfunc='count').fillna(0)
    return activity



