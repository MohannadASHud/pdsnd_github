import pandas as pd
import numpy as np
import time



CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'}


chicago_df = pd.read_csv('chicago.csv')

new_york_df = pd.read_csv('new_york_city.csv')

washington_df = pd.read_csv('washington.csv')



chicago_df['Start Time'] = pd.to_datetime(chicago_df['Start Time'])
new_york_df['Start Time'] = pd.to_datetime(new_york_df['Start Time'])



for df in [chicago_df, new_york_df]:
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour



new_york_df[['Start Time', 'month', 'day_of_week', 'hour']].head()



def popular_times(df, city_name):
    print(f"\n--- Popular Times of Travel in {city_name} ---")

    most_common_month = df['month'].mode()[0]
    print(f"Most Common Month: {most_common_month}")

    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {most_common_day}")

    most_common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {most_common_hour}")





def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city, month, day
    """
    print("Hello! Let's explore some US bikeshare data!")

    # City input
    while True:
        city = input("enter city (Chicago, New York City, Washington) (type 'exit' to quit): ").strip().lower()
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



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break




def round_trip_stats(df):
    total_trips = len(df)
    round_trips = df[df['Start Station'] == df['End Station']]
    round_trip_count = len(round_trips)

    if total_trips > 0:
        percent = round_trip_count / total_trips * 100
        print(f"{round_trip_count} out of {total_trips} trips ({percent:.2f}%) are round trips.")
    else:
        print("No data available to compute round trip statistics.")






def busiest_day_hour_combo(df):
    combo = df.groupby(['day_of_week', 'hour']).size().reset_index(name='trip_count')

    busiest = combo.loc[combo['trip_count'].idxmax()]

    print(f"The busiest day and hour in Washington is:")
    print(f"  {busiest['day_of_week'].title()} at {busiest['hour']}:00")
    print(f"  Total rides: {busiest['trip_count']}")





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




main()