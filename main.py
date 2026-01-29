import sqlite3
import pandas as pd

#db 환경 세팅(매번 초기화)

conn = sqlite3.connect(r'Data\shopping_mall.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Products")
cursor.execute("DROP TABLE IF EXISTS Orders")

cursor.execute("""
    CREATE TABLE Products (
        product_id VARCHAR(10) PRIMARY KEY,
        product_name VARCHAR(50),
        stock_quantity INT,
        safety_stock INT
    )
""")
cursor.execute("""
    CREATE TABLE Orders (
        order_id INT PRIMARY KEY,
        product_id VARCHAR(10),
        quantity INT,
        order_date DATE
    )
""")

cursor.executemany('INSERT INTO Products VALUES (?, ?, ?, ?)', [
    ("A001", '기본 반팔티', 10, 5),
    ("B002", '와이드 데님', 2, 5)
])
conn.commit()

#엑셀 주문서 불러오기
data = {
    '주문번호': [101, 101, 102],     # 101번이 두 번 있음 (중복 주문 테스트)
    '고객명': ['김철수', '김철수', '이영희'],
    '상품코드': ['A001', 'A001', 'B002'], 
    '수량': [6, 6, 5],               # A001: 6개 주문 (성공 예상), B002: 5개 주문 (재고 2개라 실패 예상)
    '날짜': ['2026-01-29', '2026-01-29', '2026-01-29']
}
df = pd.DataFrame(data)

print('주문서 확인')
print(df)

print('처리 시작')
for index, row in df.iterrows():
    order_id = row['주문번호']
    p_id = row['상품코드']
    order_qty = row['수량']
    
    # 중복 방지
    cursor.execute("SELECT count(*) FROM Orders WHERE order_id = ?", (p_id,))
    is_exist = cursor.fetchone()[0]
    
    if is_exist > 0:
        print('중복 확인')
        continue
    
    #재고 확인
    cursor.execute("SELECT stock_quantity, safety_stock, product_name FROM Products WHERE product_id = ?", (p_id,))
    product_info = cursor.fetchone()
    
    if not product_info:
        print("상품 커드 없음")
        continue
    
    print(product_info)
    current_stock = product_info[0]
    safety_stock = product_info[1]
    p_name = product_info[2]
    
    if current_stock < order_qty:
        print(f"{p_name} 재고 부족 (주문 {order_qty} 개 / 현재 {current_stock} 개)")
        continue
    
    cursor.execute("INSERT INTO Orders (order_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)", (order_id, p_id, order_qty, row["날짜"]))
    cursor.execute("UPDATE Products SET stock_quantity = stock_quantity - ? WHERE product_id = ?", (order_qty, p_id))
    
    print(f"{row['고객명']}님 주문 처리 완료 ({p_name} {order_qty}개 출고)")
    
    remain_stock = current_stock - order_qty
    if remain_stock <= safety_stock:
        print(f"{p_name} 재고가 {remain_stock}개 남음")
        
#최종 저장 및 마감
conn.commit()
conn.close()
print("종료")