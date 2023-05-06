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


def sub(data: str):
    data = data.replace(" ", "").replace("\n", "")
    return data


def del_null(data: str):
    if not data or data == '':
        return True
    return False


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
    # parser = Rule(
    #     "电影信息数据集",
    #     tag="div",
    #     attrs={
    #         "class": "el-card__body"
    #     },
    #     children=[
    #         Rule("电影名", tag="h2", attrs={"class": "m-b-sm"}, display={"text": True}),
    #         Rule("电影类型", tag="div", attrs={"class": "categories"}, display={"text": True}),
    #         Rule("影片信息", tag="div", attrs={"class": "m-v-sm info"}, display={"text": True})
    #     ]
    # )
    # spider.set_params(
    #     start_urls=yield_urls("https://ssr1.scrape.center/page", 2),
    #     rule=parser,
    #     storage_func=Storage("./test.csv", StorageType.CSV),
    #     thread_num=1
    # )

    # parser = Rule(
    #     "豆瓣新片排行数据集",
    #     tag="div",
    #     attrs={"class": "pl2"},
    #     children=[
    #         Rule("地址", tag="a", display={"href": True}, show=True, sep="|"),
    #         Rule("电影名", tag="a", display={"text": False}, show=True, sep="|")
    #     ]
    # )
    # spider.set_params(
    #     start_urls=["https://movie.douban.com/chart/"],
    #     rule=parser,
    #     storage_func=Storage("./test.csv", StorageType.CSV),
    #     thread_num=1
    # )

    parser = Rule(
        "2048游戏项目设计大纲",
        tag="div",
        attrs={"class": "markdown_views"},
        children=[
            Rule("一级标题", tag="h1", display={"text": False}, show=True, sep="|"),
            Rule("二级标题", tag="h2", display={"text": False}, show=True, sep="|"),
            Rule("三级标题", tag="h3", display={"text": False}, show=True, sep="|")
        ],
        show=False
    )
    spider.set_params(
        start_urls=["https://blog.csdn.net/weixin_46231858/article/details/129977507"],
        rule=parser,
        storage_func=Storage("./test.json", StorageType.JSON),
        thread_num=1
    )
    spider.start()
