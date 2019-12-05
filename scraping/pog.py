from scraping.scraping import Scraping
from common.msg import Msg

# ベタ書き
class Pog(Scraping):
  def __init__(self, url):
    super().__init__(url)
    self.POGSTARION = "pogstarion.com"
  def topHeader(self):
    # 配列をアンパック
    user,*_ = self.getString('th.user');
    prize, *_ = self.getString('th.money')
    return [
        {'text': '順位', 'value': 'order'},
        {'text': user, 'value': 'user'},
        {'text': prize, 'value': 'prize'},
        # なぜか認識しないため直書き
        # self.getString('th.recent')
        {'text': '直近', 'value': 'recent'}
    ]
  def topBody(self):
    all = zip(self.getString('td.user'), 
              self.getString('td.money'),
              self.getString('td.recent'),
              self.getUrl('td.user > a'))
    tbody = []
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
  def eachPHeader(self):
    horse,*_ = self.getString('th.bamei')
    birth,*_ = self.getString('th.birthyear')
    house,*_ = self.getString('th.zaikyuflag')
    result,*_ = self.getString('th.sogochakukaisu1')
    prize,*_ = self.getString('th.gokei_syokin')
    recent,*_ = self.getString('th.new_syokin')
    coach,*_ = self.getString('th.chokyosiryakusyo')
    blood,*_ = self.getString('th.ketto')
    return [
        {'text': 'No', 'value': 'order'},
        {'text': horse, 'value': 'horse'},
        {'text': birth, 'value': 'birth'},
        {'text': house, 'value': 'house'},
        # {'text': result, 'value': 'result'},
        {'text': prize, 'value': 'prize'},
        # {'text': recent, 'value': 'recent'},
        # {'text': coach, 'value': 'coach'},
        # {'text': blood, 'value': 'blood'},
    ]
  def eachPBody(self):
    all = zip(self.getString(self.eachPtd(2)),
              self.getString(self.eachPtd(4)),
              self.getString(self.eachPtd(5)),
              self.getString(self.eachPtd(6)),
              self.getString(self.eachPtd(8)),
              self.getString(self.eachPtd(9)),
              self.getString(self.eachPtd(10)),
              self.getString(self.eachPtd(12)),
              )
    tbody = []
    cnt = 1
    for horse, birth, house, result, prize, recent, coach, blood in all:
      tbody.append({
          'order': cnt,
          'horse': horse,
          'birth': birth,
          'house': house,
          'result': result,
          'prize': prize,
          'recent': recent,
          'coach': coach,
          'blood': blood,
      })
      cnt += 1
    return tbody
  def eachPtd(self, i):
    return '.umalist_comment > tbody > tr > td:nth-child({0})'.format(i)
  
  def eachP(self):
    # 表の関係上一部データをコメントで省略する
    # ヘッダのみ削除しているので、データとしては送っている
    return {
        'header': self.eachPHeader(),
        'tbody': self.eachPBody()
    }

  def horseHeader(self):
   return [
       {'text': 'No', 'value': 'order'},
       {'text': '馬名', 'value': 'horse'},
       {'text': '賞金', 'value': 'prize'},
       {'text': 'ユーザー名', 'value': 'user'},
   ]

  def horseBody(self):
    urls = self.getUrl('td.user > a')
    users = self.getString('td.user')
    tbody = []
    for i, (url, user) in enumerate(zip(urls, users)):
      scr = Scraping(url)
      horses = scr.getString(self.eachPtd(2))
      prizes = scr.getString(self.eachPtd(8))
      # 1行ずつのデータを作成
      for i, (horse, prize) in enumerate(zip(horses, prizes), 1):
        tbody.append({
          'user': user,
          'horse': horse,
          'prize': int(prize)
        })
    # 辞書のリストをソード
    # reverse=True   降順
    return sorted(tbody, key=lambda x:x['prize'], reverse=True)
    
  def horse(self):
    if not self.parsedUrl.netloc == self.POGSTARION:
      return {"error": Msg.pogMsg("URL_ERROR")}
    return {
      'header': self.horseHeader(),
      'tbody': self.horseBody()
    }


  def getHouseHorseNames(self):
    urls = self.getUrl('td.user > a')
    users = self.getString('td.user')
    runners = []
    for url, user in zip(urls, users):
      scr = Scraping(url)
      horses = scr.getString(self.eachPtd(2))
      houses = scr.getString(self.eachPtd(5))
      horseUrls = scr.getUrl(self.eachPtd(2) + " > a")
      for horse, house, horseUrl in zip(horses, houses, horseUrls):
        if not house == 'Ｏ':
          continue
        runners.append({'user': user, 'horse': horse})
    return runners

  # targetHorses [A,B,C]
  # compareHorses [{name: ,horse:},{..}...]
  # return matched index of compareHorses
  def hasMatchingHorse(self, targetHorses, compareHorses, favs, raceInfo):
    willRaceIndex = []
    for i, (targetHorse, fav) in enumerate(zip(targetHorses,favs)):
      for compareHorse in compareHorses:
        if compareHorse['horse'] == targetHorse:
          compareHorse.update(**raceInfo)
          compareHorse['fav'] = fav
    return compareHorses

 
  def getRaceUrls(self):
    urls = []
    raceListUrls = Scraping('https://race.netkeiba.com/?pid=race_list').getUrl('#race_list_header > dd > a')
    # 未発走のみにする
    futureRaceUrls = list(filter(lambda n: not 'id=p' in n, raceListUrls))
    for raceDateUrl in futureRaceUrls:
      racesUrl = Scraping(raceDateUrl).getUrl('.racename > a')
      for raceUrl in racesUrl:
        urls.append(raceUrl)
    return urls


  def race(self):
    if not self.parsedUrl.netloc == self.POGSTARION:
      return {"error": Msg.pogMsg("URL_ERROR")}
    
    names = self.getHouseHorseNames()
    urls = self.getRaceUrls()
    return {
        'header': [
            {'text': 'ユーザ名', 'value': 'user'},
            {'text': '開催日', 'value': 'date'},
            {'text': '開催地', 'value': 'place'},
            {'text': 'レース', 'value': 'round'},
            {'text': 'タイトル', 'value': 'title'},
            {'text': '距離', 'value': 'distance'},
            {'text': '馬名', 'value': 'horse'},
            {'text': '人気', 'value': 'fav'},
            {'text': '賞金', 'value': 'prize'},
            {'text': '詳細', 'value': 'detail'},
        ],
        'urls': urls,
        'names':names
    }

  def raceEach(self, horse):
      horseNames = self.getString(".horsename > div > a")
      favs = self.getString(".bml")
      raceInfo = {
          'place': self.getString('.race_place > ul > li > .active')[0],
          'round': self.getString('.race_num > ul > li > .active')[0],
          'title': self.getString('.racedata > dd > h1'),
          'distance': self.getString('.racedata > dd > p')[0],
          'detail': self.getString('.racedata > dd > p')[1],
          'date': self.getString('.race_otherdata > p')[0],
          'prize': self.getString('.race_otherdata > p')[3].strip('本賞金：'),
          'url': self.url
      }
      return {'raceHorse': self.hasMatchingHorse(horseNames, horse, favs, raceInfo)}
    
