#!/usr/bin/env python
# coding: utf-8

# > **Tip**: Welcome to the Investigate a Dataset project! You will find tips in quoted sections like this to help organize your approach to your investigation. Before submitting your project, it will be a good idea to go back through your report and remove these sections to make the presentation of your work as tidy as possible. First things first, you might want to double-click this Markdown cell and change the title so that it reflects your dataset and investigation.
# 
# # Project: Investigate a TMDb movie data
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# TMDb movie data is used as part of Udacity Data Analyst project.This data set contains information
# about 10,000 movies collected from the Movie Database (TMDb),including user ratings and revenue.Using the datasets, some questions were analysed such as trends over the years and profits etc.

# In[8]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import sys
sys.path
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > **Tip**: In this section of the report, you will load in the data, check for cleanliness, and then trim and clean your dataset for analysis. Make sure that you document your steps carefully and justify your cleaning decisions.
# 
# ### General Properties

# In[15]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv(r'C:/Users/Asus/Downloads/tmdb-movies.csv')
df.info()


# #### The file consists of 21 columns with 10866 entries.Null values are present in the following columns:imdb_id , cast , homepage , director , tagline , keywords , overview , genres , production_companies. Null columns will be removed and the data will be analysed for the questions mentioned above.
# 

# In[20]:


df.head()


# > **Tip**: You should _not_ perform too many operations in each cell. Create cells freely to explore your data. One option that you can take with this project is to do a lot of explorations in an initial notebook. These don't have to be organized, but make sure you use enough comments to understand the purpose of each code cell. Then, after you're done with your analysis, create a duplicate notebook where you will trim the excess and organize your steps so that you have a flowing, cohesive report.
# 
# > **Tip**: Make sure that you keep your reader informed on the steps that you are taking in your investigation. Follow every code cell, or every set of related code cells, with a markdown cell to describe to the reader what was found in the preceding cell(s). Try to make it so that the reader can then understand what they will be seeing in the following cell(s).
# 
# ### Data Cleaning (Replace this with more specific notes!)

# In[17]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.
print('Total rows and coulmns before data cleaning',df.shape)


# In[22]:


#checking whether there is null values
df.isnull().sum()


# In[24]:


#filtering of columns which is needed or useful for analysis of the data of the dataframe
filter_column=[ 'id', 'imdb_id', 'popularity', 'budget_adj', 'revenue_adj', 'homepage', 'keywords', 'overview', 'production_companies', 'vote_count', 'vote_average']

#storing the filtered column using drop()
movies=df.drop(filter_column,axis=1)
movies.head()


# In[26]:


#Removing duplicate objects
df.drop_duplicates(inplace=True)


# In[28]:


#Replace data which has 0 with NaN and Removing rows which has NaN for value in any column/row
df=df.replace(0,np.NaN)
df=df.dropna()


# In[29]:


#Converting the popularity, runtime, budget and revenue into integer values
df[['popularity','runtime','budget_adj', 'revenue_adj']] = df[['popularity','runtime','budget_adj', 'revenue_adj']].applymap(np.int64)


# In[31]:


df.insert(7,'profit',df['revenue_adj']-df['budget_adj'])


# In[32]:


print('Total rows and coulmns after data cleaning',df.shape)
df.info()


# In[34]:


#Saving the clean data into a separate file
df.to_csv(r'C:/Users/Asus/Downloads/clean_tmdb_data.csv', index=False)


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **Tip**: Now that you've trimmed and cleaned your data, you're ready to move on to exploration. Compute statistics and create visualizations with the goal of addressing the research questions that you posed in the Introduction section. It is recommended that you be systematic with your approach. Look at one variable at a time, and then follow it up by looking at relationships between variables.
# 
# ### Research Question 1 Popular movies over the years

# In[35]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.
def trend(column_x,column_y):
    #load clean data
    df = pd.read_csv(r'C:/Users/Asus/Downloads/clean_tmdb_data.csv')
    #set graph size
    plt.figure(figsize=(5,3), dpi = 120)
    #plotting the graph
    plt.plot(df.groupby(column_x)[column_y].sum())
    df.groupby(column_x)[column_y].sum().describe()
    max_value = df.groupby(column_x)[column_y].sum().idxmax()
    min_value = df.groupby(column_x)[column_y].sum().idxmin()
    return max_value,min_value,plt


# #### Finding the maximum and minimum profits over the years 

# In[38]:


maxm_value,minm_value,plt=trend('release_year','profit')
#x-axis label
plt.xlabel('Year of Release', fontsize = 10)
#y-axis label
plt.ylabel('Earned profits', fontsize = 10)
#title of the graph
plt.title('Profit margins over years')
plt.show()
print('Maximum profitable year',maxm_value)
print('Minimum profitable year',minm_value)


# ### The maximum and minimum profitable year was found to be 2015 and 1986 respectively. From the late 1990s there is a considerable increase in profits. While mid years of last two decades saw a considerable decrease as well.

# ### Research Question 2  Popularity trends over the years

# In[46]:


#x-axis label
maxm_value,minm_value,plt=trend('release_year','popularity')
plt.xlabel('Release Year', fontsize = 10)
#y-axis label
plt.ylabel('Popularity', fontsize = 10)
#title of the graph
plt.title('Trend of popular movies over the years')
plt.show()
print('Most Popular year for movies',maxm_value)
print('Least Popular year for movies',minm_value)


# #### As per the plot, the most and the least popular year for movies was found to be 2015 and 1961. In the 21st century the trend is increasing abruptly though a slight decrease was sighted in the mid 2010s.

# ### Research Question 3 How the revenue, profit and budget is related to the number of movies?

# In[44]:


figure = plt.figure(figsize=(10,6),dpi=150)


# In[47]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.
plt.hist([
        df['budget_adj'],df['revenue_adj'],df['profit']
        ], 
         stacked=False, color = ['r','b','g'],
         bins = 30,label = ['Budget','Revenue', 'Profit'])
###Labeling the graph : x-axis,y-axis and Title
plt.xlabel('Amount in USD')
plt.ylabel('Number of Movies')
plt.title(' Budget,Revenue and Profit distribution')
### Adding legend 
plt.legend()


# #### From the histogram plot, the budget have a sharp relation with the number of movies. Both budget and revenue are related.

# <a id='conclusions'></a>
# ## Conclusions
# 
# > **Tip**: Finally, summarize your findings and the results that have been performed. Make sure that you are clear with regards to the limitations of your exploration. If you haven't done any statistical tests, do not imply any statistical conclusions. And make sure you avoid implying causation from correlation!
# 
# > **Tip**: Once you are satisfied with your work, you should save a copy of the report in HTML or PDF form via the **File** > **Download as** submenu. Before exporting your report, check over it to make sure that the flow of the report is complete. You should probably remove all of the "Tip" quotes like this one so that the presentation is as tidy as possible. Congratulations!

# ####  In conclusion, the analysis showed the most and the least profitable years. Also, the trends of movies(over the years) in terms the most and the least popular are depicted. The budget, price and revenue with respect to number of movies were addressed showing a less clear picture in some aspects. This might be due to non-consistent values or there might be inaccuracy of information.
# 

# In[ ]:




