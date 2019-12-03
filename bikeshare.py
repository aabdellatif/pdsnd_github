import time
import pandas as pd
import numpy as np
import sys

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

    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

    city = ""
    month = ""
    day = ""

    print('Hello! Let\'s explore some US bikeshare data!\n')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city.lower() not in cities:
        city = input("Which city would you like to choose: Chicago, New York City, or Washington?\n")

    # Get user input for month (all, january, february, ... , june)
    while month.lower() not in months:
        month = input("What month would you like to filter by? Type either 'January', 'February', etc. Type 'all' if you don't want to filter by month.\n")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while day.lower() not in days:
        day = input("What day would you like to filter by? Type either 'Sunday', 'Monday', etc. Type 'all' if you don't want to filter by day.\n")

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

    city = city.lower()
    month = month.lower()
    day = day.lower()

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    if df.empty:
        sys.exit("You must have filtered on something that didn't exist in the table, causing an empty table. Exiting program. Please restart the script.")

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    if df['month'].nunique() != 1:
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        print("The most common month: ", months[df['month'].mode()[0] - 1], "\n")


    # Display the most common day of week
    if df['day_of_week'].nunique() != 1:
        print("The most common day of the week: ", df['day_of_week'].mode()[0], "\n")

    # Display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour: ", df['hour'].mode()[0], "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("The most commonly used start station: ", df['Start Station'].mode()[0], "\n")

    # Display most commonly used end station
    print("The most commonly used end station: ", df['End Station'].mode()[0], "\n")

    # Display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + " / " + df['End Station']
    print("The most frequent combination of start station and end station trip: ", df['Station Combo'].mode()[0], "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("The total travel time is: ", int(df['Trip Duration'].sum()), " seconds\n")

    # Display mean travel time
    print("The average travel time is: ", int(df['Trip Duration'].mean()), " seconds\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n", df['User Type'].value_counts(), "\n")

    try:
        # Display counts of gender
        print("Counts of gender:\n", df['Gender'].value_counts(), "\n")

        # Display earliest, most recent, and most common year of birth
        print("Earliest year of birth: ", int(df['Birth Year'].min()), "\n")
        print("Most recent year of birth: ", int(df['Birth Year'].max()), "\n")
        print("Most common year of birth: ", int(df['Birth Year'].mode()[0]), "\n")
    except KeyError:
        return
    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def raw_data_request(df):
    """ Prompts the user if they want to see 5 lines of the data """
    answer = input("\nDo you want to see the first 5 lines of the data? y/n (Other inputs will be considered a no.)\n")
    if answer == "y" or answer == "yes":
        print(df.head(5))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data_request(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
