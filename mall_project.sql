-- CREATE TABLE Products (
--     product_id VARCHAR(10) PRIMARY KEY,
--     product_name VARCHAR(50),
--     price INT,
--     stock_quantity INT,
--     safety_stock INT
-- );

-- insert INTO Products VALUES
--     ("A001", "기본 반팔티(White)", 15000, 100, 10),
--     ("B002", "와이드 데님 팬츠", 39000, 50, 5),
--     ("C003", "오버핏 후드티", 45000, 30, 5);

-- CREATE TABLE Orders (
--     order_id INT PRIMARY KEY,
--     customer_name VARCHAR(20),
--     product_id VARCHAR(10),
--     quantity INT,
--     order_date DATE,
--     FOREIGN KEY (product_id) REFERENCES Products(product_id)
-- );

-- INSERT INTO Orders VALUES
--     (1, '김철수', 'A001', 2, '2026-01-29'),
--     (2, '이영희', 'B002', 1, '2026-01-29'),
--     (3, '박민수', 'A001', 5, '2026-01-30');

-- SELECT 
--     o.order_date,
--     o.customer_name,
--     p.product_name,
--     o.quantity,
--     p.price
-- FROM Orders AS o
-- JOIN Products AS p
-- ON o.product_id = p.product_id;

-- UPDATE Products
-- SET stock_quantity = 98
-- WHERE product_id = "A001"; --재고 변경

-- UPDATE Products
-- SET stock_quantity = stock_quantity - 2 --주문 수량만큼 뺴기
-- WHERE product_id = "A001";

-- SELECT *
-- FROM Products
-- WHERE product_id = "A001";