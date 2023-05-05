from data_spider import Spider, StorageType, Storage, Rule
from bs4 import BeautifulSoup


# def parse_func(response):
#     # print(response)
#     # 将HTML页面解析为BeautifulSoup对象
#     soup = BeautifulSoup(response, 'html.parser')
#     # 找到所有的h2标签
#     h2_tags = soup.find_all('div')
#     # 提取出h2标签中的文本，并将其存储在列表中
#     titles = [tag.text for tag in h2_tags]
#     return titles

def yield_urls(url: str, pages: int):
    for i in range(pages):
        yield f"{url}/{i + 1}"


if __name__ == '__main__':
    spider = Spider()
    # parser = Rule(
    #     tag="a",
    #     attrs={
    #         "class": "name"
    #     },
    #     children=[
    #         Rule(tag="h2", attrs={"class": "m-b-sm"}, display={"text": True})
    #     ],
    #     display={"text": True}
    # )
    parser = Rule(
        "电影信息数据集",
        tag="div",
        attrs={
            "class": "el-card__body"
        },
        children=[
            Rule("电影名", tag="h2", attrs={"class": "m-b-sm"}, display={"text": True}),
            Rule("电影类型", tag="div", attrs={"class": "categories"}, display={"text": True}),
            Rule("影片信息", tag="div", attrs={"class": "m-v-sm info"}, display={"text": True})
        ]
    )
    spider.set_params(
        start_urls=yield_urls("https://ssr1.scrape.center/page", 2),
        rule=parser,
        storage_func=Storage("./test.csv", StorageType.CSV),
        thread_num=2
    )
    spider.start()
