#!/bin/bash

# Function to check if a Python package is installed
function check_python_package {
    if python3 -c "import $1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Check if BeautifulSoup is installed
if check_python_package "bs4"; then
    echo "BeautifulSoup is installed."
else
    echo "BeautifulSoup is not installed. Installing..."
    pip3 install beautifulsoup4
fi

# Change directory to the location of the script
cd "$(dirname "$0")"

# Execute the Python script
python3 <<END
import requests
from bs4 import BeautifulSoup
import os

# Function to download a file
def download_file(url, filename):
    with open(filename, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)

# Function to extract cart links from a page
def extract_cart_links(page_url):
    # Send a GET request to the page URL
    page_response = requests.get(page_url)

    # Parse the HTML content of the page
    page_soup = BeautifulSoup(page_response.content, 'html.parser')

    # Find all cart links on the page
    cart_links = page_soup.find_all('a', href=lambda href: href and 'play?cart=' in href)

    return cart_links

# URL of the webpage containing the top games
main_page_base_url = 'https://tic80.com/play?cat=0&sort=2&page='

# Get the directory of the script
script_directory = os.path.dirname(os.path.realpath(__file__))

# Loop through multiple pages
for page_number in range(1, 3):  # Change range as needed
    page_url = main_page_base_url + str(page_number)

    # Extract cart links from the current page
    cart_links = extract_cart_links(page_url)

    # Iterate over each cart link
    for cart_link in cart_links:
        # Construct URL for the cart page
        cart_url = 'https://tic80.com' + cart_link['href']

        # Send a GET request to the cart page URL
        cart_response = requests.get(cart_url)

        # Parse the HTML content of the cart page
        cart_soup = BeautifulSoup(cart_response.content, 'html.parser')

        # Find the TIC file link on the cart page
        tic_file_link = cart_soup.find('a', href=lambda href: href and '/cart/' in href and href.endswith('.tic'))
        
        # Check if the TIC file link is found
        if tic_file_link:
            tic_file_url = 'https://tic80.com' + tic_file_link['href']
            
            # Get the filename from the URL
            filename = os.path.join(script_directory, tic_file_url.split('/')[-1])

            # Check if the file already exists
            if os.path.exists(filename):
                print("File already exists:", tic_file_url)
            else:
                # Download the TIC file
                download_file(tic_file_url, filename)
                print("Downloaded:", tic_file_url)
        else:
            print("TIC file link not found on:", cart_url)

print("Download link extraction complete.")
END
