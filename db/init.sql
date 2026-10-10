CREATE TABLE cocktails (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    base VARCHAR(60) NOT NULL,
    ingredients TEXT NOT NULL,
    preparation TEXT NOT NULL,
    price INTEGER NOT NULL
);

COPY cocktails (id, name, base, ingredients, preparation, price)
FROM '/docker-entrypoint-initdb.d/cocktails.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
