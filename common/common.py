import datetime

class Common:
  @classmethod
  def strWeekDays(self):
    DIFF_JST_FROM_UTC = 9
    jaTime = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    return [(jaTime + datetime.timedelta(days=i)).strftime("%Y%m%d") for i in range(1, 8)]
