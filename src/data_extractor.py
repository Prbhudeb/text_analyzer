from bs4 import BeautifulSoup
import requests
import logging

def extract_data(url):

    try:
        # Validate URL
        if not url.startswith("http"):
            logging.error(f"Invalid URL: {url}")
            return None

        # Fetch the webpage
        response = requests.get(url, timeout=10)  # Timeout to prevent hanging
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        # Parse HTML content
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Extract relevant data
        data_div = soup.find('div', class_='td-post-content tagdiv-type')
        if data_div:
            data_text = data_div.get_text(separator=" ").strip()
            # Extract only the text before "Contact Details"
            if "Contact Details" in data_text:
                data_text = data_text.split("Contact Details")[0]
            return data_text.strip()
        else:
            logging.warning("No content found with the specified class: 'td-post-content tagdiv-type'")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for URL {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while processing the URL {url}: {e}")
        return None
