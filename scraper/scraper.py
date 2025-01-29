import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests

# Create necessary directories
os.makedirs('data/card_images', exist_ok=True)

class TCGPlayerScraper:
    def __init__(self):
        print("Initializing Chrome WebDriver...")
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--disable-notifications')
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        self.base_url = "https://www.tcgplayer.com/search/one-piece-card-game/product"
        self.service = Service(ChromeDriverManager().install())

    def download_image(self, card_name, img_url):
        """Download and save card image."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
            }
            
            response = requests.get(img_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Clean filename
            safe_name = ''.join(c for c in card_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            img_filename = f"data/card_images/{safe_name}.jpg"
            
            with open(img_filename, 'wb') as img_file:
                img_file.write(response.content)
            return img_filename
        except Exception as e:
            print(f"Error downloading image for {card_name}: {e}")
            return None

    def scrape_page(self, page_number):
        """Scrape a single page of card data using Selenium."""
        url = f"{self.base_url}?productLineName=one-piece-card-game&view=grid&page={page_number}"
        driver = None
        cards_data = []
        
        try:
            print(f"\nAccessing page {page_number}...")
            driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
            driver.get(url)
            
            # Wait for content to load
            wait = WebDriverWait(driver, 20)
            print("Waiting for content to load...")
            
            # Wait for the product grid to load
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-card__title"))
            )
            
            # Additional wait for all content
            time.sleep(5)
            
            # Get all card elements
            print("Finding all card elements...")
            titles = driver.find_elements(By.CLASS_NAME, "product-card__title")
            print(f"Found {len(titles)} cards")
            
            for title_elem in titles:
                try:
                    # Get the parent container for this card
                    card_container = title_elem.find_element(By.XPATH, "./ancestor::div[contains(@class, 'search-result')]")
                    
                    # Get card name
                    name = title_elem.text.strip()
                    
                    # Get price (looking for market price specifically)
                    try:
                        price = card_container.find_element(
                            By.CSS_SELECTOR, 
                            "[class*='price']"
                        ).text.strip()
                    except:
                        price = "Price not available"
                    
                    # Get image URL
                    try:
                        img_elem = card_container.find_element(
                            By.CLASS_NAME, "lazy-image__wrapper"
                        )
                        img_url = img_elem.get_attribute('src')
                    except:
                        img_url = None
                        
                    print(f"Processing card: {name}")
                    
                    # Download image if available
                    image_path = self.download_image(name, img_url) if img_url else None
                    
                    cards_data.append({
                        'Name': name,
                        'Price': price,
                        'Image URL': img_url,
                        'Image Path': image_path
                    })
                    
                except Exception as e:
                    print(f"Error processing card: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping page {page_number}: {e}")
        
        finally:
            if driver:
                driver.quit()
            
        return cards_data

    def scrape_all_pages(self, num_pages, delay=3):
        """Scrape multiple pages of card data."""
        all_cards_data = []
        
        for page in range(1, num_pages + 1):
            print(f"\n{'='*50}")
            print(f"Scraping page {page} of {num_pages}")
            print(f"{'='*50}")
            
            page_data = self.scrape_page(page)
            
            if page_data:
                all_cards_data.extend(page_data)
                print(f"Added {len(page_data)} cards from page {page}")
            else:
                print(f"No data found on page {page}")
            
            if page < num_pages:
                print(f"Waiting {delay} seconds before next request...")
                time.sleep(delay)
        
        if all_cards_data:
            df = pd.DataFrame(all_cards_data)
            output_file = 'data/cards_data.csv'
            df.to_csv(output_file, index=False)
            print(f"\nScraping completed! Total cards collected: {len(all_cards_data)}")
            print(f"Data saved to '{output_file}'")
        else:
            print("\nNo data was collected. Please check the website structure or try again later.")

            

if __name__ == "__main__":
    print("Starting TCGPlayer scraper...")
    scraper = TCGPlayerScraper()
    scraper.scrape_all_pages(5)  # Start with 1 page for testing