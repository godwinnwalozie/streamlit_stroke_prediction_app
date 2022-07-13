# importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import joblib
import pickle
from wordcloud import WordCloud
import seaborn as sns


st.set_page_config(layout="wide")

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 2rem;
                    padding-bottom: 5rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-wjbhl0 {
                    padding-top: 3rem;
                    padding-right: 1rem;
                    padding-bottom: 1rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


# button styling
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: indigo;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #6F84FF;
    color:#ffffff
    }
</style>""", unsafe_allow_html=True)


@st.cache(suppress_st_warning=True, allow_output_mutation=True, persist= True)
def load_model():
    model = pickle.load(open("/home/mazi/Data_Science_ML/Streamlit Machine Learning Apps/pages/model_twitter.pkl", "rb"))
    data = pd.read_csv("/home/mazi/Data_Science_ML/Streamlit Machine Learning Apps/pages/twitter_cleaned.csv", usecols=[0,1,2])
    return model, data

model,data = load_model()

# unpacking turple
model_load, dataset = model, data



with st.container():
    st.title(" 𝐓𝐰𝐢𝐭𝐭𝐞𝐫 - 𝐒𝐞𝐧𝐭𝐢𝐦𝐞𝐧𝐭𝐬 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐨𝐟 𝐓𝐰𝐞𝐞𝐭𝐬")
    st.info( """ ### Negative 👎 Neutral😐 Positive 👍   """)
   
    
   
    st.markdown (""" Sentiment Analysis is the use of ML models to recognize and categorize statements made in reviews, tweets, or chats about a product or\
        sevices , if the feedbacks are are positive, negative, or neutral.\\
        This type of models will help customer the success or product teams to ascertain if the product is doing well, or if there is an area that clients are not happy about, such as price, quality and so on.""")


col1, col2 = st.columns(2)
col1.metric("Estimator", "KNeighborsClassifier")
col2.metric("Prediction Score Accuracy", "72% w/o hyperparameter tuning")
#st.write(data.sample(3))

with st.container():

    
    col1, col2 = st.columns(2)
    with col1:

        st.markdown("")
        with st.container():
            st.subheader("Model testing")
            st.write("##### Enter a sample tweet to test ")

            tweet = st.text_input('Enter a tweet to test, at least 30 characters') 

            if st.button('click to make a prediction 👈'):
                if tweet == "" :
                    counter = len(tweet)  
                    st.markdown(f" character counter: {counter}")
                    st.error(" ##### ...no do mago mago, 😀 input some text")
                    
                    
                elif len(tweet) < 30:
                    counter = len(tweet)  
                    st.markdown(f" character counter: {counter}")
                    st.error(" #####  😔 you too like mago mago ,enter more chracter")
                
                else:
                    probab = model_load.predict_proba([tweet])
                    probab_neg = model_load.predict_proba([tweet])[:,0]
                    probab_neut = model.predict_proba([tweet])[:,1]
                    probab_pos = model_load.predict_proba([tweet])[:,2]
                    prediction = model_load.predict([tweet])[0] 
                    if prediction  == -1 :
                        prediction =  "Negative review 👎" 
                    elif  prediction == 0:
                        prediction = "Neutral Review   😐"
                    else:
                        prediction = "Positive Review  ⭐👍"
                    st.write(f" #### {prediction} ")
                    st.write(f" ##### Negative @ {probab_neg *100}%   Neutral @{probab_neut*100}%  Positive @ {probab_pos*100}% ")
                  


                    

with col2:
    st.sidebar.title("Select plots")
    option = st.sidebar.radio('what plots would you like to be displayed', 
                      ("positive key words","negative key words",'count of tweets by airline', 
                       'distribution of sentiments(pie chart)', "sentiments by airline(bar graph)"))
    
    st.markdown("")
    st.subheader("  Use the sidebars to select plot types")
    
    
    
    #wordcloud postive sentiments
    @st.cache(hash_funcs={matplotlib.figure.Figure: lambda _: None})
    def wordcloud_pos ():
        fig, ax = plt.subplots() 
        super = dataset.loc[:,["tweets","airline_sentiment"]]
        text = "".join(super[super.airline_sentiment == "positive"].tweets)
        wc= WordCloud(max_words = 4000,background_color = "white").generate(text)
        ax.imshow(wc,interpolation='bilinear')
        plt.title("most occuring positive words", fontsize = 13)
        plt.axis("off")
        return fig
    plot1 = wordcloud_pos()
    
    #wordcloud negative sentiments
    @st.cache(hash_funcs={matplotlib.figure.Figure: lambda _: None})
    def wordcloud_neg ():
        fig, ax = plt.subplots() 
        super = dataset.loc[:,["tweets","airline_sentiment"]]
        text = "".join(super[super.airline_sentiment == "negative"].tweets)
        wc= WordCloud(max_words = 4000,background_color = "white").generate(text)
        ax.imshow(wc,interpolation='bilinear')
        plt.title("most occuring negative words", fontsize = 13)
        plt.axis("off")
        return fig
    plot2 = wordcloud_neg()
    
    # count of customer tweets by airline'
    @st.cache(hash_funcs={matplotlib.figure.Figure: lambda _: None})
    def tweet_count ():
            fig, ax = plt.subplots(figsize =(10,5)) 
            dataset.loc[:,["airline","airline_sentiment"]].groupby("airline").count().plot(kind = "bar", ax= ax)
            plt.title("count of customer tweets by airline", fontsize = 13);
            return fig
    plot3 = tweet_count ()
    
    
    # sentiment % by airlines 
    @st.cache(hash_funcs={matplotlib.figure.Figure: lambda _: None})
    def perc_sentiment ():        
        fig, ax = plt.subplots(figsize =(4,4))
        dataset.airline_sentiment.value_counts().plot(kind = "pie", autopct = "%.2f%%", explode = (0.02,0.02,0.02)  )
        plt.title("sentiment % by airlines across airlines- pie chart", fontsize = 13)
        plt.axis("off")
        return fig
    plot4= perc_sentiment ()
    

    # sentiments by airline
    @st.cache(hash_funcs={matplotlib.figure.Figure: lambda _: None})
    def sent ():            
        fig, ax = plt.subplots(figsize =(10,5))        
        pd.crosstab(dataset.airline, dataset.airline_sentiment).plot( kind = "bar", ax = ax)
        plt.title("sentiment by airlines - bar graph" , fontsize = 13);
        return fig
    plot5= sent()




    if option  == "positive key words":
        plot1
    elif  option == "negative key words":
        plot2
    elif option == "count of tweets by airline":
        plot3
    elif option == "distribution of sentiments(pie chart)" :
        plot4
    else:
        plot5