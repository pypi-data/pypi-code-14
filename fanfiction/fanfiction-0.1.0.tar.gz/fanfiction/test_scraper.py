from fanfiction import Scraper

if __name__ == '__main__':
    scraper = Scraper()
    story = scraper.scrape_story_metadata(3005227)
