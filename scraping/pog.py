from scraping.scraping import Scraping

class Pog(Scraping):
  def __init__(self, url):
    super().__init__(url)
    self.users, self.prizes, self.recents, self.urls = \
      self.getString('td.user'), \
      self.getString('td.money'), \
      self.getString('td.recent'), \
      self.getUrl('td.user > a')
  def topHeader(self):
    return [
        '順位',
        *self.getString('th.user'),
        *self.getString('th.money'),
        # なぜか認識しないため直書き
        # self.getString('th.recent')
        '直近'
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
    return {
      'header' : self.topHeader(),
      'tbody' : self.topBody()
    }
      

