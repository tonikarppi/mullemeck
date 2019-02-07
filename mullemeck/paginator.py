class Paginator:
  def __init__(self, list, per_page):
    self.per_page = per_page
    self.list = []
    i = len(list)
    j = 0
    while(i > -per_page):
      self.list.append([])
      for y in range(0, per_page):
        if((i-y) <= 0):
          break
        self.list[j].append(list[j*per_page+y])
      j += 1
      i -= per_page
