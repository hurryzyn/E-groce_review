CREATE TABLE IF NOT EXISTS app_reviews (
    reviewId VARCHAR(255) PRIMARY KEY,
    app_name VARCHAR(100),
    review_date TIMESTAMPTZ,
    rating INT,
    review_text TEXT,
    sentiment VARCHAR(10)
);