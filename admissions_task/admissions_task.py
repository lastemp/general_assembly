import csv
import sys
from statistics import mean

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew

from scipy.stats import probplot


# Maps to pledged amounts of the kickstarter dataset
kickstarter_dataset = []


def create_histogram_backers(filename):
    # Assuming you have a CSV file named 'data.csv' with a column 'backers'

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename, encoding='latin-1')

    # Plot the histogram
    plt.hist(df['backers'], bins=20, color='blue', edgecolor='black')
    plt.title('Distribution of Number of Backers')
    plt.xlabel('Number of Backers')
    plt.ylabel('Frequency')
    plt.show()

    # Calculate skewness
    skewness = skew(df['backers'])
    print(f"Skewness of the distribution: {skewness}")


def create_histogram_duration(filename):
    # Assuming you have a CSV file named 'data.csv' with a column 'duration'

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename, encoding='latin-1')

    # Plot the histogram
    # Q-Q plot
    probplot(df['duration'], dist="norm", plot=plt)
    plt.title("Q-Q plot")
    plt.show()


def get_best_length_of_time_to_run_a_campaign(filename):
    # Assuming you have a CSV file named 'data.csv' with a column 'duration'

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename, encoding='latin-1')

    # Separate successful and unsuccessful campaigns:
    successful_campaigns = df[df['status'] == 'successful']
    # unsuccessful_campaigns = df[df['status'] == 'failed']

    # Calculate the average duration of successful campaigns:
    average_duration_successful = successful_campaigns['duration'].mean()
    print(f"Average duration of successful campaigns: {average_duration_successful}")

    # Visualize the distribution of campaign durations:
    plt.figure(figsize=(10, 6))
    plt.hist(successful_campaigns['duration'], bins=30,
             alpha=0.5, label='Successful Campaigns')
    """ plt.hist(unsuccessful_campaigns['duration'], bins=30,
             alpha=0.5, label='Unsuccessful Campaigns') """
    plt.xlabel('Campaign Duration')
    plt.ylabel('Number of Campaigns')
    plt.legend()
    plt.show()

    # Analyze the correlation between campaign duration and success:
    correlation_duration_success = df[['duration', 'status']].apply(
        lambda x: x['duration'] if x['status'] == 'successful' else 0, axis=1).corr(df['duration'])
    print(f"Correlation between campaign duration and success: {correlation_duration_success}")


def get_ideal_pledge_goal(filename):
    # Assuming you have a CSV file named 'data.csv' with a column 'duration'

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename, encoding='latin-1')

    # Convert the "goal," "pledged," and "funded percentage" columns to numeric format:
    df['goal'] = pd.to_numeric(df['goal'])
    df['pledged'] = pd.to_numeric(df['pledged'])
    df['funded percentage'] = pd.to_numeric(df['funded percentage']) / 100.0

    # Separate successful and unsuccessful campaigns:
    successful_campaigns = df[df['status'] == 'successful']
    # unsuccessful_campaigns = df[df['status'] == 'failed']

    # Calculate the average goal of successful campaigns:
    average_goal_successful = successful_campaigns['goal'].mean()
    print(f"Average goal of successful campaigns: {average_goal_successful}")

    # Visualize the distribution of campaign goals:
    plt.figure(figsize=(10, 6))
    plt.hist(successful_campaigns['goal'], bins=30,
             alpha=0.5, label='Successful Campaigns')
    """ plt.hist(unsuccessful_campaigns['goal'], bins=30,
             alpha=0.5, label='Unsuccessful Campaigns') """
    plt.xlabel('Campaign Goal')
    plt.ylabel('Number of Campaigns')
    plt.legend()
    plt.show()

    # Analyze the funded percentage achieved by successful campaigns:
    average_funded_percentage_successful = successful_campaigns['funded percentage'].mean(
    )
    print(f"Average funded percentage of successful campaigns: {average_funded_percentage_successful}")


def get_projects_most_successful_getting_funded(filename):
    # type of projects would be most successful at getting funded
    # Assuming you have a CSV file named 'data.csv' with a column 'duration'

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename, encoding='latin-1')

    # Group campaigns by "category" and "subcategory":
    grouped_by_category = df.groupby(['category', 'subcategory'])

    # Calculate the success rate for each category/subcategory:
    success_rate = grouped_by_category['status'].apply(lambda x: (
        x == 'successful').sum() / len(x)).reset_index(name='success_rate')

    # Identify the categories/subcategories with the highest success rates:
    top_categories = success_rate.sort_values(
        by='success_rate', ascending=False).head(10)
    print(top_categories)

    # Visualize the success rates:
    plt.figure(figsize=(12, 6))
    plt.bar(top_categories['category'] + ' - ' +
            top_categories['subcategory'], top_categories['success_rate'])
    plt.xlabel('Category - Subcategory')
    plt.ylabel('Success Rate')
    plt.title('Top 10 Categories/Subcategories with Highest Success Rates')
    plt.xticks(rotation=45, ha='right')
    plt.show()


def get_ideal_month_day_time_to_launch_campaign(filename):
    # ideal month/day/time to launch a campaign
    # Assuming you have a CSV file named 'data.csv' with a column 'duration'

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename, encoding='latin-1')

    # Convert the "funded date" column to a pandas datetime object:
    df['funded date'] = pd.to_datetime(df['funded date'])

    # Extract information about the month, day, and time:
    df['month'] = df['funded date'].dt.month
    df['day'] = df['funded date'].dt.day
    df['hour'] = df['funded date'].dt.hour

    # Analyze the successful campaigns by month:
    successful_campaigns = df[df['status'] == 'successful']
    success_by_month = successful_campaigns['month'].value_counts(
    ).sort_index()

    # Visualize the success rates by month:
    plt.figure(figsize=(10, 6))
    plt.bar(success_by_month.index, success_by_month.values)
    plt.xlabel('Month')
    plt.ylabel('Number of Successful Campaigns')
    plt.title('Successful Campaigns by Month')
    plt.show()

    # Analyze the successful campaigns by day:
    success_by_day = successful_campaigns['day'].value_counts().sort_index()

    # Visualize the success rates by day:
    plt.figure(figsize=(12, 6))
    plt.bar(success_by_day.index, success_by_day.values)
    plt.xlabel('Day')
    plt.ylabel('Number of Successful Campaigns')
    plt.title('Successful Campaigns by Day')
    plt.show()

    # Analyze the successful campaigns by hour:
    success_by_hour = successful_campaigns['hour'].value_counts().sort_index()

    # Visualize the success rates by hour:
    plt.figure(figsize=(12, 6))
    plt.bar(success_by_hour.index, success_by_hour.values)
    plt.xlabel('Hour')
    plt.ylabel('Number of Successful Campaigns')
    plt.title('Successful Campaigns by Hour')
    plt.show()


def load_data(filename):
    """
    Load data from CSV files into memory.
    """

    # Load movies
    with open(filename, 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['pledged'] != '':
                try:
                    pledged = int(row["pledged"])
                except ValueError:
                    # Handle the case where the value is not a valid integer
                    print(f"Invalid value: {row['pledged']}")
            else:

                pledged = 0

            kickstarter_dataset.append(pledged)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python admissions_task.py data")

    # Load data from files into memory
    """ print("Loading data...")
    load_data(sys.argv[1])
    print("Data loaded.")
    #print(kickstarter_dataset)
    list_avg = mean(kickstarter_dataset)
    print("Average value of the list:\n")
    print(list_avg) """

    # Create a histogram that shows the distribution for number of backers
    create_histogram_backers(sys.argv[1])

    # Create a histogram that shows the distribution for duration
    # create_histogram_duration(sys.argv[1])

    # Get the best length of time to run a campaign
    # get_best_length_of_time_to_run_a_campaign(sys.argv[1])

    # Get the ideal pledge goal
    # get_ideal_pledge_goal(sys.argv[1])

    # Get type of projects would be most successful at getting funded
    # get_projects_most_successful_getting_funded(sys.argv[1])

    # Get ideal month/day/time to launch a campaign
    # get_ideal_month_day_time_to_launch_campaign(sys.argv[1])


if __name__ == "__main__":
    main()
