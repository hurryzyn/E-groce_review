import pandas as pd
import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from io import StringIO
import sys

print("Memuat model Analisis Sentimen (NLP)...")
analyzer = SentimentIntensityAnalyzer()

DB_NAME = "grocery_db"
DB_USER = "postgres"
DB_PASS = "111"
DB_HOST = "localhost"
DB_PORT = "5432"


def analyze_sentiment(text):
    """
    Menganalisis sentimen teks menggunakan VADER.
    Mengembalikan 'positif', 'negatif', atau 'netral'.
    """
    if not isinstance(text, str):
        return 'netral'
        
    score = analyzer.polarity_scores(text)
    compound = score['compound']
    
    if compound >= 0.05:
        return 'positif'
    elif compound <= -0.05:
        return 'negatif'
    else:
        return 'netral'

def create_table(conn):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS app_reviews (
        reviewId VARCHAR(255) PRIMARY KEY,
        app_name VARCHAR(100),
        review_date TIMESTAMPTZ,
        rating INT,
        review_text TEXT,
        sentiment VARCHAR(10)
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(create_table_query)
            conn.commit()
            print("Tabel 'app_reviews' siap digunakan.")
    except Exception as e:
        print(f"Error saat membuat tabel: {e}")
        conn.rollback()
        raise e

def copy_data_to_db(conn, df):
    """
    Menggunakan metode COPY FROM STDIN PostgreSQL untuk
    memasukkan data dari DataFrame Pandas dengan SANGAT CEPAT.
    """
    buf = StringIO()
    df.to_csv(buf, index=False, header=False)
    buf.seek(0)
    
    copy_query = """
        COPY app_reviews(reviewId, app_name, review_date, rating, review_text, sentiment) 
        FROM STDIN WITH (FORMAT CSV)
    """
    
    try:
        with conn.cursor() as cur:
            cur.copy_expert(sql=copy_query, file=buf)
            conn.commit()
            print(f"Berhasil menyalin {len(df)} baris ke database.")
    except Exception as e:
        print(f"Error saat menyalin data: {e}")
        conn.rollback()
        raise e

if __name__ == "__main__":
    try:
        print("Membaca file ")
        df = pd.read_csv('raw_reviews.csv')
        
        print("Melakukan Analisis Sentimen...")
        df['sentiment'] = df['review_text'].apply(analyze_sentiment)
        
        df_final = df[['reviewId', 'app_name', 'review_date', 'rating', 'review_text', 'sentiment']]
        
        print(f"Menghubungkan ke PostgreSQL di {DB_HOST}:{DB_PORT}...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        
        create_table(conn)
        
        copy_data_to_db(conn, df_final)

        conn.close()
        
        print(f"\n ETL Selesai. Data masuk ke database '{DB_NAME}'.")

    except FileNotFoundError:
        print("Error: File 'raw_reviews.csv' tidak ditemukan.")
    except psycopg2.OperationalError as e:
        print(f"\n--- ERROR KONEKSI DATABASE ---")
        print("Gagal terhubung ke PostgreSQL.")
        print("Pastikan:")
        print("1. Container Docker PostgreSQL  sedang UP kali.")
        print("2. Detail DB udah benar.")
        print(f"Detail Error: {e}")
    except Exception as e:
        print(f"error: {e}")