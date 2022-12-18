import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """Check user's inputs for a given inputs
    Args:
        check_input (string): Request inputs for the three inputs
        check_type (int): attached to each inputs different number
    """
    print('\nHello! Let\'s explore some US BikeShare data!\n')
    # We get user input for city (chicago, new york city, washington).
    # We used a while loop to handle invalid inputs as in CITY_DATA dictionary.
    city = input("Please enter a city name (Chicago, New York City, Washington) \n \n: ").lower()
    while city not in CITY_DATA.keys():
        print("Please enter a city name from listed above.")
        city = input("Try again, as follows (Chicago, New York City, or Washington) \n \n : ").lower()

    # We get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("\n \nPlease enter a month name (January, February, March, April, May, June, or All) \n \n: ").lower()
        if month in months:
            break
        else:
            print("Try again, please enter a month name from above list.")

    # We get user input for day of week
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    # We used a while loop (Check True)to handle the invalid input as in days above.
    while True:
        day = input("\n \nPlease enter a day name:\n(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All) \n \n: ").lower()
        if day in days:
            break
        else:
            print("Try again, please enter a day name as mentioned above.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    # Read from CSV data file and return as a user inputs
    df = pd.read_csv(CITY_DATA[city])
    # Get Start time column extract month, day and hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    # use if statement to exclude "ALL" from month names list
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # use if statement to exclude "All" from day names list
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

#1 Popular times of travel (The Most Common)
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time() # Start time is the current time

    # Display the most common month, day, and hour to the specified city.
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = df['month'].mode()[0]
    results_list = {'The Most Common': ['Most common Month is:', 'Most common Day is:', 'Most common Hour is :'],
             'Results': [ months[month-1].title() , df['day_of_week'].mode()[0], df['Start Hour'].mode()[0] ]}
    index_labels = ['R1' , 'R2', 'R3']
    df_list = pd.DataFrame(results_list, index= index_labels)
    print(df_list)
    
    # Display time taken by subtracting current time from start time
    print("\nThese calculations took %s seconds."% round((time.time() - start_time), 6))
    print('-'*60)

#2 Popular stations and trip (Most Common)
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time() # Start time is the current time
    # Display most commonly used Start and End station
    popular_combo_stations = df['Start Station'] +" -> "+ df['End Station']
    results_list = {'The Most Popular': ['Most common Start station is:', 'Most common End station is:', 'Popular Start & End station is:'],
             'Results': [ df['Start Station'].mode()[0] , df['End Station'].mode()[0], popular_combo_stations.head(1)]}
    index_labels = ['R1' , 'R2', 'R3']
    df_list = pd.DataFrame(results_list, index= index_labels)
    print(df_list)
    
    # Display time taken by subtracting current time from starting time
    print("\nThese calculations took %s seconds." % round((time.time() - start_time), 6))
    print('-'*60)

#3 Trip duration
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time() # Start time is the current time
    # Display total travel time by using SUM total time (seconds / 60 ) spent in all trips and round it.
    print('Display total travel time (hours): ', f"{round(((df['Trip Duration'].sum())/ 60), None): ,}", 'hours')
    # Display average travel time by using MEAN time (hours) spent in all trips and round it.
    print('Display mean travel time (hours): ', round(((df['Trip Duration'].mean())/ 60), 2), 'hours')
    # Display average travel time by using Min time (hours) spent in all trips and round it.
    print('Display minimum travel time (hours): ', round(((df['Trip Duration'].min())/ 60), 2), 'hours')
    # Display time taken by subtracting current time from start time.
    print("\nThese calculations took %s seconds." % round((time.time() - start_time), 6))
    print('-'*60)

#4 User info
def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()# Start time is the current time

    # Display counts of user types (membership)
    print('\nDisplay counts of membership user types (persons):')
    print(df['User Type'].value_counts().to_frame())
    # Display counts of user types (membership)
    print('\nDisplay percentage of membership user type (Percent):\n')
    print(df.loc[:,'User Type'].value_counts('Subscriber')*100)
    # Display counts of gender , except washington city (no gender column)
    print('\nDisplay counts of gender user type (persons):')
    if city != "washington":
        print('\n',df['Gender'].value_counts().to_frame())
        # Display percentage of gender , except washington city (no gender column)
        print('\nDisplay percentage of gender user type (percent):\n')
        print(df.loc[:,'Gender'].value_counts('Male')*100)
    # Display earliest, most recent, and most common year of birth
        print('\nDisplay earliest, most recent, and most common year of birth:')
        print('\nMost common year of birth is: ', int(df['Birth Year'].mode()[0]))
        print('Most recent year of birth is: ', int(df['Birth Year'].max()))
        print('The Earliest year of birth is: ', int(df['Birth Year'].min()))
    else:
        print('\nNo data available for {} city.'.format(city))
    # Display time taken by subtracting current time from start time
    print("\nThese calculations took %s seconds." % round((time.time() - start_time), 5))
    print('-'*60)

def display_data(df, city):
    """Displays Raw data for a given city"""

    print("\nRaw data available to display...\n")
    
    more_input = input('If you need to display more 5 rows of raw data type Yes, or Any to finish:  ').lower()
    if more_input == ('yes'):
        print('\nDisplaying Row Data...\n')
        counter = 0 # row counter starting
        while True:
            print(df.iloc[counter : counter + 5]) # display rows by column labels + 5
            counter += 5
            print('\nDisplaying Row Data...\n')
            more_input = input('Show more 5 rows of raw data type Yes, or Any to finish:  ').lower()
            if more_input != ('yes'):
                break
                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df, city)

        restart = input('\nWould you like to restart? type Yes, or Any to finish.\n')
        if restart.lower() != 'yes':
            break
                
if __name__ == '__main__':
    main()
