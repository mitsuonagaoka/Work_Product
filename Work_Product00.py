# streamlit run Work_Product00.py

import sqlite3

import streamlit as st
import pandas as pd

# データベースに接続
db_name = 'product.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()

# テーブルの作成（初回のみ実行）
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    )
''')

def add_product(name, price, quantity):
    # 商品を追加
    c.execute('''
        INSERT INTO products (name, price, quantity)
        VALUES (?, ?, ?)
    ''', (name, price, quantity))
    conn.commit()

def get_all_products():
    # 全ての商品を取得
    c.execute('SELECT * FROM products')
    return c.fetchall()

# Streamlitアプリケーションの設定
def main():
    st.title('販売生産管理アプリ')

    # 商品追加フォーム
    st.header('商品追加')
    product_name = st.text_input('商品名')
    product_price = st.number_input('価格', step=0.01)
    product_quantity = st.number_input('数量', step=1)

    if st.button('追加'):
        add_product(product_name, product_price, product_quantity)
        st.success('商品を追加しました')

    # 商品一覧表示
    st.header('商品一覧')

    # t_受注Dataテーブルからデータを読み込む
    db_name = 'product.db'
    conn = sqlite3.connect(db_name)
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    pd.DataFrame(rows, columns=['番号', '名称', '価格', '数量'])

    # 品番を入力する
    search_term = st.text_input('品番を入力してください')

    # 品番でフィルタリングする
    if search_term:
        query = f"SELECT * FROM products WHERE id LIKE '%{search_term}%'"
    else:
        query = "SELECT * FROM products"
    df = pd.read_sql(query, conn)
    conn.close()

    # データフレームを表示
    st.write(df)


# アプリの実行
if __name__ == '__main__':
    main()


# streamlit run Work_Product00.py
