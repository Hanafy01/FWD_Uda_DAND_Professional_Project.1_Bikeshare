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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
      city = str(input("Enter the city targeted for data analysis  : ")).lower()
      if city not in CITY_DATA:
            print('Sorry...you did not enter a city in the focus of our study')
            continue
      break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march', 'april', 'may','june','all']
        month = str(input("Enter the targeted month   : ")).lower()
        if month not in months:
              print('Sorry...you did not enter a valid month')
              continue
        break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
          days = ['friday', 'saturday', 'sunday', 'monday', 'tuesday' , 'wednesday','thursday','all']
          day = str(input("Enter the targeted day of week : ")).lower()
          if day not in days:
                print('Sorry...you did not enter a valid day')
                continue
          break
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

    df['Start Time'] = pd.to_datetime(df['Start Time'] )

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
       months = ['january', 'february', 'march', 'april', 'may', 'june']
       month = months.index(month) + 1
       df = df[df['month'] == month]
    if day != 'all':

       df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    Common_Month = df['month'].value_counts().idxmax()
    print('Most Common Month:', Common_Month)
    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    common_day = df['day_of_week'].value_counts().idxmax()
    print('The most common day of week:', common_day)
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    c_start_hour = df['hour'].value_counts().idxmax()
    print('The most common start hour:', c_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    com_u_start_station = df["Start Station"].value_counts().idxmax()
    print('The most commonly used start station :' , com_u_start_station)
    # TO DO: display most commonly used end station
    com_u_end_station = df["End Station"].value_counts().idxmax()
    print('The most commonly used end station :' , com_u_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    start_end_station = df.groupby(["Start Station"])["End Station"].value_counts().idxmax()
    print('The most frequent combination of start station and end station trip :' , start_end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['total_travel_time'] = df['End Time']-df['Start Time']
    print('Total travel time : ' , df['total_travel_time'])
    # TO DO: display mean travel time
    print('The mean travel time : ' , df['total_travel_time'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('The counts of user types are : ' , user_counts)
    # TO DO: Display counts of gender
    try:
       gender_counts =  df['Gender'].value_counts()
       print('The counts of gender : ' , gender_counts)
    except:
          print('Genders data is only available in  Chicago and New York City files')

    # TO DO: Display earliest, most recent , and most common year of birth
    # most recent according to month
    try:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['earliest_hour'] = df['Start Time'].dt.hour.sort_values(ascending=True)
        df['most_recent'] = df['Start Time'].dt.month.sort_values(ascending=True)
        com_birth_year =  df.groupby(['earliest_hour','most_recent' ])['Birth Year'].value_counts().idxmax()
        print('The earliest, most recent , and most common year of birth : ' , com_birth_year )


    except:
          print('Birth years data is only available in  Chicago and New York City files')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        j = 0
        k = 5
        while True:
              df_copy = df.copy().iloc[j:k , :]
              time_stats(df_copy )
              station_stats(df_copy )
              trip_duration_stats(df_copy )
              user_stats(df_copy )
              next_5 = input('\nWould you like to display next 5 rows? Enter yes or no.\n')
              if next_5 == 'yes':
                 j += 5
                 k += 5
                 continue
              break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
           break


if __name__ == "__main__":
	main()
