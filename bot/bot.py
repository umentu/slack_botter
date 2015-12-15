# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
import datetime 

# ライブラリのパスを追加
sys.path.append( os.path.dirname(__file__) )

from hatebu_bot import Hatebu
from slack_bot import Slack

def judge_new_date(current, new):
    """
    はてブから取得した日付がデータベースのlast_postより新しい日付かを判定する
    """

    current_datetime = datetime.datetime.strptime(current, "%Y-%m-%dT%H:%M:%S+09:00")
    new_datetime = datetime.datetime.strptime(new, "%Y-%m-%dT%H:%M:%S+09:00")

    return current_datetime < new_datetime


if __name__ == "__main__":

    hatebu = Hatebu()
    slack = Slack("SlackのToken")

    # データベースアクセス
    path = os.path.dirname(os.path.dirname( os.path.abspath(__file__))) + "/db"
    connect = sqlite3.connect(path + "/hatena.db")
    cursor = connect.cursor()

    sql = """
    SELECT * FROM hatebu_list
    """

    con = cursor.execute(sql)
    for row in con:

        (idx, channel, word, bookmark_count, last_post) = row
        xml = hatebu.get_rss_data(word, bookmark_count)
        parse_data = hatebu.parse_xml_data(xml)

        for data in parse_data:
            
            # last_post より はてブから取得した日付が 新しい場合はslackに投稿する。
            if judge_new_date(last_post, data["date"]):

                last_post = data["date"]
                message = """
                ブックマーク数: {0}
                タイトル: {1}
                URL: {2} 
                """.format(data["bookmark_count"], data["title"], data["url"])
                
                # slackに投稿する。
                slack.post_message_to_channel(channel, message)

                # データベースのlast_postを更新する
                sql = """
                UPDATE hatebu_list SET last_post = ? WHERE id = ?
                """
                cursor.execute(sql, (last_post, idx))
    
    # データベースの変更を更新
    connect.commit()
    # データベースを閉じる
    connect.close()

