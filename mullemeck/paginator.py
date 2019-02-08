class Paginator:
    def __init__(self, list, per_page, pointer):
        self.per_page = per_page
        self.list = []
        self.number_of_items = len(list)
        self.pointer = pointer
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
        if self.number_of_items % per_page != 0:
            self.number_of_pages = (self.number_of_items // per_page) + 1
        else:
            self.number_of_pages = (self.number_of_items // per_page)

    def __str__(self):
        return_string = "Printing the paginator object!\n"
        for x in range(0, self.number_of_pages):
            return_string += "Member with index: "+str(x)+"\n ["
            for y in range(0, len(self.list[x])):
                return_string += " "+str(self.list[x][y])+", "
            return_string += "] \n"
        return return_string
