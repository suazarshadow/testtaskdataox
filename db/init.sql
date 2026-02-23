CREATE DATABASE сarstest;

CREATE USER scraper_agent WITH PASSWORD 'D7Apd9MCSf3C';


\c сarstest;


GRANT ALL ON SCHEMA public TO scraper_agent;
ALTER SCHEMA public OWNER TO scraper_agent;


CREATE TABLE cars (
    id BIGSERIAL PRIMARY KEY,

    url TEXT NOT NULL UNIQUE,              
    title TEXT,
    price_usd NUMERIC(12,2),                
    odometer BIGINT,                        

    username TEXT,
    phone_number BIGINT,                    

    image_url TEXT,
    images_count INT,

    car_number TEXT,
    car_vin TEXT,

    datetime_found TIMESTAMPTZ DEFAULT NOW(),   
    last_updated TIMESTAMPTZ DEFAULT NOW()      
);


CREATE UNIQUE INDEX idx_cars_url ON cars(url);

CREATE INDEX idx_cars_price ON cars(price_usd);
CREATE INDEX idx_cars_title ON cars(title);

CREATE INDEX idx_cars_vin ON cars(car_vin);
CREATE INDEX idx_cars_number ON cars(car_number);
CREATE INDEX idx_cars_phone ON cars(phone_number);


GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO auto_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO auto_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO auto_user;


ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO auto_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO auto_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON FUNCTIONS TO auto_user;


GRANT CONNECT, CREATE, TEMP ON DATABASE auto_scraper TO auto_user;

