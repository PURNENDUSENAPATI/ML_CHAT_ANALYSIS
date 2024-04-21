import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("WHATSAPP_APP_ANALYSER")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    user_list = df['user'].unique().tolist()

    user_list.sort()
    user_list.insert(0, "Overall")
    select_user = st.sidebar.selectbox("CHOOSE THE ANALYSIS WRT", user_list)
    if st.sidebar.button("Analysis"):

        num_messages, words, num_media, num_links = helper.fetch_stats(select_user, df)
        st.title("TOP STATICS")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header('Total Media')
            st.title(num_media)
        with col4:
            st.header("Total Links")
            st.title(num_links)

        #MONTHLY TimeLINE
        st.title('Monthly_Timeline')
        timeline = helper.monthly_timeline(select_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'])
        plt.xticks(rotation='vertical')

        # Display the plot using st.pyplot()
        st.pyplot(fig)





         # DAILY TIMING
        st.title('Daily_Timeline')
        daily_timeline = helper.daily_timeline(select_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'],color = 'black')
        plt.xticks(rotation='vertical')

        # Display the plot using st.pyplot()
        st.pyplot(fig)

        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day  = helper.week_activity_map(select_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(select_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title('Weakly Activity Map')
        user_heatmap = helper.activity_heatmap(select_user,df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, cmap='coolwarm', ax=ax)

        st.pyplot(fig)


        # Finding the busiest user s in the group
        if select_user == 'Overall':
            st.title('Most Busy User')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

            # Generate and display the word cloud for the overall dataset
            st.title("Wordcloud")
            df_wc = helper.create_word(select_user, df)
            if df_wc is not None:  # Check if word cloud is generated
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                ax.axis('off')  # Turn off axis
                st.pyplot(fig)
            else:
                st.write("No word cloud available for the selected user.")

            # Display common words for the overall dataset
            st.title("Common Words")
            common_df = helper.common_user(select_user, df)
            st.dataframe(common_df)

        else:  # Display data specific to the selected user
            st.title('User: {}'.format(select_user))
            st.title("Wordcloud")
            df_wc = helper.create_word(select_user, df)
            if df_wc is not None:  # Check if word cloud is generated
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                ax.axis('off')  # Turn off axis
                st.pyplot(fig)
            else:
                st.write("No word cloud available for the selected user.")

            st.title("Common Words")
            common_df = helper.common_user(select_user, df)
            fig,ax = plt.subplots()
            ax.barh(common_df[0],common_df[1])
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
            st.dataframe(common_df)

        # EMOJI ANALYSIS
        st.title("Emoji Statistics")
        emoji_df = helper.emoji_helper(select_user,df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(10), labels=emoji_df[0].head(10), autopct='%0.2f', shadow=True, startangle=90)
            st.pyplot(fig)