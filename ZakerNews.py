import requests
from bs4 import BeautifulSoup
import webbrowser
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

def printtitle(hotpoint, article, src):
    flag = 1
    print('-------------------HOT--------------------\n')
    for a in hotpoint:
        print('[%d]' % flag + a['title'])
        flag += 1
        #print('链接：\thttps:' + a['href'] + '\n')
    print('\n------------------------------------------\n')
    for i in range(0, len(article)):
        print('[%d]' % flag + article[i].a['title'] + '\t来源：' + src[i].a['title'])
        #print('来源：' + src[i].a['title'])
        flag += 1
        #print('链接：\thttps:' + article[i].a['href'] + '\n')

def printarticle(url):
    re = requests.get(url, headers = header)
    bs = BeautifulSoup(re.text, 'lxml')
    title = bs.find('h1', attrs={'class': 'article-title'})
    content = bs.find('div', id='content')
    print('\033[1;47m\033[1;30m%s\033[0m\033[0m' % title.text)
    print(content.get_text('\n'))

def jumper(url):
    re = requests.get(url, headers=header)
    bs = BeautifulSoup(re.text, 'lxml')
    origin = bs.find('div', attrs={'class': 'from'})
    webbrowser.open_new_tab(origin.a['href'])

def main():
    r = requests.get('http://www.myzaker.com/', headers=header)

    # print(r.status_code)

    soup = BeautifulSoup(r.text, 'lxml')

    hotpoint = soup.find_all('a', attrs={'class': 'carousel'})

    article = soup.find_all('div', attrs={'class': 'article-wrap'})
    src = soup.find_all('div', attrs={'class': 'article-footer'})
    printtitle(hotpoint, article, src)
    # flag = 1
    # print('-------------------HOT--------------------\n')
    # for a in hotpoint:
    #     print('[%d]' % flag + a['title'])
    #     flag += 1
    #     #print('链接：\thttps:' + a['href'] + '\n')
    # print('\n------------------------------------------\n')
    # for i in range(0, len(article)):
    #     print('[%d]' % flag + article[i].a['title'] + '\t来源：' + src[i].a['title'])
    #     #print('来源：' + src[i].a['title'])
    #     flag += 1
    #     #print('链接：\thttps:' + article[i].a['href'] + '\n')
    # #webbrowser.open_new_tab('https:' + article[0].a['href'])
    while 1:
        par = input('Please input the news num to review detail(Input \'exit\' to exit):')
        if par == 'exit':
            return
        try:
            par = int(par)
            if par < 1 or par >= len(hotpoint)+len(article):
                print('Num error, input again!')
            else:
                if par <= len(hotpoint):
                    printarticle('https:' + hotpoint[par-1]['href'])
                else:
                    printarticle('https:' + article[par-len(hotpoint) - 1].a['href'])
                while 1:
                    act = input('Please input \'r\' to return or input \'o\' jump to the original web:')
                    if act == 'r':
                        printtitle(hotpoint, article, src)
                        break
                    elif act == 'o':
                        if par <= len(hotpoint):
                            jumper('https:' + hotpoint[par-1]['href'])
                        else:
                            jumper('https:' + article[par-len(hotpoint) - 1].a['href'])
                    else:
                        print('Input error, please try again!')
        except ValueError as e:
            print('Input error, please try again!')

if __name__ == '__main__':
    main()
