CREATE TABLE streets (
    id SERIAL PRIMARY KEY,
    street TEXT UNIQUE
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    city TEXT UNIQUE
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    street_id INTEGER 
    REFERENCES streets
    ON DELETE CASCADE,
    city_id INTEGER 
    REFERENCES cities
    ON DELETE CASCADE
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    created_at TIMESTAMP, 
    address_id INTEGER REFERENCES addresses
);

CREATE TABLE review_categories (
    id SERIAL PRIMARY KEY,
    category TEXT UNIQUE
);

CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    grade INTEGER,
    restaurant_id INTEGER REFERENCES restaurants
    ON DELETE CASCADE,
    category_id INTEGER REFERENCES review_categories
    ON DELETE CASCADE
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    content TEXT,
    sent_at TIMESTAMP,
    restaurant_id INTEGER REFERENCES restaurants
    ON DELETE CASCADE
);

CREATE TABLE info (
    id SERIAL PRIMARY KEY,
    description TEXT,
    opening TIME,
    closing TIME,
    tags TEXT[],
    restaurant_id INTEGER REFERENCES restaurants
    ON DELETE CASCADE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    pwhash TEXT,
    role TEXT
);