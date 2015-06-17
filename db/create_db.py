# -*- coding: utf-8 -*-

import os
import sqlite3

if __name__ == '__main__':

    # データベースアクセス

    path = os.path.dirname( os.path.abspath(__file__))
    connect = sqlite3.connect(path + "/hatena.db")
    cursor = connect.cursor()

    # テーブル作成

    sql = """
    CREATE TABLE hatebu_list (
        id INTEGER PRIMARY KEY, 
        channel VARCHAR(128),
        word TEXT, 
        bookmark_count INTEGER,
        last_post TEXT
    );
    """

    # テーブル確認

    cursor.execute(sql)

    sql = """ 
    SELECT * FROM sqlite_master;
    """

    con = cursor.execute(sql)
    for row in con:
        print(row)

    # テストデータ挿入

    sql = """ 
    INSERT INTO hatebu_list (
         channel, 
         word, 
         bookmark_count, 
         last_post) 
         VALUES ( 
         ?,?,?,?
    );
    """

    cursor.execute(sql,('general', 'Linux', 30, '2000-01-01T00:00:00+09:00'))

    # テストデータ確認

    sql = """
    SELECT * FROM hatebu_list;
    """

    con = cursor.execute(sql)
    for row in con:
        print(row)

    # 変更を更新する
    connect.commit()

    # データベースを閉じる
    connect.close()
