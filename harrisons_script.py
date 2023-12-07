import pandas as pd
import os
import sys
from urllib.parse import unquote
import matplotlib.pyplot as plt


def main():
    csv_path = get_csv()
    dataframe = mkdf(csv_path)
    site_visit_count(dataframe)
    get_encoded_urls(dataframe)
    plot_browsing_times(dataframe)
    
    return

# Gets the path of the CSV file from the command line
def get_csv():
    num_params = len(sys.argv)
    if num_params >= 1:
        csv_path = sys.argv[1]
        if os.path.isfile(csv_path):
            return csv_path
        else:
            print('Error: CSV file does not exist')
            sys.exit(1)
    else:
        print('Error: missing CSV file path')
        sys.exit(1)

# Creates the data frame
def mkdf(csv):
    df = pd.read_csv(csv)
    return df

# Extracts the hour from the Date/Time column
def plot_browsing_times(df):
    df['Hour'] = pd.to_datetime(df['Date/Time']).dt.hour

    # Plotting the times of day that have the most browser usage
    plt.figure(figsize=(10, 5))
    plt.hist(df['Hour'], bins=range(0, 25), edgecolor='black', align='left')  # Specify bins to include all hours
    plt.title('Internet Browsing Times')
    plt.xlabel('Hour of Day')
    plt.ylabel('Frequency')
    plt.xticks(range(0, 24))  # Set x-axis ticks for each hour
    plt.show()

# Displays the most and least visited sites
def site_visit_count(df):
    pd.set_option('display.max_rows', None)  # Set to display all rows
    
    # Sites visited the most
    most_visited_sites = df['URL'].value_counts().nlargest(5)
    print("Top 5 Most Visited Sites:")
    print(most_visited_sites.to_string(header=False))

    # Sites visited the least
    least_visited_sites = df['URL'].value_counts()
    least_visited_count = least_visited_sites.min()
    least_visited_sites = least_visited_sites[least_visited_sites == least_visited_count]

    print("\nLeast Visited Sites:")
    print(least_visited_sites.to_string(header=False))
    print()

# Checks and prints encoded URLS
def get_encoded_urls(df):
    decoded_urls = set()

    print('Encoded URLS: \n')
    for url in df['URL']:
        # Check if the URL has already been decoded
        if url in decoded_urls:
            continue

        decoded_url = unquote(url) # Decodes URL
        decoded_urls.add(url) # Adds URL to set
    
        if url != decoded_url:
            print(f"Encoded URL: {url}")
            print(f"Decoded URL: {decoded_url}")
            print()  # Add a blank line

# Call the main function
if __name__ == "__main__":
    main()
