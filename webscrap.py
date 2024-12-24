import requests
from bs4 import BeautifulSoup
import pandas as pd

def google_search_scraper(query, num=10):
    # Replace spaces in the query with '+'
    query = query.replace(" ", "+")
    # Construct the Google search URL
    url = f"https://www.google.com/search?q={query}&num={num}"

    # Set headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    
    # Send the GET request to Google
    response = requests.get(url, headers=headers)
    
    # Check if the response is successful
    if response.status_code != 200:
        print("Failed to retrieve results")
        return None

    # Parse the response content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find search result elements
    results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text if g.find('h3') else "No title"
        link = g.find('a')['href'] if g.find('a') else "No link"
        description = g.find('span', class_='aCOpRe').text if g.find('span', class_='aCOpRe') else "No description"
        results.append({"Title": title, "Link": link, "Description": description})
    
    # Convert the results to a DataFrame for better presentation
    df = pd.DataFrame(results)
    return df

# Example Usage
if __name__ == "__main__":
    query = input("Enter your search query: ")
    num = int(input("Enter the number of results to scrape (e.g., 10): "))
    result = google_search_scraper(query, num)
    
    if result is not None:
        print(result)
        # Save the results to a CSV file
        result.to_csv("results.csv", index=False)
        print("Results saved to 'results.csv'.")
