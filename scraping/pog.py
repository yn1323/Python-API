from scraping.scraping import Scraping
from common.msg import Msg

class Pog(Scraping):
  def __init__(self, url):
    super().__init__(url)
    self.POGSTARION = "pogstarion.com"
    self.users, self.prizes, self.recents, self.urls = \
      self.getString('td.user'), \
      self.getString('td.money'), \
      self.getString('td.recent'), \
      self.getUrl('td.user > a')
  def topHeader(self):
    # 配列をアンパック
    user,*_ = self.getString('th.user');
    prize, *_ = self.getString('th.money')
    return [
        {'text': '順位', 'value': 'order'},
        {'text': user, 'value': 'user'},
        {'text': prize, 'valye': 'prize'},
        # なぜか認識しないため直書き
        # self.getString('th.recent')
        {'text': '直近', 'value': 'recent'}
    ]

  def topBody(self):
    tbody = []
    all = zip(self.users, self.prizes, self.recents, self.urls)
    cnt = 1
    for user, prize, recent, url in all:
      tbody.append({
          'order': cnt,
          'user': user,
          'prize': prize,
          'recent': recent,
          'url': url
      })
      cnt += 1
    return tbody
  def top(self):
    if not self.parsedUrl.netloc == self.POGSTARION:
      return {"error": Msg.pogMsg("URL_ERROR")}
    return {
      'header' : self.topHeader(),
      'tbody' : self.topBody()
    }
