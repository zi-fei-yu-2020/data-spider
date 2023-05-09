from data_spider import Spider, StorageType, Storage, Rule


def yield_urls(url: str, pages: int):
    for i in range(pages):
        yield f"{url}/{i + 1}"


def process_url(data: str):
    data = data.replace("\t", "").replace("\\n", "")
    data = data.split(",")
    res = []
    for d in data:
        if ".webp" in d:
            d = d.split(" ")
            res.append(f"https://www.russfuss.com{d[0]}".replace("\n", ""))
    return res


def del_null(data: str):
    if not data or data == '':
        return True
    return False


def single_to_list(data: str):
    return [data]


if __name__ == '__main__':
    spider = Spider()
    # parser = Rule(
    #     "电影信息数据集",
    #     tag="div",
    #     attrs={
    #         "class": "el-card__body"
    #     },
    #     children=[
    #         Rule("电影名", tag="h2", attrs={"class": "m-b-sm"}, display={"text": False}, show=True),
    #         Rule("电影类型", tag="div", attrs={"class": "categories"}, display={"text": False}, show=True),
    #         Rule("影片信息", tag="div", attrs={"class": ["info", "m-v-sm"]}, display={"text": False}, show=True)
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

    # parser = Rule(
    #     "2048游戏项目设计大纲",
    #     tag="div",
    #     attrs={"class": "markdown_views"},
    #     children=[
    #         Rule("一级标题", tag="h1", display={"text": False}, show=True, sep="|"),
    #         Rule("二级标题", tag="h2", display={"text": False}, show=True, sep="|"),
    #         Rule("三级标题", tag="h3", display={"text": False}, show=True, sep="|")
    #     ],
    #     show=False
    # )
    # spider.set_params(
    #     start_urls=["https://blog.csdn.net/weixin_46231858/article/details/129977507"],
    #     rule=parser,
    #     storage_func=None,
    #     thread_num=1
    # )

    # parser = Rule(
    #     "纹理图片",
    #     tag="img",
    #     display={"srcset": True},
    #     show=True,
    #     process_method=process_url
    # )
    # spider.set_params(
    #     start_urls=["https://www.russfuss.com/"],
    #     rule=parser,
    #     thread_num=4
    # )

    # parser = Rule(
    #     "电影信息数据集",
    #     tag="div",
    #     attrs={
    #         "class": "el-card__body"
    #     },
    #     children=[
    #         Rule("电影名", tag="h2", attrs={"class": "m-b-sm"}, display={"text": False}, show=True),
    #         Rule("电影类型", tag="div", attrs={"class": "categories"}, display={"text": False}, show=True),
    #         Rule("电影封面", tag="img", attrs={"class": "cover"}, display={"src": True}, show=True)
    #     ]
    # )
    # spider.set_params(
    #     start_urls=["https://ssr1.scrape.center/"],
    #     rule=parser,
    #     thread_num=4
    # )

    parser = Rule(
        "知乎文章目录",
        tag="blockquote",
        attrs={
            "data-pid": "_WA9m1oo"
        },
        children=[
            Rule("目录", tag="br", display={"string": False}, show=True, offset=1),
        ],
        show=False
    )
    spider.set_params(
        start_urls=["https://zhuanlan.zhihu.com/p/109342493"],
        rule=parser,
        thread_num=1
    )
    spider.start()
    print(spider.get())
    # data = [[{'标题': '2048游戏项目计', '二级标题': '介绍|项目结构|技术栈|实现细节', '三级标题': 'Model类|GameView类|MessageBox类|Block类'}]]
    # print(spider.get(0,0,"以及标题", data=data, fuzzy=False))
    # spider.download_all("./test_img")
    # spider.download_single("https://www.russfuss.com/site/assets/files/1/widethumb-1.300x111.webp", "./nice.webp")
    # spider.download_csv("./default.csv", "./test_csv", 2, 1)
