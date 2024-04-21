from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extractor = URLExtract()


def fetch_stats(select_user, df):
    if select_user != 'Overall':
        df = df[df['user'] == select_user]

    num_messages = df.shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_media = df[df['messages'] == '<Media omitted>\n'].shape[0]  # Corrected to '<Media omitted>'

    links = []
    for message in df['messages']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media, len(links)


def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100).reset_index().rename(columns={'index': 'users', 'count': 'percentage'})
    return x,df


def create_word(select_user, df):
    if select_user != 'Overall':
        df = df[df['user'] == select_user]
        f = open('stop_hinglish.txt', 'r')
        stopword = f.read()
        temp = df[df['user'] != 'group_notification']
        temp = temp[temp['messages'] != '<Media omitted>\n']
        def remove_stopword(message):
            y = []
            for word in message.lower().split():
                if word not in stopword:
                    y.append(word)
            return " ".join(y)

        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        temp['messages'] = temp['messages'].str.cat(sep =" ")
        wc_df = wc.generate(temp['messages'].str.cat(sep=" "))
        return wc_df


# most common WORDS
def common_user(select_user,df):
    f = open('stop_hinglish.txt', 'r')
    stopword = f.read()

    if select_user != 'Overall':
        df = df[df['user'] == select_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopword:
                words.append(word)


    common_df = pd.DataFrame(Counter(words).most_common(20))
    return common_df



def emoji_helper(select_user, df):
    if select_user != 'Overall':
        df = df[df['user'] == select_user]
    emojis = []
    for message in df['messages']:
        if isinstance(message, str) and message:  # Check if message is a non-empty string
            emojis.extend(c for c in message if c in emoji.UNICODE_EMOJI['en'])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(select_user,df):
    if select_user != 'Overall':
        df = df[df['user'] == select_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(select_user,df):
    if select_user != 'Overall':
        df = df[df['user'] == select_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline
def week_activity_map(select_user,df):
    if select_user != 'Overall':
        df = df[df['user'] == select_user]
    return df['day_name'].value_counts()
def month_activity_map(select_user,df):
    if select_user != 'Overall':
        df = df[df['user'] == select_user]
    return df['month'].value_counts()
def activity_heatmap(select_user,df):
    if select_user != 'Overall':
        df = df[df['user'] == select_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return user_heatmap