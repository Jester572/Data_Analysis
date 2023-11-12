# Identify the two questions about the dataset on your own.
# 1: What device do people watch the longest
# 2: What genre is the most watched
# 3: Is there a difference between men and womens favorite genre

import pandas as pd


def main():
    data = read_file()
    info = None  # Initialize info here

    while info is None:  # Check if the Pandas Series is not None
        info = compute_data(data)
        run_again = input("Would you like to chose another option? Y/N: ").upper()
        if run_again != "Y":
            break

    print("Thank you for learning with me!")


# Reads raw data file
def read_file():
    df = pd.read_csv("streaming_viewership_data.csv")
    return df


# Main navigation screen
def compute_data(data):
    valid = False
    while valid == False:
        print(
            "0: Quit\n"
            "1: View favorite genre by country\n"
            "2: View favorite genre by gender\n"
            "3: View most used to watch videos"
        )
        user_selection = input("Please select the information you would like to view: ")

        if user_selection == "1":
            return fav_genre_by_country(data)
        elif user_selection == "2":
            return fav_genre_by_gender(data)
        elif user_selection == "3":
            return watched_most_on_device(data)


# Validates that the user given country is a valid selection
def valid_country(data, country):
    if country in data["Country"].unique():
        return True
    else:
        return False


# Retrieves and calculates statistics on a given country
def fav_genre_by_country(data):
    valid = False
    # Retrieves user input and validates it
    while valid == False:
        view_countries = input(
            "Would you like to view a list of countries?(Y/N): "
        ).upper()
        if view_countries == "Y":
            for country in data["Country"].sort_values().unique():
                print(country)

        country = input("Please type a country name: ")
        valid = valid_country(data, country)
        if not valid:
            print(
                "That is not a valid Country please make sure you are capitalizing accordingly"
            )

    # Queries all data with that country
    country_data = data.query(f'Country == "{country}"')

    # Creates the table that shows the mean, min, max of the number of minutes watched
    data1 = (
        country_data.groupby(["Genre"])[["Duration_Watched (minutes)"]]
        .agg(["mean", "min", "max"])
        .reset_index()
    )
    data1.columns = ["Genre", "Mean", "Min", "Max"]

    # Creates the table that calculates the number of sessions that were started on a give Genre
    data2 = country_data["Genre"].value_counts(sort=True).reset_index()
    data2.columns = ["Genre", "Count"]
    print("\n----- Average, Minimum, Maximum time watched Genre (Minutes) -----")
    print(f"{data1}\n")
    print("\n----- Number of Sessions Recorded watching a Genre -----")
    print(f"{data2}\n")

    # Merges the two tables into one
    result = pd.merge(data1, data2, on="Genre")
    print("\n----- Previous two tables combined -----")
    print(f"{result}\n")


# Shows Mean, Min, Max of time watched by male vs female. Also shows number of sessions of genre watched by each gender
def fav_genre_by_gender(data):
    # Get and Calculate all info for male
    male = data.query(f'Gender == "Male"')
    male_data = (
        male.groupby(["Genre"])[["Duration_Watched (minutes)"]]
        .agg(["mean", "min", "max"])
        .reset_index()
    )
    male_data.columns = ["Genre", "Mean", "Min", "Max"]
    male_sessions = male["Genre"].value_counts(sort=True).reset_index()

    # Get and Calculate all info for female
    female = data.query(f'Gender == "Female"')
    female_data = (
        female.groupby(["Genre"])[["Duration_Watched (minutes)"]]
        .agg(["mean", "min", "max"])
        .reset_index()
    )
    female_data.columns = ["Genre", "Mean", "Min", "Max"]
    female_sessions = female["Genre"].value_counts(sort=True).reset_index()

    # Combines the male sessions and female sessions into one table
    result = pd.merge(male_sessions, female_sessions, on="Genre")
    result.columns = ["Genre", "Male", "Female"]

    # Prints all results
    print("\n----- Average, Minimum, Maximum time watched by Males (Minutes) -----\n")
    print(f"{male_data}\n")
    print("\n----- Average, Minimum, Maximum time watched by Females (Minutes) -----\n")
    print(f"{female_data}")
    print("\n----- Number of Sessions watched sorted by Genre -----\n")
    print(f"{result}")


# Shows which type of device is the most used to watch a session
def watched_most_on_device(data):
    info = data["Device_Type"].value_counts(sort=True)
    return info


if __name__ == "__main__":
    main()
