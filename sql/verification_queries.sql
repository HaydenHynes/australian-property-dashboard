-- Verify total row count
SELECT COUNT(*) AS total_sales
FROM property_sales;

-- Sales by suburb/locality
SELECT
    property_locality,
    COUNT(*) AS sales_count
FROM property_sales
GROUP BY property_locality
ORDER BY sales_count DESC;

-- Average purchase price by suburb/locality
SELECT
    property_locality,
    ROUND(AVG(purchase_price), 2) AS average_purchase_price
FROM property_sales
WHERE purchase_price IS NOT NULL
GROUP BY property_locality
ORDER BY average_purchase_price DESC;

-- Most expensive sales
SELECT
    property_locality,
    property_street_name,
    property_house_number,
    purchase_price,
    contract_date
FROM property_sales
WHERE purchase_price IS NOT NULL
ORDER BY purchase_price DESC
LIMIT 20;

-- Sales volume by property nature
SELECT
    nature_of_property,
    COUNT(*) AS sales_count
FROM property_sales
GROUP BY nature_of_property
ORDER BY sales_count DESC;