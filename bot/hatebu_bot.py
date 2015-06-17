# -*- coding: utf-8 -*-
 
from urllib3 import PoolManager
import urllib
import feedparser
import datetime
 
class Hatebu(object):
 
    http = None
 
    def __init__(self):
 
        self.http = PoolManager()
 
    def get_rss_data(self, word, threshold):
        """
        はてブから キーワード( = word)、ブックマーク数 (= threshold)を基に
        xmlデータを取得してくるメソッド
        """
 
        url = urllib.request.quote("b.hatena.ne.jp/keyword/{0}?mode=rss&sort=current&threshold={1}".format(str(word), str(threshold)))
 
        response = self.http.request_encode_url('GET', url)
        result = response.data.decode('utf-8')
 
        return result
 
    def parse_xml_data(self, xml):
        """
        取得してきたXMLデータを解析して必要な情報のみを抜き出す。
        """
 
        result = []
 
 
        feed = feedparser.parse(xml)
 
        """
        各ブックマークは、XMLデータのentriesタグの中にItemタグ単位で保存されている。
        feed["entries"]でentriesの中から一つずつItemを取り出し、dataに格納する。
        dataは、Itemタグ内のtitleやdateの情報がparse関数によってdict型に変換されて
        格納されているため、data["title"]などで必要な情報が得られる。
        """

        for data in feed["entries"]:

            # hatebu_bookmarkcountの項目がない場合があるため、項目がある場合のみ取得 
            if "hatena_bookmarkcount" in data.keys():
 
                tmp = dict(title=data["title"],
                           date=data["date"],
                           url=data["links"][0]["href"],
                           bookmark_count=data["hatena_bookmarkcount"])
                result.append(tmp)
 
        # resultにブックマークを格納した時に、取得した順と逆に格納されてしまうため、取得順になるように reversed関数で配列を逆順にしている。
        return reversed(result)
 
if __name__ == "__main__":
 
    hatebu = Hatebu()
    xml = hatebu.get_rss_data("Linux", 30)
    parse = hatebu.parse_xml_data(xml)
 
    for d in parse:
        print(d["date"])

