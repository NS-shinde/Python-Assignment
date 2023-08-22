import requests
import csv
from bs4 import BeautifulSoup

# URL of the initial product listing page
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
num_pages = 20  # Number of pages to scrape

# Lists to store scraped data
product_urls = []
product_names = []
product_prices = []
product_ratings = []
product_review_counts = []

# Loop through each page
for page in range(1, num_pages + 1):
    page_url = f"{base_url}&page={page}"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all product containers
    product_containers = soup.find_all("div", class_="sg-col-inner")

    # Extract data from each product container
    for container in product_containers:
        # Extract product URL
        product_link = container.find("a", class_="a-link-normal")
        if product_link:
            product_urls.append("https://www.amazon.in" + product_link["href"])
        
        # Extract product name
        product_name = container.find("span", class_="a-text-normal")
        if product_name:
            product_names.append(product_name.text)
        
        # Extract product price
        product_price = container.find("span", class_="a-price")
        if product_price:
            product_prices.append(product_price.find("span", class_="a-offscreen").text)
        
        # Extract product rating
        product_rating = container.find("span", class_="a-icon-alt")
        if product_rating:
            product_ratings.append(product_rating.text)
        
        # Extract number of reviews
        review_count = container.find("span", class_="a-size-base")
        if review_count:
            product_review_counts.append(review_count.text)

# Print or save the scraped data
for i in range(len(product_urls)):
    print("Product URL:", product_urls[i])
    print("Product Name:", product_names[i])
    print("Product Price:", product_prices[i])
    print("Rating:", product_ratings[i])
    print("Number of Reviews:", product_review_counts[i])
    print("=" * 50)

# You can save this data in a CSV file or any other format for further analysis
# Create a CSV file to save the data
csv_filename = "scraped_products.csv"

# Write the scraped data into the CSV file
with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"])
    
    for i in range(len(product_urls)):
        csv_writer.writerow([product_urls[i], product_names[i], product_prices[i], product_ratings[i], product_review_counts[i]])

print("Data has been saved to", csv_filename)