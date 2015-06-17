# -*- coding: utf-8 -*-
 
import os
import sys
import csv

# sqlite3をインポート
import sqlite3

# slack_botライブラリもインポート
sys.path.append( os.path.dirname(__file__) )
from slack_bot import Slack

from bottle import route, run
from bottle import TEMPLATE_PATH, jinja2_template as template
from bottle import static_file
from bottle import get, post, request, response
from bottle import redirect 


# sites.pyが設置されているディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# テンプレートファイルを設置するディレクトリのパスを指定
TEMPLATE_PATH.append(BASE_DIR + "/views")

@route('/css/<filename>')
def server_css(filename):
    """ setting for css file """
    return static_file(filename, root=BASE_DIR+"/static/css")

@route('/js/<filename>')
def server_js(filename):
    """ setting for js file """
    return static_file(filename, root=BASE_DIR+"/static/js")

@route('/img/<filename>')
def server_img(filename):
    """ setting for img file """
    return static_file(filename, root=BASE_DIR+"/static/img")

@route('/font/<filename>')
def server_font(filename):
    """ setting for font file """
    return static_file(filename, root=BASE_DIR+"/static/fonts") 


@route('/hatebu')
@route('/hatebu/')
def hatebu():

    # データベースアクセス

    path = os.path.dirname(os.path.dirname( os.path.abspath(__file__))) + "/db"
    connect = sqlite3.connect(path + "/hatena.db")
    cursor = connect.cursor()

    # hatebu_list テーブルからデータを取得
    sql = """ 
    SELECT * FROM hatebu_list
    """ 

    # 取得したデータをパースしてリストに保存

    hatebu_list = []
    con = cursor.execute(sql)
    for row in con:
        tmp_row = {}
        for idx, col in enumerate(cursor.description):
            tmp_row[col[0]] = row[idx]

        hatebu_list.append(tmp_row)            

    connect.close()

    # Slackのチャンネル一覧を取得
    slack = Slack("SlackのToken")
    channel_list = slack.get_channnel_list()

    return template('hatebu', hatebu_list=hatebu_list, channel_list=channel_list)


@route('/hatebu_create', method='GET')
def hatebu_create():

    # 作成ボタンが押されずに/hatebu_createにアクセスが来たらリダイレクト
    if request.query.create is None:
        redirect("/hatebu")

    # データベースアクセス
    path = os.path.dirname(os.path.dirname( os.path.abspath(__file__))) + "/db"
    connect = sqlite3.connect(path + "/hatena.db")
    cursor = connect.cursor()

    sql = """ 
    INSERT INTO hatebu_list (
         channel, 
         word, 
         bookmark_count, 
         last_post) 
         VALUES ( 
         ?, 
         ?, 
         ?, 
         ?);
    """

    channel = request.query.channel
    word = request.query.word
    bookmark_count = request.query.bookmark_count
    last_post = '2000-01-01T00:00:00'

    # データベースにデータを挿入
    cursor.execute(sql,(channel,word,bookmark_count,last_post))

    # 変更を更新する
    connect.commit()

    # データベースを閉じる
    connect.close()

    # 元ページにリダイレクト
    redirect("/hatebu")


@route('/hatebu_updel', method='GET')
def hatebu_updel():

    # 作成ボタンが押されずに/hatebu_createにアクセスが来たらリダイレクト
    if request.query.updel is None:
        redirect("/hatebu")

    # データベースアクセス
    path = os.path.dirname(os.path.dirname( os.path.abspath(__file__))) + "/db"
    connect = sqlite3.connect(path + "/hatena.db")
    cursor = connect.cursor()

    if request.query.updel == "更新":
        # 更新ボタンが押された場合

        sql = """ 
        UPDATE hatebu_list SET
             channel = ?, 
             word = ?, 
             bookmark_count = ? 
             WHERE id = ?;
        """

        idx = request.query.id
        channel = request.query.channel
        word = request.query.word
        bookmark_count = request.query.bookmark_count

        # データベースにデータを挿入
        cursor.execute(sql,(channel,word,bookmark_count,idx))

    else:
        # 削除ボタンが押された場合

        sql = """ 
        DELETE FROM hatebu_list WHERE id = ?;
        """

        idx = request.query.id

        # データベースにデータを挿入
        cursor.execute(sql,(idx))

    # 変更を更新する
    connect.commit()

    # データベースを閉じる
    connect.close()

    # 元ページにリダイレクト
    redirect("/hatebu")


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)

