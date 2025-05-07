
def paged_list(total, page=1, paging_line=5, row_size=10):
    page = int(page or 1)
    row_size = int(row_size or 10)
    page_num = (page - 1) * row_size

    start_page = (page - 1) // paging_line * paging_line + 1
    end_page = ((total + row_size - 1) // row_size) + 1

    pre_page_yn = start_page > 1
    next_page_yn = start_page + paging_line < end_page
    next_page = min(start_page + paging_line, end_page)
    max_page = min(next_page, end_page)

    return {
        'page': page,
        'page_num': page_num,
        'row_size': row_size,
        'end_page': end_page,
        'start_page': start_page,
        'pre_page_yn': pre_page_yn,
        'pre_page': max(1, start_page - 1),
        'next_page_yn': next_page_yn,
        'next_page': next_page,
        'max_page': max_page,
    }

