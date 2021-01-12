import time

import numpy as np
import pandas as pd
from pandas.core.algorithms import value_counts
from pandas.core.tools.datetimes import to_datetime

CITY_DATA = {
    "chicago": pd.read_csv("chicago.csv"),
    "new york": pd.read_csv("new_york_city.csv"),
    "washington": pd.read_csv("washington.csv")}
month_text = ["january", "february", "march", "april", "may", "june"]
day_text = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    # get user input for city (chicago, new york city, washington)
    print("Would you like to see data for Chicago, New York, or Washington?")
    while True:
        try:
            city = input("Please type the city name:").lower()
        except ValueError:
            print("That's not a valid input, please try again")
            continue
        else:
            if city not in CITY_DATA.keys():
                print("City out of range, please try again")
                continue
            else:
                break

    # ask user how they'd like to filter the date
    print('Would you like to filter the data by month, day, both, or "none" for no time filter?')
    while True:
        try:
            date_filter = input("Specify the date filter:").lower()
        except ValueError:
            print("That's not a valid input, please try again")
            continue
        else:
            if date_filter not in ["month", "day", "both", "none"]:
                print("Input out of range, please try again")
                continue
            else:
                break

    month, day = None, None
    # get user input for month
    if date_filter in ["month", "both"]:
        print("Which month - January, February, March, April, May, or June?")
        while True:
            try:
                month = input("Specify the month:").lower()
            except ValueError:
                print("That's not a valid input for month, please try again")
                continue
            else:
                if month not in month_text:
                    print("Month out of range, please try again")
                    continue
                else:
                    break
                
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if date_filter in ["day", "both"]:
        print("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?")
        while True:
            try:
                day = input("Specify the day:").lower()
            except ValueError:
                print("That's not a valid input for day, please try again")
                continue
            else:
                if day not in day_text:
                    print("Day out of range, please try again")
                    continue
                else:
                    break
    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = CITY_DATA[city]
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day"] = df["Start Time"].dt.weekday 
    df["hour"] = df["Start Time"].dt.hour

    if month != None:
        month = month_text.index(month) + 1
        df = df.loc[df["month"] == month]

    if day != None:
        day = day_text.index(day) 
        df = df.loc[df["day"] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most popular month
    month_mode = df["month"].mode()[0]
    month_mode_count = df.loc[df["month"] == month_mode].count()[0]
    print("Most Popular Month: {}, Count: {} ".format(
            month_mode, month_mode_count))

    # display the most popular day
    day_mode = df["day"].mode()[0]
    day_mode_count = df.loc[df["day"] == day_mode].count()[0]
    print("Most Popular Day: {}, Count: {} ".format(
            day_mode, day_mode_count))

    # display the most popular hour
    hour_mode = df["hour"].mode()[0]
    hour_mode_count = df.loc[df["hour"] == hour_mode].count()[0]
    print("Most Popular Hour: {}, Count: {} ".format(
            hour_mode, hour_mode_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    s_station_mode = df["Start Station"].mode()[0]
    s_station_mode_count = df.loc[df["Start Station"] == s_station_mode].count()[0]
    print("Most Popular Start Station: {}, Count: {} ".format(
            s_station_mode, s_station_mode_count))

    # display most commonly used end station
    e_station_mode = df["End Station"].mode()[0]
    e_station_mode_count = df.loc[df["End Station"] == e_station_mode].count()[0]
    print("Most Popular End Station: {}, Count: {} ".format(
            e_station_mode, e_station_mode_count))

    # display most frequent combination of start station and end station trip
    df["Station Combo"] = df["Start Station"] + " --> " + df["End Station"]
    stn_combo_mode = df["Station Combo"].mode()[0]
    stn_combo_mode_count = df.loc[df["Station Combo"] == stn_combo_mode].count()[0]
    print("Most Popular End Station: {}, Count: {} ".format(
            stn_combo_mode, stn_combo_mode_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    print("The total trip duration in hours: ", df["Trip Duration"].sum()/3600)

    # display mean travel time
    print("The mean trip duration in minutes: ", df["Trip Duration"].mean()/ 60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    type_count = df["User Type"].value_counts()
    print("The counts of user types: ", type_count, "\n", "-"*10, "\n")
    
    # Display counts of gender
    if city != 'washington':
        age_count = df["Gender"].value_counts()
        print("The counts of gender: ", age_count, "\n", "-"*10, "\n")
    
    # Display earliest, most recent, and most common year of birth
        print("The earliest birth: ", df["Birth Year"].min(), "\n", "-"*10, "\n",
                "The latest birth: ", df["Birth Year"].max(), "\n", "-"*10, "\n",
                "The most common birth: ", df["Birth Year"].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def raw_data(df):
    """
    Asks user if they wanna see the raw data.
    Returns:
        if 'yes' - print 5 rows of the data at a time, then ask if wanna see more
        if 'yes' - ontinue prompting and printing the next 5 rows at a time
        if 'no' - stop printing raw data
    """
    
    # ask users if they wanna see the raw data, and print the raw data 5 lines a time
    print("Would you like to see the raw data?")
    count = 0
    while True:
        try:
            raw = input("Please type 'yes' or 'no':").lower()
        except ValueError:
            print("That's not a valid input, please try again")
            continue
        else:
            if raw == 'yes':
                print(df.iloc[count:count+5,:])
                print("Do you wanna see more raw data?")
                count +=1
                continue
            else:
                break
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        df.info()
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()

