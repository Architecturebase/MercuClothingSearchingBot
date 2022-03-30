# from new_image_demo import
import asyncio

from tqdm import tqdm

from bs4 import BeautifulSoup
from requests_html import HTMLSession, AsyncHTMLSession
import random
from new_image_demo import detectioner
wb_short_sleeve_top_male = ['мужская+футболка', 'мужская+рубашка+с+коротким+рукавом', 'мужское+поло']
wb_short_sleeve_top_female = ['женская+сорочка', 'женская+футболка', 'женская+рубашка+с+коротким+рукавом',
 'женское+поло']

wb_long_sleeve_top_male = ['мужская+рубашка', 'мужская+сорочка', 'мужская+ветровка', 'мужское+худи', 'мужской+свитер',
 'мужской+кардиган']
wb_long_sleeve_top_female = ['женская+блузка','женская+рубашка','женское+худи','женская+кофта','женский+свитер',
                             'женский+кардиган']
wb_short_sleeve_outwear_female = ['женская+жилетка', 'женская+куртка+с+коротким+рукавом']
wb_short_sleeve_outwear_male = ['мужская+жилетка', 'мужская+куртка+с+коротким+рукавом']

wb_long_sleeve_outwear_female = ['женская+куртка', 'женский+пуховик', 'женская+ветровка', 'женское+пальто']
wb_long_sleeve_outwear_male = ['мужская+куртка', 'мужской+пуховик', 'мужская+ветровка', 'мужское+пальто']

wb_vest_male = ['мужская+майка']
wb_vest_female = ['женская+майка']

wb_sling_male = ['мужская+майка']
wb_sling_female = ['женская+майка']

wb_shorts_male = ['мужские+шорты', 'мужские+шорты+спортивные', 'мужские+шорты+джинсовые', 'мужские+шорты+для+купания']
wb_shorts_female = ['женские+шорты', 'женские+шорты+джинсовые', 'женские+шорты+спортивные']

wb_trousers_male = ['мужские+брюки', 'мужские+штаны', 'мужские+джинсы', 'мужские+брюки+карго', 'мужские+брюки+спортивные',
 'мужские+брюки+чинос']
wb_trousers_female = ['женские+брюки', 'женские+штаны', 'женские+джинсы', 'женские+брюки+спортивные', 'женские+лосины']

wb_short_sleeve_dress = ['платье+с+коротким рукавом']
wb_long_sleeve_dress = ['платье+с+длинным рукавом']

wb_vest_dress = ['платье+без+рукавов']
wb_sling_dress = ['платье+без+плечей']

wb_cloth_type_male = {'short sleeve top': wb_short_sleeve_top_male, 'long sleeve top': wb_long_sleeve_top_male, 'short sleeve outwear':
                  wb_short_sleeve_outwear_male, 'long sleeve outwear': wb_long_sleeve_outwear_male, 'vest' : wb_vest_male, 'sling':
                  wb_sling_male, 'shorts' : wb_shorts_male, 'trousers': wb_trousers_male}
wb_cloth_type_female = {'short sleeve top': wb_short_sleeve_top_female, 'long sleeve top': wb_long_sleeve_top_female, 'short sleeve outwear':
                    wb_short_sleeve_outwear_female, 'long sleeve outwear': wb_long_sleeve_outwear_female, 'vest': wb_vest_female,
                    'sling':wb_sling_female, 'shorts': wb_shorts_female, 'trousers': wb_trousers_female, 'short sleeve dress': wb_short_sleeve_dress,
                    'long sleeve dress': wb_long_sleeve_dress, 'vest dress': wb_vest_dress, 'sling dress': wb_sling_dress}


# gender = input()
# cloth_type_id = []
# search_for_list = []
# if gender == 'мужская':
#     for i in range(len(cloth_type)):
#         cloth_type_id.append(i)
#         search_for = wb_cloth_type_male[cloth_type[i]]
#         search_for_list.append(search_for)
#         #дальше тут должен быть парсер
# elif gender == 'женская':
#     for i in range(len(cloth_type)):
#         cloth_type_id.append(i)
#         search_for = wb_cloth_type_female[cloth_type[i]]
#         search_for_list.append(search_for)
#         #дальше тут должен быть парсер
# detections = ['short sleeve top', 'long_sleeve_top']
# color = ['черный', 'синий', 'белый']
async def parsing_male(detections: list, color: list):
    links_list_male = []

    for item in detections:
        list_obj = []
        if item in wb_cloth_type_male:
            url1 = f"https://www.wildberries.ru/catalog/0/search.aspx?search={(color[0])}{random.choice(wb_cloth_type_male[item])}"
            url2 = f"https://www.wildberries.ru/catalog/0/search.aspx?search={color[0]}{random.choice(wb_cloth_type_male[item])}"
            # url3 = f"https://www.wildberries.ru/catalog/0/search.aspx?search={random.choice(color)}{random.choice(wb_cloth_type_male[item])}"
            urls = [url1, url2]

            for k in range(len(urls)):
                parse_res = await parsing(urls[k])
                # print(type(parse_res))
                # print(len(parse_res))

                for link in parse_res:
                    list_obj.append(link)
                    if len(list_obj) > 2:
                        break

        links_list_male.append(list_obj)
                # session = AsyncHTMLSession()
                #
                # async def links_grabber():
                #     response = session.get(urls[k])
                #
                #     await response.html.arender(sleep=3, keep_page=True, scrolldown=2)
                #
                #     soup = BeautifulSoup(response.html.raw_html, "html.parser")
                #
                #
                #     for link in soup.find_all('div', {'class': 'product-card__wrapper'}):
                #         links = link.find('a', href=True)
                #         links_list_male.append(links['href'])
                #
                #     await response.html.arender(sleep=1)
                # results = session.run(links_grabber())

    return links_list_male

async def parsing_female(detections: list, color: list):
    links_list_female = []

    for item in detections:
        list_obj = []
        if item in wb_cloth_type_female:
            url1 = f"https://www.wildberries.ru/catalog/0/search.aspx?search={color[0]}{random.choice(wb_cloth_type_female[item])}"
            url2 = f"https://www.wildberries.ru/catalog/0/search.aspx?search={color[0]}{random.choice(wb_cloth_type_female[item])}"
            # url3 = f"https://www.wildberries.ru/catalog/0/search.aspx?search={random.choice(color)}{random.choice(wb_cloth_type_male[item])}"
            urls = [url1, url2]

            for k in range(len(urls)):
                parse_res = await parsing(urls[k])
                # print(type(parse_res))
                # print(len(parse_res))

                for link in parse_res:
                    list_obj.append(link)
                    if len(list_obj) > 2:
                        break

        links_list_female.append(list_obj)

    return links_list_female

def links_returner(links_list_gender):
    if len(links_list_gender)>0:
        return random.choice(links_list_gender)


async def parsing (url):
    # url = #здесь должна быть ссылка, основанная на детекции типа одежды и цвета

    session = AsyncHTMLSession()

    response = await session.get(url)
    await asyncio.sleep(1)
    await response.html.arender(sleep=3, keep_page=True, scrolldown=2, timeout=15)

    soup = BeautifulSoup(response.html.raw_html, "html.parser")

    links_list = []
    for link in tqdm(soup.find_all('div', {'class': 'product-card__wrapper'})):
        links = link.find('a', href=True)
        links_list.append(links['href'])
    print(len(links_list))
    return links_list



# url = "https://www.wildberries.ru/catalog/0/search.aspx?search=черный+женские+брюки"
#
# session = HTMLSession()
#
# response = session.get(url)
# response.html.render(sleep=3, keep_page=True, scrolldown=2)
#
# soup = BeautifulSoup(response.html.raw_html, "html.parser")
#
# links_list = []
# for link in soup.find_all('div', {'class': 'product-card__wrapper'}):
#     links = link.find('a', href = True)
#     links_list.append(links['href'])
#     # print(links['href'])
#
# # for link in soup.findAll('a', {'class':'product-card__wrapper'}):
# #     try:
# #         print(link['href'])
# #     except KeyError:
# #         pass
# print(links_list)

def func(detections: list, color: list): #-> tuple

    return
