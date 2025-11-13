import pandas as pd
from google_play_scraper import reviews, Sort
import time

apps_to_scrape = {
        'AlloFresh': 'id.allofresh.ecommerce',
        'Astro': 'com.astro.shop',
        'Sayurbox': 'com.sayurbox',
        'HappyFresh': 'com.happyfresh.android'
}

REVIEW_COUNT_PER_APP = 200

print("Memulai proses scraping...")

all_reviews_list = []

for app_name, app_id in apps_to_scrape.items():
    print(f"Mengambil {REVIEW_COUNT_PER_APP} review terbaru untuk: {app_name} ({app_id})")
    
    try:
        result, _ = reviews(
            app_id,
            lang='id',
            country='id',
            sort=Sort.NEWEST,
            count=REVIEW_COUNT_PER_APP,
            filter_score_with=None 
        )
        
        for r in result:
            r['app_name'] = app_name 
        
        all_reviews_list.extend(result)
        
        print(f"Berhasil! {len(result)} review untuk {app_name} ditambahkan.")
        
        time.sleep(3) 

    except Exception as e:
        print(f"Gagal mengambil review untuk {app_name}. Error: {e}")

print(f"\nTotal review dari semua aplikasi terkumpul: {len(all_reviews_list)}")

if len(all_reviews_list) > 0:
    print("Mengubah data jadi df")
    df = pd.DataFrame(all_reviews_list)
    
    df_selected = df[['reviewId', 'app_name', 'at', 'score', 'content']]
    
    df_final = df_selected.rename(columns={
        'at': 'review_date',
        'score': 'rating',
        'content': 'review_text'
    })
    
    output_filename = 'raw_reviews.csv'
    df_final.to_csv(output_filename, index=False, encoding='utf-8')
    
    print(f"\n done.")
    print(f"Data saved: {output_filename}")
    print(f"Total baris data: {len(df_final)}")

else:
    print("review gak berhasil diambil.")