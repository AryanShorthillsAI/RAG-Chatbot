import os
import requests
from bs4 import BeautifulSoup
from extractor import extract_text_from_pdf


# Function to fetch the page and retrieve the script download link
def fetch_script_page(movie_name, script_url):
    """
    Fetches the script page, extracts the download link, and downloads the script as a PDF.
    Skips downloading if the link is a Google Drive link.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    if "drive.google.com" in script_url:
        print(f"Skipping script download for {movie_name}: Google Drive link detected ({script_url})")
        return

    response = requests.get(script_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_link_tag = soup.find('a', class_='js-button-read', href=True)

        if script_link_tag:
            script_download_url = script_link_tag['href']
            print(f"Found script download link for {movie_name}: {script_download_url}")
            download_script(movie_name, script_download_url)
        else:
            print(f"No script download link found for {movie_name}")
    else:
        print(f"Failed to retrieve the script page for {movie_name}. Status code: {response.status_code}")

# Function to download the script and save it as a PDF
def download_script(movie_name, script_download_url):
    """
    Downloads the script from the provided URL and saves it as a PDF in the 'scripts' folder.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    script_response = requests.get(script_download_url, headers=headers)

    if script_response.status_code == 200:
        folder = 'scripts'
        os.makedirs(folder, exist_ok=True)
        filename = f"{movie_name.replace(' ', '_').replace('/', '_')}.pdf"
        file_path = os.path.join(folder, filename)

        with open(file_path, 'wb') as f:
            f.write(script_response.content)

        print(f"Script for {movie_name} downloaded and saved as {filename}")
        
        # After downloading the script
        file_path = os.path.join(folder, filename)
        extract_text_from_pdf(file_path)  # This will extract and save JSON automatically

    else:
        print(f"Failed to download script for {movie_name}. Status code: {script_response.status_code}")

# Function to retrieve movie names and corresponding script URLs from the main page
def fetch_movie_scripts(url):
    """
    Fetches movie names and their corresponding script download links from the main URL.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_dict = get_movie_titles_and_years(soup)
        script_dict = get_script_links(soup)
        return movie_dict, script_dict
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return {}, {}

# Function to extract movie titles and years from the main page
def get_movie_titles_and_years(soup):
    """
    Extracts the movie titles and release years from the BeautifulSoup object of the main page.
    """
    movie_dict = {}
    movies = soup.find_all('h2')

    for movie in movies:
        movie_title = movie.get_text().strip()
        year_start = movie_title.find('(') + 1
        year_end = movie_title.find(')')
        release_year = movie_title[year_start:year_end] if year_start != 0 and year_end != -1 else "Unknown"
        movie_dict[movie_title] = release_year

    return movie_dict

# Function to extract the script download links from the main page
def get_script_links(soup):
    """
    Extracts the script download links from the BeautifulSoup object of the main page.
    """
    script_dict = {}
    script_links = soup.find_all('a', href=True)

    for link in script_links:
        if "Read the screenplay!" in link.get_text():
            script_url = link['href']
            if "drive.google.com" in script_url:
                continue
            movie_name = link.find_previous('h2').get_text().strip()
            script_dict[movie_name] = script_url

    return script_dict

# Main execution
def main():
    url = 'https://bulletproofscreenwriting.tv/christopher-nolan-screenplay-download/'
    movie_dict, script_dict = fetch_movie_scripts(url)

    if movie_dict:
        print("Movie Dictionary:")
        for title, year in movie_dict.items():
            print(f"{title}: {year}")
        
        print("\nMovie Script Links:")
        for title, script_url in script_dict.items():
            print(f"{title}: {script_url}")
        
        for movie_name, script_url in script_dict.items():
            fetch_script_page(movie_name, script_url)
    else:
        print("No movie data found.")


if __name__ == "__main__":
    main()