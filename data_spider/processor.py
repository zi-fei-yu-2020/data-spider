import re
from bs4 import BeautifulSoup


class Rule:
    def __init__(self, column_name: str, tag: str = None, attrs: dict = None, display=None, children: list = None):
        self.column_name = column_name
        if display is None:
            display = {"text": False}
        self.tag = tag
        self.attrs = attrs
        self.display = display
        self.children = children or []
        self.rule_dict = None

    def add_children(self, child_rules):
        for child_rule in child_rules:
            self.add_child(child_rule)

    def add_child(self, child_rule):
        if not isinstance(child_rule, Rule):
            raise TypeError("The child rule must be an instance of Rule class.")
        self.children.append(child_rule)

    def __str__(self):
        if not self.rule_dict:
            return "Object not established without calling the establish method"
        return str(self.rule_dict)

    def establish(self):
        self.rule_dict = {
            "tag": self.tag,
            "attrs": self.attrs,
            "children": [child_rule.establish() for child_rule in self.children]
        }
        for k, v in self.display.items():
            self.rule_dict[k] = v
        return self.rule_dict


class Processor:
    def __init__(self):
        pass

    def __get_data(self, item, rule):
        data = {}
        for k, v in rule.display.items():
            if v:
                data[rule.column_name] = item.get_text(strip=True)
        return data

    def __get_child_data(self, item, child_rule):
        column_name = child_rule.column_name
        tag = child_rule.tag
        attrs = child_rule.attrs or {}
        display = child_rule.display
        children = child_rule.children or []
        elements = item.find_all(tag, attrs=attrs)
        child_data = []
        if elements:
            for element in elements:
                try:
                    if children:
                        child_data.append(self.process(str(element), child_rule))
                    else:
                        child_data.append(element.get_text(strip=True))
                except Exception as e:
                    print(f"Error occurred while parsing tag {tag}: {e}")
            for k, v in display.items():
                if v:
                    return {column_name: child_data}
                else:
                    return child_data
        return None

    def process(self, html, rule: Rule):
        rule.establish()
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all(rule.tag, attrs=rule.attrs)
        result = []
        for item in items:
            data = self.__get_data(item, rule)
            for child_rule in rule.children:
                child_data = self.__get_child_data(item, child_rule)
                if child_data:
                    data.update(child_data)
            result.append(data)
        return result


if __name__ == '__main__':
    # rule = Rule(tag="div", attrs={"class": "item"})
    # child_rules1 = [
    #     Rule(tag="a", attrs={"class": "title"}),
    #     Rule(tag="span", attrs={"class": "rating_num"}, display=("text", False))
    # ]
    # rule.add_children(child_rules1)
    # quote_rule = Rule(tag="p", attrs={"class": "quote"})
    # quote_rule.add_child(Rule(tag="span", attrs={"class": "inq"}, display=("link", True)))
    # rule.add_child(quote_rule)
    #
    # # 将Rule转换成dict类型的规则
    # print(rule.establish())
    # print(rule)
    pass
