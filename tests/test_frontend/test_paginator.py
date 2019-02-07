from mullemeck.paginator import Paginator


def test_paginate_number_list():
    list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    per_page = 5
    paginated_list = Paginator(list, per_page)
    assert(paginated_list.list[0][0] == 0)
    assert(paginated_list.list[0][1] == 1)
    assert(paginated_list.list[0][2] == 2)
    assert(paginated_list.list[0][3] == 3)
    assert(paginated_list.list[0][4] == 4)
    assert(paginated_list.list[1][0] == 5)
    assert(paginated_list.list[1][1] == 6)
    assert(paginated_list.list[1][2] == 7)
    assert(paginated_list.list[1][3] == 8)
    assert(paginated_list.list[1][4] == 9)
    assert(paginated_list.list[2][0] == 10)
    assert(paginated_list.list[2][1] == 11)
    assert(paginated_list.list[2][2] == 12)
    assert(paginated_list.list[2][3] == 13)
    assert(paginated_list.list[2][4] == 14)
    assert(paginated_list.list[3][0] == 15)
    assert(paginated_list.list[3][1] == 16)
    assert(paginated_list.list[3][2] == 17)


def test_paginate_single_items():
    list = [0, 1, 2, 3, 4]
    per_page = 1
    paginated_list = Paginator(list, per_page)
    assert(paginated_list.list[0][0] == 0)
    assert(paginated_list.list[1][0] == 1)
    assert(paginated_list.list[2][0] == 2)
    assert(paginated_list.list[3][0] == 3)
    assert(paginated_list.list[4][0] == 4)
