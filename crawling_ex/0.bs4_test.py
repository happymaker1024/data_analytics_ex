html_doc = """
<html>
 <head>
  <title>
   The Dormouse's story
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    The Dormouse's story
   </b>
  </p>
  <p class="story">
   Once upon a time there were three little sisters; and their names were
   <a class="sister" href="http://example.com/elsie" id="link1">
    Elsie
   </a>
   ,
   <a class="sister" href="http://example.com/lacie" id="link2">
    Lacie
   </a>
   and
   <a class="sister" href="http://example.com/tillie" id="link2">
    Tillie
   </a>
   ; and they lived at the bottom of a well.
  </p>
  <p class="story">
   ...
  </p>
 </body>
</html>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())

# print(soup.title)
# print(soup.title.string)
# print("-"*30)
# print(soup.select_one('title'))
# print(soup.select_one('title').get_text())
# <title>The Dormouse's story</title>

# print(soup.title.name)
# print(soup.title.parent.name)  # head
# print(soup.p)
# print(soup.p['class'])
# print(soup.a)
# -------------------
# 첫번째 p 태그를 선택 하는 방법
# p.select_one('p'))
# p태그 모두 선택하기
p_eles = soup.select('p')
for p in p_eles:
    # print(p)
    print(p.get_text().strip())
    print("-"*30)