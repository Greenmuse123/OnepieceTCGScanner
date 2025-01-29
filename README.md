One Piece TCG Scraper

📌 Description

This script scrapes card data from the One Piece TCG website using Selenium and BeautifulSoup. The data is then saved into a CSV file for easy access and analysis.

🛠️ Requirements

Make sure you have the following installed:

Python 3.x

Google Chrome (latest version)

Chromedriver (compatible with your Chrome version)

The following Python libraries:

pip install selenium beautifulsoup4 pandas

🚀 Setup

Clone or download this repository:

git clone https://github.com/your-repo/one_piece_tcg_scraper.git
cd one_piece_tcg_scraper/scraper

Ensure chromedriver is installed and placed in a directory accessible by your system.

Adjust the number of pages to scrape by modifying the scrape_all_pages method at the end of scraper.py. The default is set to 5 pages, but you can change this as needed:

scraper.scrape_all_pages(num_pages=5)  # Adjust this number as needed

📦 Running the Scraper

To start scraping, run:

python scraper.py

The script will automatically fetch the requested number of pages and save the data to data/cards_data.csv.

⚠️ Important Notes

The website structure may change over time, so if scraping stops working, check for updates in the HTML elements.

The script includes a delay to avoid getting blocked by the website.

📄 Output

The scraper will save all collected card data to:

data/cards_data.csv

This file will contain columns such as:

Card Name

Card Type

Price

Availability

❓ Troubleshooting

Chromedriver version mismatch: Ensure that your chromedriver version matches your Chrome browser version.

Website layout changes: If the script stops working, inspect the website’s structure and update the relevant XPath/CSS selectors.

No data collected?: Check if the website has protection against scraping (like CAPTCHAs) and adjust accordingly.

Happy Scraping! 🚀