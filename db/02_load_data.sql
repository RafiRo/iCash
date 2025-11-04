-- disable foreign key
ALTER TABLE purchases DROP CONSTRAINT IF EXISTS purchases_supermarket_id_fkey;
ALTER TABLE purchases DROP CONSTRAINT IF EXISTS purchases_user_id_fkey;

--load csv
\copy products_list (product_name, unit_price) FROM '/docker-entrypoint-initdb.d/products_list.csv' WITH (FORMAT csv, HEADER true);
\copy purchases (supermarket_id, "timestamp", user_id, item_list, total_amount) FROM '/docker-entrypoint-initdb.d/purchases.csv' WITH (FORMAT csv, HEADER true);

--updates tables for missing data
INSERT INTO supermarket (supermarket_id)
SELECT DISTINCT p.supermarket_id
FROM purchases p
WHERE p.supermarket_id IS NOT NULL
  AND NOT EXISTS (
      SELECT 1 FROM supermarket s WHERE s.supermarket_id = p.supermarket_id
  );

INSERT INTO app_user (user_id)
SELECT DISTINCT p.user_id
FROM purchases p
WHERE p.user_id IS NOT NULL
  AND NOT EXISTS (
      SELECT 1 FROM app_user u WHERE u.user_id = p.user_id
  );

-- Re-enable foreign key
ALTER TABLE purchases
    ADD CONSTRAINT purchases_supermarket_id_fkey
        FOREIGN KEY (supermarket_id)
        REFERENCES supermarket(supermarket_id);

ALTER TABLE purchases
    ADD CONSTRAINT purchases_user_id_fkey
        FOREIGN KEY (user_id)
        REFERENCES app_user(user_id);





--
--\copy product_list (product_name, unit_price)FROM '/docker-entrypoint-initdb.d/products_list.csv'WITH (FORMAT csv, HEADER true);
--\copy purchases (supermarket_id, "timestamp", user_id, item_list, total_amount)FROM '/docker-entrypoint-initdb.d/purchases.csv'WITH (FORMAT csv, HEADER true);