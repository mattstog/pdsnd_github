import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington) using a while loop to handle invalid inputs
    city = ''
    while(city.lower() not in CITY_DATA):
        city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()
    
    print('Great, I Love ' + city.title() + '!\n')

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = ''
    while(month not in months):
        month = input('Which month would you like to see? \nChoose from this list: [All, January, February, March, April, May, June] ').lower()
    
    print(month.title() + ' is my favorite month!\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Which day would you like to see? \nChoose from this list: [All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday] ').lower()
    if(day != 'all'):
        print(day.title() + 's are the best\n')
    else:
        print('\n')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Reading in the df for the city input
    df = pd.read_csv(CITY_DATA[city])    

    # Cleaning up the datetime data
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day'] = pd.to_datetime(df['Start Time']).dt.weekday_name


    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].mode()[0]
    print('The most common month was ' + str(month))

    # display the most common day of week
    day = df['day'].mode()[0]
    print('The most common day of the week was ' + day)

    # display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    hour = df['hour'].mode()[0]
    print('the most common start hour was ' + str(hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts()
    print('The most commonly used start station was ' + start_station.index[0])

    # display most commonly used end station
    end_station = df['End Station'].value_counts()
    print('The most commonly used end station was ' + end_station.index[0])

    # display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + " TO " + df['End Station']
    start_end_station = df['start_end_station'].value_counts()
    print('The most frequent combination of start station and end station trip was ' + start_end_station.index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).dt.seconds.sum()
    print('The total travel time was ' + str(total_travel_time) + ' seconds')

    # display mean travel time
    average_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).dt.seconds.mean()
    print('The average travel time was ' + str(average_travel_time) + ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types: ')
    print(user_types)

    # Display counts of gender
    genders = df['Gender'].value_counts()
    print('\nGender counts: ')
    print(genders)

    # Display earliest, most recent, and most common year of birth
    earliest_year = int(df['Birth Year'].min())
    print('\nThe earliest year of birth was ' + str(earliest_year))

    recent_year = int(df['Birth Year'].max())
    print('\nThe most recent year of birth was ' + str(recent_year))

    common_year = int(df['Birth Year'].mode()[0])
    print('\nThe most common year of birth was ' + str(common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
