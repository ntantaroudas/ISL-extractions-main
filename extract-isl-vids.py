import requests
from bs4 import BeautifulSoup
import string
import time
import os


def download_mp4(mp4_url):
    # Extract file name from the URL (everything after the last '/')
    filename = mp4_url.split("/")[-1]
    print(f"Downloading: {mp4_url} as {filename}...")
    
    # Request the mp4 file using stream mode
    try:
        with requests.get(mp4_url, stream=True) as r:
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {mp4_url}: {e}")


def main():
    # URL template with a placeholder for the letter
    base_url = "https://web.archive.org/web/timemap/json?url=http%3A%2F%2Fwww.handspeak.com%2Fworld%2Fisl%2F{letter}%2F&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=10000&_=1740512674034"
    
    # Iterate over each letter in the alphabet
    for letter in string.ascii_lowercase[9:]:
        url = base_url.format(letter=letter)
        print(f"Processing letter '{letter}' with URL: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching page for letter {letter}: {e}")
            continue

        res_json = response.json()[1:]

        # Iterate through each td element and extract the href from its child <a> tag
        for link in res_json:
          mp4_url = 'https://web.archive.org/web/' + link[2] + '/' + link[0]
          time.sleep(5)
          if 'index' not in mp4_url:
            download_mp4(mp4_url)
        time.sleep(60)


if __name__ == "__main__":
    main()

