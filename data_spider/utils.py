import random


class UserAgentPool:
    """
    User-Agent池

    根据平台分3类，每类有若干知名的浏览器UA类型，category参数对应3类平台，browser对应若干浏览器类型

    - pc：电脑端      chrome|firefox|ie
    - mobile：手机端  chrome|firefox|safari
    - tablet：平板端  chrome|firefox|safari
    """

    def __init__(self):
        self.__user_agents = {
            'pc': {
                'chrome': [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
                    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
                ],
                'firefox': [
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
                ],
                'ie': [
                    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
                    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                ],
            },
            'mobile': {
                'chrome': [
                    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36',
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.163 Mobile/15E148 Safari/604.1',
                    'Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/11.2 Chrome/75.0.3770.143 Mobile Safari/537.36',
                    'Mozilla/5.0 (Linux; Android 9; Pixel 3a XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.143 Mobile Safari/537.36',
                ],
                'firefox': [
                    'Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
                    'Mozilla/5.0 (Android 9; Mobile; rv:79.0) Gecko/79.0 Firefox/79.0',
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.1 Mobile/15E148 Safari/605.1.15',
                ],
                'safari': [
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                    'Mozilla/5.0 (iPad; CPU OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                ],
            },
            'tablet': {
                'chrome': [
                    'Mozilla/5.0 (Linux; Android 10; SM-T500) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36',
                    'Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.163 Mobile/15E148 Safari/604.1',
                ],
                'firefox': [
                    'Mozilla/5.0 (Android 10; Tablet; rv:68.0) Gecko/68.0 Firefox/68.0',
                    'Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
                ],
                'safari': [
                    'Mozilla/5.0 (iPad; CPU OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
                    'Mozilla/5.0 (iPad; CPU OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                ],
            },
        }
        self.__ua_list = []
        self.__ua_category_list = []

    def add_user_agent(self, category: str, browser: str, ua: str):
        self.__user_agents[category][browser].append(ua)

    def remove_user_agent(self, category: str, browser: str, ua: str):
        try:
            self.__user_agents[category][browser].remove(ua)
        except ValueError:
            print(f"{ua} not found in the pool for {category} {browser}.")

    def get_random_user_agent(self, category: str = None, browser: str = None):
        if category is None:
            category = random.choice(list(self.__user_agents.keys()))
        if browser is None:
            browser = random.choice(list(self.__user_agents[category].keys()))
        return random.choice(self.__user_agents[category][browser])

    def get_user_agent(self, category: str, browser: str):
        return random.choice(self.__user_agents[category][browser])

    def __str__(self):
        return str(self.__user_agents)


class DataProcess:
    @staticmethod
    def sub(data: str):
        data = data.replace(" ", "").replace("\n", "").replace(" ", "")
        return data

    @staticmethod
    def del_null(data: str):
        if not data or data == '':
            return True
        return False

