#!/usr/bin/env python
# coding: utf-8

# In[1]:


##SETUP 
import pandas as pd
csv_path="HeroesOfPymoli.csv"
data_pd=pd.read_csv(csv_path)

#SHOW COLUMN NAMES IN CSV
#data_pd.count() to show that no clean up was needed
#data head to show columns
data_pd.head()


# In[2]:


#1 TOTAL PLAYER COUNT
player_count=len(data_pd["SN"].unique())
player_count

#new data frame
total_players_df=pd.DataFrame({"Total Players": [player_count]})

#print dataframe
total_players_df


# In[3]:


#2 PURCHASING ANALYSIS(total)
number_unique_item=len(data_pd["Item Name"].unique())
average_price = data_pd["Price"].mean() #format price
number_of_purchases=data_pd["Purchase ID"].count()
total_revenue=data_pd["Price"].sum() #format this to have price

#new data frame
purchasing_analysis_df = pd.DataFrame({"Number of Unique Items": [number_unique_item],
                              "Average Price": [average_price],
                              "Number of Purchases": [number_of_purchases],
                              "Total Revenue": [total_revenue]})

#formatting
purchasing_analysis_df["Average Price"]=purchasing_analysis_df["Average Price"].map("${:,.2f}".format)
purchasing_analysis_df["Total Revenue"]=purchasing_analysis_df["Total Revenue"].map("${:,.2f}".format)

#print dataframe
purchasing_analysis_df


# In[4]:


#3 GENDER DEMOGRAPHICS (percentage and count by gender)
refined_sn=data_pd.drop_duplicates(subset="SN")

gender_counter=refined_sn["Gender"].value_counts()
gender_percentages=(gender_counter)/(player_count)

#new data frame
gender_df = pd.DataFrame({ "Total Count": gender_counter,
                        "Percentage of Players": gender_percentages,})

#formatting
gender_df["Percentage of Players"] = gender_df["Percentage of Players"].map("{:,.2%}".format)

#print data frame
gender_df


# In[5]:


#4 PURCHASING ANALYSIS (gender)
#purchase count,average purchase price, total purchase value and ave purchase total per person by gender
gender_purchase_count=data_pd.groupby(['Gender']).count()["Price"]
gender_average_price=data_pd.groupby(["Gender"]).mean()["Price"]
gender_total=data_pd.groupby(["Gender"]).sum()["Price"]
gender_average_total=gender_total/gender_df["Total Count"]

#new data frame
gender_purchasing_analysis_df=pd.DataFrame({"Purchase Count": gender_purchase_count,
                                         "Average Purchase Price": gender_average_price,
                                         "Total Purchase Value": gender_total,
                                         "Avg Total Purchase per Person": gender_average_total})
#formatting
gender_purchasing_analysis_df["Average Purchase Price"]=gender_purchasing_analysis_df["Average Purchase Price"].map("${:,.2f}".format)
gender_purchasing_analysis_df["Total Purchase Value"]=gender_purchasing_analysis_df["Total Purchase Value"].map("${:,.2f}".format)
gender_purchasing_analysis_df["Avg Total Purchase per Person"]=gender_purchasing_analysis_df["Avg Total Purchase per Person"].map("${:,.2f}".format)

#print data frame
gender_purchasing_analysis_df


# In[6]:


#5 AGE DEMOGRAPHICS:(find youngest & oldest)
print(data_pd["Age"].min())
print(data_pd["Age"].max())


# In[7]:


age_demographics=data_pd.drop_duplicates(subset="SN")


# In[8]:


#create bins & bin labels (youngest(7)-oldest(45)
bins=[0,9.9,14.9,19.9,24.9,29.9,34.9,39.9,50]
age_bin_labels=["<10","10-14","15-19","20-24","25-29","30-34","35-39","40+"]

age_demographics["Age Group"]= pd.cut(age_demographics["Age"], bins, labels=age_bin_labels)

age_group_totals=age_demographics["Age Group"].value_counts()
age_group_percentages=age_group_totals/player_count

age_demographics=pd.DataFrame({"Total Count" : age_group_totals, "Percentage of Players": age_group_percentages})

#formatting
age_demographics["Percentage of Players"] = age_demographics["Percentage of Players"].map("{:,.2%}".format)

#print data frame
age_demographics.sort_index()


# In[9]:


#6 PURCHASING ANALYSIS(AGE) 
purchasing_analysis_age["Age Group"] = pd.cut(purchasing_analysis_age["Age"], bins, labels=age_bin_labels, include_lowest=True)

age_purchase_count = purchasing_analysis_age.groupby(["Age Group"]).count()["Price"]
average_purchase_price = purchasing_analysis_age.groupby(["Age Group"]).mean()["Price"]
total_purchase = purchasing_analysis_age.groupby(["Age Group"]).sum()["Price"]
average_total_purchase = total_purchase / age_group_totals

# new data frame
age_purchase_df = pd.DataFrame({"Purchase Count": age_purchase_count,
                                "Average Purchase Price": average_purchase_price,
                                "Total Purchase Value": total_purchase,
                                "Avg Total Purchase per Person": average_total_purchase})
#formatting
age_purchase_format_dict = {"Average Purchase Price": "${0:,.2f}",
                            "Total Purchase Value": "${0:,.2f}",
                            "Avg Total Purchase per Person": "${0:,.2f}"}
age_purchase_df.index.name = "Age Range"

#print data frame
age_purchase_df.sort_index().style.format(age_purchase_format_dict)


# In[10]:


#7 TOP SPENDERS
grouped_SN_df = data_pd.groupby (['SN'])

SN_total_purchase_price= grouped_SN_df["Price"].sum()
SN_purchase_count = grouped_SN_df["SN"].count()
SN_average_purchase = grouped_SN_df["Price"].mean()

#new data frame 
SN_table = pd.DataFrame({"Total Purchase Value":SN_total_purchase_price,
                           "Average Purchase Price":SN_average_purchase,
                           "Purchase Count":SN_purchase_count})

SN_summary = pd.DataFrame(SN_table.nlargest(5,'Total Purchase Value'))
SN_top5 = SN_summary[["Purchase Count","Average Purchase Price","Total Purchase Value"]]

#formatting
SN_top5 ["Average Purchase Price"] = SN_top5 ["Average Purchase Price"].map("${:,.2f}".format)
SN_top5 ["Total Purchase Value"] = SN_top5 ["Total Purchase Value"].map("${:,.2f}".format)

#print data frame
SN_top5


# In[11]:


#8 MOST POPULAR ITEMS (Identify 5 most popular items by purchase count and list:Item ID, Item Name, Item Price)

popular_item_df = data_pd.groupby (['Item ID','Item Name'])

item_price = popular_item_df["Price"].sum()/popular_item_df["Item ID"].count()
item_purchase_count = popular_item_df["Item ID"].count()
price_sum = popular_item_df["Price"].sum()

item_table=pd.DataFrame({"Purchase Count":item_purchase_count,
                        "Total Purchase Value":price_sum,
                        "Item Price":item_price})

#new data frame
item_summary=pd.DataFrame(item_table.nlargest(5,'Total Purchase Value'))
item_top5 = item_summary[["Purchase Count","Item Price","Total Purchase Value"]]

#formatting
item_top5 ["Total Purchase Value"] = item_top5 ["Total Purchase Value"].map("${:,.2f}".format)
item_top5 ["Item Price"] = item_top5 ["Item Price"].map("${:,.2f}".format)

#print data frame
item_top5


# In[12]:


#9 MOST PROFITABLE ITEM

#new data frame
profitable_summary=pd.DataFrame(item_table.nlargest(5,'Total Purchase Value'))
most_profitable = profitable_summary[["Purchase Count","Item Price","Total Purchase Value"]]

#formatting
most_profitable ["Total Purchase Value"] = most_profitable ["Total Purchase Value"].map("${:,.2f}".format)
most_profitable["Item Price"] = most_profitable ["Item Price"].map("${:,.2f}".format)

#print data frame
most_profitable


# In[ ]:





# In[ ]:




