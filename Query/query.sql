
SELECT
    app_name,
    COUNT(*) AS total_reviews,
    AVG(rating) AS average_rating,
    
    (SUM(CASE WHEN sentiment = 'positif' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS positive_percentage,
    (SUM(CASE WHEN sentiment = 'negatif' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS negative_percentage
    
FROM
    app_reviews
GROUP BY
    app_name
ORDER BY
    total_reviews DESC;



SELECT
    app_name,
    SUM(CASE WHEN LOWER(review_text) LIKE '%lama%' THEN 1 ELSE 0 END) AS keluhan_pengiriman_lama,
    SUM(CASE WHEN LOWER(review_text) LIKE '%mahal%' THEN 1 ELSE 0 END) AS keluhan_harga_mahal,
    SUM(CASE WHEN LOWER(review_text) LIKE '%error%' OR LOWER(review_text) LIKE '%crash%' THEN 1 ELSE 0 END) AS keluhan_aplikasi_error,
    
    SUM(CASE WHEN LOWER(review_text) LIKE '%cepat%' THEN 1 ELSE 0 END) AS pujian_pengiriman_cepat
FROM
    app_reviews
GROUP BY
    app_name;


SELECT
    DATE_TRUNC('week', review_date) AS review_week,
    app_name,
    AVG(rating) AS weekly_average_rating
FROM
    app_reviews
GROUP BY
    review_week, app_name
ORDER BY
    review_week DESC;