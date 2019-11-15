# あまり良くない使い方
class Msg:
  @classmethod
  def pogMsg(self, type):
    msg = {
      'URL_ERROR': 'URLがPOGスタリオンのサイトではありません。'
    }
    return msg[type]

  @classmethod
  def common(self, type):
    msg = {
      'URL_NOT_FOUND': 'URLが無効です。'
    }
    return msg[type]
