import scraping as scr

class Pog:
  def __init__(self, url):
    self.scr = scr.Scraping(url)
    self.users, self.prizes, self.recents, self.urls = \
      self.scr.getString('td.user'), \
      self.scr.getString('td.money'), \
      self.scr.getString('td.recent'), \
      self.scr.getUrl('td.user > a')
