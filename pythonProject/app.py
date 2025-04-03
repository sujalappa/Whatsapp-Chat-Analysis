import streamlit as st
import preprocessing,helper
import matplotlib.pyplot as plt
import seaborn as sns

from helper import most_common_words, most_commmon_emoji

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessing.preprocess(data)
    user_list = df['Sender'].unique().tolist()
    user_list.insert(0,"overall")
    user_selected= st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Statistical Analysis")
        num_msg,len_words,num_media,num_link = helper.fetch_stats(user_selected,df)
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(len_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)

        with col4:
            st.header("links Shared")
            st.title(num_link)
        #timeline analysis
        col1,col2 = st.columns(2)
        with col1:
            st.header("Monthly Timeline")
            timeline = helper.monthly_time_lime(user_selected, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['Message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header(" ")
            tl = df.groupby(['year','month']).count()['Message'].sort_values(ascending=False).reset_index()
            tl['year'] = tl['year'].astype(str)
            st.dataframe(tl)
       #activity map
        st.title("Day-Wise Chat Distribution")
        dailyline = helper.daily_time_line(user_selected,df)
        fig,ax = plt.subplots()
        ax.bar(dailyline.index,dailyline.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title("Weekly Activity Map")
        heat_map = helper.activity_heat_map(user_selected,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(heat_map)
        st.pyplot(fig)

        if user_selected == 'overall':
            x,per_chat = helper.fetch_most_active_users(df)

            col1,col2 = st.columns(2)

            with col1:
               st.header("Most_active_Users")
               fig,ax = plt.subplots()
               ax.bar(x.index,x.values)
               plt.ylabel("Msg Frequency")
               plt.xticks(rotation="vertical")
               st.pyplot(fig)
            with col2:
                st.header(" ")
                st.dataframe(per_chat)
        st.title("Word Cloud")
        df_wc = helper.create_word_cloud(user_selected,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df= helper.most_common_words(user_selected,df)
        st.title("Most Common Words")
        fig,ax = plt.subplots()
        ax.bar(most_common_df["Word"],most_common_df["Frequency"])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # emoji analysis
        most_commmon_emoji_df = helper.most_commmon_emoji(user_selected,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)
        plt.rcParams['font.family'] = 'DejaVu Sans'

        with col1:
            st.header(" ")
            st.dataframe(most_commmon_emoji_df)
        with col2:
            st.header("Top emoji's used")
            top_emoji_df = most_commmon_emoji_df.head(5)
            fig,ax = plt.subplots()
            ax.pie(top_emoji_df['Frequency'],labels=top_emoji_df['Emoji'],autopct="%0.2f")
            st.pyplot(fig)