CREATE TABLE categories(
	codename VARCHAR(255) PRIMARY KEY,
	name VARCHAR(255)
);

CREATE TABLE expenses(
	id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	category_codename VARCHAR(255),
    amount BIGINT,
	created_at DATE default NOW(),
    FOREIGN KEY (category_codename) REFERENCES categories (codename)
);

INSERT INTO categories(
    codename, name
    )
    VALUES
    ('products', 'продукты'),
    ('cafe', 'кафе'),
    ('car', 'авто'),
    ('transport', 'транспорт'),
    ('other', 'другое');
