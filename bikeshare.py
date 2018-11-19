import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
"""
Iterating through city data in order to get a list of available cities to be checked in get_filters
Returns: List of cities
"""

city_names = []

for key, value in CITY_DATA.items():
    city_names.append(key)

"""
Iterating through the dataframe in order to get a de-duplicated list of all given months in the csv\'s of CITY_LIST
Returns: De-duplicated list of months
"""

months_list = []

for key, value in CITY_DATA.items():
    df = pd.read_csv(value)
    df['Month'] = pd.to_datetime(df['Start Time']).dt.month.apply(lambda x: calendar.month_name[x])
    months_list = df['Month'].unique()

"""
Iterating through the dataframe in order to get a de-duplicated list of all given weekdays in the csv's of CITY_LIST
Returns: De-duplicated list of days
"""

day_of_weeks = []

for key, value in CITY_DATA.items():
    df = pd.read_csv(value)
    df['DoW'] = pd.to_datetime(df['Start Time']).dt.weekday_name
    day_of_weeks = df['DoW'].unique()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Hi there! Would you like to see data for Chicago, New York City or Washington: ').lower()
            if city in city_names:
                break
            else:
                print('That is not a valid City name. Please try again')
        except KeyboardInterrupt:
            print('not moving forward')
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('So which month would you like to analye? Please provide month (January or December e.g.) or enter all for the entirety: ').title()
            if month in months_list:
                break
            elif month == 'All':
                break
            else:
                print('That is not a valid month! Please try again')
        except KeyboardInterrupt:
            print('not moving forward')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Is there a specific day you want this analysis to be based on? Please enter the day of the week (e.g. Sunday) or enter all: ').title()
            if day in day_of_weeks:
                break
            elif day == 'All':
                break
            else:
                print('That is not a valid day. Please try again')
        except KeyboardInterrupt:
            print('not moving forward')


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.time
    df['month'] = df['Start Time'].dt.month.apply(lambda x: calendar.month_name[x])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['station_combination'] = df['Start Station'] + ' - ' + df['End Station']
    if month != 'All':
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('\nThe most common month is: ',common_month)

    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('\nThe most common week day is: ',common_day_of_week)
    # TO DO: display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('\nThe most common hour is: ',common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('\nThe most common start station is: ', common_start_station)
    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nThe most common used end station is: ',common_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    common_station_combination = df.groupby(['Start Station', 'End Station']).count().idxmax()
    print('\nThe most common station combination is: ',common_station_combination)
  # data.groupby(['Year', 'Department'])['Salary'].sum()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""


    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_days = int(total_travel_time / (60*24))
    print('\nTotal Trip Duration in days was: ', total_travel_days)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_days = round((mean_travel_time / 60),1)
    print('\nAverage Trip Duration in minutes was: ', mean_travel_days)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_count_subscriber = df['User Type'].value_counts()['Subscriber']
    user_count_customer = df['User Type'].value_counts()['Customer']
    print('\nThere are several types of customers: There are {} subscribers and {} customers'.format(user_count_subscriber,user_count_customer))

    # TO DO: Display counts of gender
    try:
        male_count = df['Gender'].value_counts()['Male']
        female_count = df['Gender'].value_counts()['Female']
        print('\nThe distribution of genders is as follows. There are {} females and {} males'.format(female_count,male_count))
        # TO DO: Display earliest, most recent, and most common year of birth
        early_birth = int(df['Birth Year'].min())
        print('\nOur oldest cyclist were born in: ', early_birth)

        recent_birth = int(df['Birth Year'].max())
        print('\nOur youngest cyclist were born in: ', recent_birth)

        most_birth = int(df['Birth Year'].mean())
        print('\nIn average our cyclist were born in: ', most_birth)

    except KeyError:
        print('\nNo gender and birth information available unfortunately')
    finally:
        print('')


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

        while True:
            raw_data_read = input('\nWould you like to scroll through the raw data? Enter yes or no: ')
            if raw_data_read.lower() == 'yes' or raw_data_read.lower() == '':

                while True:
                    try:
                        amount_lines = int(input('\nHow many lines would you like to see. Enter a number: '))
                        print(df.head(amount_lines))
                        break
                    except ValueError:
                        print('\nThat\'s not a number :) Please enter a number: ')

                while True:
                    scroll_further = str(input('\nWould you like to see 5 more lines raw data? Enter yes or no: '))
                    if scroll_further != 'yes':
                        break
                    else:
                        amount_lines += 5
                        print(df.head(amount_lines))
            break

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
