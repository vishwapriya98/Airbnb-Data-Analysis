import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import seaborn as sns
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
#---------------------------------------------------------------------------------------------------
#page configuration
st.set_page_config(page_title= "Airbnb Data Visualization | By VISHWA PRIYA",
                   #page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *vishwa*!
                                       # Data has been gathered from mongodb atlas"""}
                  )


# Set page configuration

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Overview","Explore"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                          )


#CONNECTING MYSQL
connect = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "98655",
    database="airbnb"
    )

    # Create a new database and use
mycursor = connect.cursor()
engine = create_engine('mysql+pymysql://root:98655@localhost/airbnb', echo=False)


# READING THE CLEANED DATAFRAME
df = pd.read_csv('Airbnb_data.csv')

# HOME PAGE
if selected == "Home":
    #col1,col2 = st.columns(2,gap= 'medium')
    st.markdown("## :blue[Domain] : Travel Industry, Property Management and Tourism")
    st.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    st.markdown("## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
    # st.markdown("#   ")
    # st.markdown("#   ")


if selected == "Overview":
    selected_value = st.selectbox("Select an option:", ["Average Price", "Availability"])
    if selected_value =="Average Price":

        col1,col2=st.columns(2)
        with col1:
            mycursor.execute("select Country,avg(Price)as AvgPrice from airbnb.data group by Country;")
            res=mycursor.fetchall()
            df1=pd.DataFrame(res, columns=['Country', 'AvgPrice']).reset_index(drop=True)
            df1.index += 1
        #print(df1)
            fig4= px.bar(df1,
                         title='Country and its Average Price',
                         x='Country',
                         y='AvgPrice',
                         orientation='v',
                         color='Country',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig4)
        with col2:
            mycursor.execute("select Property_type,avg(Price)as AvgPrice from airbnb.data group by Property_type;")
            res=mycursor.fetchall()
            df2=pd.DataFrame(res, columns=['Property_type', 'AvgPrice']).reset_index(drop=True)
            df2.index += 1
        #print(df1)
            fig= px.bar(df2,
                         title='Property_type and its Average Price',
                         x='Property_type',
                         y='AvgPrice',
                         orientation='v',
                         color='Property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig)
    if selected_value =="Availability":
        col1,col2=st.columns(2)
        with col1:
            mycursor.execute("select Room_type,sum(Availability_365)as Availability from airbnb.data group by Room_type;")
            res=mycursor.fetchall()
            df1=pd.DataFrame(res, columns=['Room_type', 'Availability']).reset_index(drop=True)
            df1.index += 1
            fig = px.pie(df1, names="Room_type", values="Availability")

            st.plotly_chart(fig)
            
        with col2:
            mycursor.execute("select country,sum(Availability_365)as Availability from airbnb.data group by Country;")
            res=mycursor.fetchall()
            df2=pd.DataFrame(res, columns=['Country','Availability']).reset_index(drop=True)
            df2.index += 1
            fig = px.bar(df2,
                         #title='Top 10 Property Types',
                         x='Country',
                         y='Availability',
                         orientation='v',
                         color='Availability',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True) 


     

        
if selected == 'Explore':
    select = st.selectbox('Select your Question',
        ['1. Top 10 Property_types based on country and room_type',
         '2. Top 10 Host_name based on Property_type and country',
         '3. Total number of listings for each room_type',
         '4. Average review score based on country, property_type, and room_type',
         '5. Relation between reviewscores and price'],
         key='collection_question')

    if select == '1. Top 10 Property_types based on country and room_type':
        col1, col2 = st.columns(2)

        with col1:
            country = st.selectbox('Select a Country', sorted(df.Country.unique()))
            room = st.selectbox('Select Room_type', sorted(df.Room_type.unique()))

            if country and room:
                query = """
                SELECT Country, Property_type, Room_type, COUNT(Property_type) AS CountProperty 
                FROM airbnb.data 
                WHERE Country = %s AND Room_type = %s 
                GROUP BY Country, Room_type, Property_type 
                ORDER BY CountProperty DESC 
                LIMIT 10;
                """

                mycursor.execute(query, (country, room))
                res = mycursor.fetchall()
                df1 = pd.DataFrame(res, columns=['Country', 'Property_type', 'Room_type', 'CountProperty']).reset_index(drop=True)

                df1.index += 1

                st.write(df1)

        with col2:
            fig = px.bar(df1,
                    title='Top 10 Property Types',
                    x='CountProperty',
                    y='Property_type',
                    orientation='h',
                    color='Property_type',
                    color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)
    
    if select == '2. Top 10 Host_name based on Property_type and country':
        col1, col2 = st.columns(2)

        with col1:
            country = st.selectbox('Select a Country', sorted(df.Country.unique()))
            if country:
                query="SELECT Country, Property_type, Host_name,count(Host_name) as Number FROM airbnb.data where Country=%s GROUP BY Country, Property_type,Host_name order by Number desc limit 10;"
                mycursor.execute(query,country)
                res1=mycursor.fetchall()
                df2 = pd.DataFrame(res1, columns=['Country', 'Property_type','Host_name',"Number"]).reset_index(drop=True)
                df2.index += 1
                st.write(df2)
        with col2:
            fig4 = px.sunburst(df2, path=['Property_type', 'Host_name'], values='Number',
                               color='Number', hover_data=['Number'],
                               color_continuous_scale='Jet',
                               )
            st.plotly_chart(fig4)
    
    if select=='3. Total number of listings for each room_type':
        col1, col2 = st.columns(2)
        with col1:
            country = st.selectbox('Select a Country', sorted(df.Country.unique()))
            if country:
                query="select Country,Room_type,count(Room_type) as Total from airbnb.data where country= %s group by Country ,Room_type ;"
                mycursor.execute(query,country)
                res4=mycursor.fetchall()
                df3 = pd.DataFrame(res4, columns=['Country', 'Room_type','Total']).reset_index(drop=True)
                df3.index += 1
                st.write(df3) 
        with col2:
            fig4= px.bar(df3,
                         title='Total Listings',
                         x='Room_type',
                         y='Total',
                         orientation='v',
                         color='Room_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)   
            st.plotly_chart(fig4)
            
    if select == '4. Average review score based on country, property_type, and room_type':
        col1, col2 = st.columns(2)

        with col1:
            country = st.selectbox('Select a Country', sorted(df.Country.unique()))
            room = st.selectbox('Select Room_type', sorted(df.Room_type.unique()))

            if country and room:
                query="select Country, Property_type, avg(Review_scores) as AverReviewScore FROM airbnb.data where Country=%s and room_type=%s GROUP BY Country, Property_type,Room_type order by AverReviewScore limit 10;"

                mycursor.execute(query,(country,room))
                res=mycursor.fetchall()
                df4= pd.DataFrame(res, columns=['Country', 'Property_type','AverReviewScore']).reset_index(drop=True)
                df4.index += 1
                st.write(df4)  
        
        with col2:
            


            labels = df4.Property_type
            sizes = df4.AverReviewScore
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')  
            st.pyplot(fig)
    if select=='5. Relation between reviewscores and price':
        mycursor.execute("select review_scores,price from airbnb.data;")
        res=mycursor.fetchall()
        df6= pd.DataFrame(res, columns=['Review_Scores', 'Price']).reset_index(drop=True)
        df6.index += 1
        

        fig, ax = plt.subplots()
        ax.scatter(df6['Review_Scores'], df6['Price'])

        # Add labels and title
        ax.set_xlabel('Review Scores')
        ax.set_ylabel('Price')
        ax.set_title('Scatter Plot of Review Scores vs Price')

        # Display the scatter plot in Streamlit
        st.pyplot(fig)

    
        
            
    
            