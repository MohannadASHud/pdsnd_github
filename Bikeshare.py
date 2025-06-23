#!/usr/bin/env python
# coding: utf-8

# # Project: Explore US Bikeshare Data

# In[2]:


import pandas as pd
import numpy as np
import time


# In[3]:


CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'}


# ## 1. Importing Data
# ### Import Data from Chicago 

# In[5]:


chicago_df = pd.read_csv('chicago.csv')
chicago_df.info()


# In[6]:


print("Chicago Data:")
print(chicago_df.head(), '\n')


# ### Import Data from New York

# In[8]:


new_york_df = pd.read_csv('new_york_city.csv')
new_york_df.info()


# In[9]:


print("New York City Data:")
print(new_york_df.head(), '\n')


# ### Import Data from  Washington

# In[11]:


washington_df = pd.read_csv('washington.csv')
washington_df.info()


# In[12]:


print("Washington Data:")
print(washington_df.head())


# ## 2. Conversions and Extractions 
# ### 2.1 Convert Start Time to datetime format

# In[14]:


chicago_df['Start Time'] = pd.to_datetime(chicago_df['Start Time'])
new_york_df['Start Time'] = pd.to_datetime(new_york_df['Start Time'])


# ### 2.2 Extracting features from Start Time

# In[16]:


for df in [chicago_df, new_york_df]:
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


# In[17]:


new_york_df[['Start Time', 'month', 'day_of_week', 'hour']].head()


# ### 2.3 Most Common Time Stats

# In[19]:


def popular_times(df, city_name):
    print(f"\n--- Popular Times of Travel in {city_name} ---")
    
    most_common_month = df['month'].mode()[0]
    print(f"Most Common Month: {most_common_month}")
    
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {most_common_day}")
    
    most_common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {most_common_hour}")


# In[20]:


popular_times(chicago_df, 'Chicago')
popular_times(new_york_df, 'New York City')


# ## 3. Adding Filters
# ### 3.1 Creating City, Month & Day of The Week Filters

# In[86]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city, month, day
    """
    print("Hello! Let's explore some US bikeshare data!")
  
    # City input
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? (type 'exit' to quit): ").strip().lower()
        if city == 'exit':
            print("Exiting program. Goodbye!")
            exit()  # Ends the program
        elif city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Invalid input. Please enter a valid city name.")

    # Month input
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Choose a month (January to June) or 'all': ").strip().lower()
        if month == 'exit':
            print("Exiting program. Goodbye!")
            exit()
        elif month in months:
            break
        print("Invalid input. Please try again.")

    # Day input
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Choose a day of week or 'all': ").strip().lower()
        if day == 'exit':
            print("Exiting program. Goodbye!")
            exit()
        elif day in days:
            break
        print("Invalid input. Please try again.")

    print('-'*40)
    return city, month, day


# ### 3.2 Loading Data

# In[24]:


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]

    # Filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


# ### 3.3 Testing the Filters
# #### 3.3.1 Test 1

# In[26]:


city = 'washington'
month = 'april'
day = 'tuesday'

df = load_data(city, month, day)
df.head()


# In[27]:


print(df['month'].unique())
print(df['day_of_week'].unique())


# #### 3.3.2 Test 2

# In[29]:


city = 'chicago'
month = 'january'
day = 'saturday'

df = load_data(city, month, day)
df.head()


# In[30]:


print(df['month'].unique())
print(df['day_of_week'].unique())


# ## 4. Calculating Most Common 
# ### 4.1 Most Common Time

# In[32]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    print(f"Most Common Month (1 = Jan ... 6 = Jun): {most_common_month}")

    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {most_common_day.title()}")

    most_common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {most_common_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

time_stats(df)


# ### 4.2 Most Common Station

# In[34]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {start_station}")

    end_station = df['End Station'].mode()[0]
    print(f"Most Common End Station: {end_station}")

    # Most common start and end station
    df['Trip Combo'] = df['Start Station'] + " → " + df['End Station']
    common_trip = df['Trip Combo'].mode()[0]
    print(f"Most Common Trip: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

station_stats(df)


# ### 4.3 Most Common Trip Duration

# In[36]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_duration} seconds ({total_duration / 3600:.2f} hours)")

    average_duration = df['Trip Duration'].mean()
    print(f"Average Travel Time: {average_duration:.2f} seconds ({average_duration / 60:.2f} minutes)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

trip_duration_stats(df)


# ### 4.4 Most Common User Stats

# In[38]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("User Types:\n", user_types.to_string(), "\n")

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Gender Counts:\n", gender_counts.to_string(), "\n")
    else:
        print("Gender data not available for this city.\n")

    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        latest_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"Earliest Birth Year: {earliest_year}")
        print(f"Most Recent Birth Year: {latest_year}")
        print(f"Most Common Birth Year: {most_common_year}")
    else:
        print("Birth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

user_stats(df)


# ## 5. Display Raw Data

# In[40]:


def display_raw_data(df):
    """Displays 5 rows of raw data upon user request."""
    start_loc = 0
    while True:
        view_data = input("\nWould you like to see 5 rows of raw data? Enter yes or no: ").strip().lower()
        if view_data != 'yes':
            break
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        if start_loc >= len(df):
            print("No more data to display.")
            break


# In[41]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


# In[42]:


df = load_data('washington', 'april', 'tuesday')
display_raw_data(df)


# ## 6. Answering Interesting Questions
# ### 6.1 What percentage of trips are round trips?

# In[44]:


def round_trip_stats(df):
    total_trips = len(df)
    round_trips = df[df['Start Station'] == df['End Station']]
    round_trip_count = len(round_trips)
    
    if total_trips > 0:
        percent = round_trip_count / total_trips * 100
        print(f"{round_trip_count} out of {total_trips} trips ({percent:.2f}%) are round trips.")
    else:
        print("No data available to compute round trip statistics.")

round_trip_stats(df)


# ### 6.2 Which day and hour combo has the highest number of rides?

# In[46]:


def busiest_day_hour_combo(df):
    combo = df.groupby(['day_of_week', 'hour']).size().reset_index(name='trip_count')

    busiest = combo.loc[combo['trip_count'].idxmax()]

    print(f"The busiest day and hour in Washington is:")
    print(f"  {busiest['day_of_week'].title()} at {busiest['hour']}:00")
    print(f"  Total rides: {busiest['trip_count']}")

busiest_day_hour_combo(df)


# In[47]:


import seaborn as sns
import matplotlib.pyplot as plt

def plot_day_hour_heatmap(df, city_name=''):
    heatmap_data = df.groupby(['day_of_week', 'hour']).size().unstack(fill_value=0)

    day_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    heatmap_data = heatmap_data.reindex(day_order)

    plt.figure(figsize=(14, 6))
    sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.5, annot=False)

    city_title = city_name.title() if city_name else "the City"
    plt.title(f'Number of Trips by Day and Hour in {city_title}', fontsize=14, pad=12)
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')

    plt.tight_layout()
    plt.show()
plot_day_hour_heatmap(df, city_name='washington')


# In[48]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("Would you like to restart? Enter yes or no: ").lower()
        if restart != 'yes':
            print("Goodbye! 🚲")
            break


# In[49]:


main()


# In[ ]:




