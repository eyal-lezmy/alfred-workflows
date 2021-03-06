#!/usr/bin/python
# encoding: utf-8

import re
import sys
from workflow import Workflow, web

base_url = 'http://www.tobest2.net'

type = {
    11: 'torrent_music_kor',
    12: 'torrent_movie_kor',
    13: 'torrent_kortv_ent',
    14: 'torrent_kortv_social',
    15: 'torrent_kortv_drama',
    21: 'torrent_music_eng',
    22: 'torrent_movie_eng',
    23: 'torrent_engtv_ent',
    24: 'torrent_engtv_social',
    25: 'torrent_engtv_drama'
}

def main(wf):

    if len(wf.args):
        args = wf.args[0].split()
    else:
        args = []

    if len(args) > 1:
        try:
            table = type[int(args[0].replace('\\', ''))]
        except KeyError:
            table = type[11]

        query = args[1].strip()
        params = dict(bo_table = table,
                      sfl = 'wr_subject',
                      sop = 'and',
                      stx = query)

    elif len(args) == 1 and len(args[0]) == 2:
        try:
            table = type[int(args[0])]
        except KeyError:
            table = type[11]

        params = dict(bo_table = table)
    else:
        params = None

    url = base_url + '/bbs/board.php'

    if len(args) > 1:
        search(web.get(url, params).text)
    elif len(args) == 1 and len(args[0]) == 2:
        top10(web.get(url, params).text)

    wf.send_feedback()


def top10(page):
    from bs4 import BeautifulSoup as Soup

    soup = Soup(page)

    rows = soup.find_all("li", class_=re.compile("^hot_icon_.*"))

    for row in rows:
        link = row.find("a")
        href = link["href"]
        # arg_link = ("%s/%s" % (base_url, href)).replace("../", "")
        title = link.find("div").string

        wf.add_item(title = title,
                    arg = href,
                    valid = True)


def search(page):
    from bs4 import BeautifulSoup as Soup

    soup = Soup(page)

    table = soup.find("table", "table")
    tbody = table.find('tbody')
    rows = tbody.find_all("tr")

    for row in rows:
        column = row.find("td", "td_subject")
        link = column.find("a")
        href = link["href"]
        # arg_link = ("%s/%s" % (base_url, href)).replace("../", "")
        date = row.find("td", "td_date").string
        size = row.find_all("td", "td_num")[-1].string

        wf.add_item(title = ''.join(link.strings),
                    subtitle = ("%s / %s" % (date, size)),
                    arg = href,
                    valid = True)


if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))
