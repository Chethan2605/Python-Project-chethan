from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

GENRE_URLS = {
    "action": "https://www.rottentomatoes.com/browse/movies_at_home/genres:action",
    "comedy": "https://www.rottentomatoes.com/browse/movies_at_home/genres:comedy",
    "drama": "https://www.rottentomatoes.com/browse/movies_at_home/genres:drama",
    "horror": "https://www.rottentomatoes.com/browse/movies_at_home/genres:horror",
    "romance": "https://www.rottentomatoes.com/browse/movies_at_home/genres:romance",
    "sci-fi": "https://www.rottentomatoes.com/browse/movies_at_home/genres:sci_fi",
    "documentary": "https://www.rottentomatoes.com/browse/movies_at_home/genres:documentary",
    "animation": "https://www.rottentomatoes.com/browse/movies_at_home/genres:animation"
}

def scrape_movies_selenium(genre, count=5):
    if genre not in GENRE_URLS:
        print(f"❌ Genre '{genre}' not supported.")
        return

    url = GENRE_URLS[genre]

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        print(f"🔍 Loading {genre.title()} movies page...")
        driver.get(url)
        time.sleep(5)  # wait for JS to render

        movie_cards = driver.find_elements(By.CSS_SELECTOR, 'a.js-tile-link')[:count]
        movie_data = []

        for i, card in enumerate(movie_cards, 1):
            try:
                title = card.find_element(By.CSS_SELECTOR, 'span.p--small').text.strip()
            except:
                title = "N/A"
            print(f"{i}. 🎬 {title}")
            movie_data.append({"Title": title, "Genre": genre.title()})

        df = pd.DataFrame(movie_data)
        output_path = os.path.join(os.path.dirname(__file__), "scraped_movies.csv")
        df.to_csv(output_path, mode="a", header=not os.path.exists(output_path), index=False)
        print(f"✅ Saved {len(df)} movies to scraped_movies.csv")
        
    except PermissionError:
        print("❌ ERROR: Cannot write to 'scraped_movies.csv'. Please close it if it's open in another app.")

    except Exception as e:
        print(f"🚨 Error: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    print("🎬 Welcome to Movie Picker!\n I will suggest a movie from your favorite genre 🍿\n")
    genre_input = input("Select your favorite genre (action, comedy, drama, horror, romance, sci-fi,): ").lower().strip()
    movie_count = 5
    scrape_movies_selenium(genre_input, count=movie_count)

    output_path = os.path.join(os.path.dirname(__file__), "scraped_movies.csv")
    print(f"\n📁 CSV saved at: {output_path}")

    print("\n📄 Preview of saved movies:")
    try:
        df_read = pd.read_csv(output_path)
        print(df_read.tail(movie_count))
    except Exception as e:
        print(f"❌ Failed to read saved CSV: {e}")
        
time.sleep(10)
