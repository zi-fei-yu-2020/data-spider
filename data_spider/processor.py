from bs4 import BeautifulSoup
from .utils import DataProcess
from .exceptions import RuleError


class Rule:
    def __init__(self, name: str, tag: str = None, attrs: dict = None, display=None, children: list = None,
                 show: bool = False, offset: int = 0, sep: str = None, exclude_method=None, process_method=None):
        self.name = name
        self.tag = tag
        self.attrs = attrs
        self.display = display or {"text": False}
        self.children = children or []
        self.show = show
        self.sep = sep
        self.exclude_method = exclude_method
        self.process_method = process_method
        self.rule_dict = None
        self.offset = offset

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
    def __init__(self, special_tags=None):
        self.special_tags = special_tags or []  # 暂时不做操作

    def __get_data(self, item, rule):
        data = {}
        for k, v in rule.display.items():
            if k == "text":
                data[rule.name] = item.text
            elif k == "string":
                data[rule.name] = item.string
            else:
                data[rule.name] = item.get(k)
            data[rule.name] = str(item.parent.contents[item.parent.index(item) + rule.offset])
            data[rule.name] = DataProcess.default_process(data.get(rule.name, None), rule.process_method)
            if not rule.show:
                data.pop(rule.name, None)
                break
            if DataProcess.default_exclude(data[rule.name], rule.exclude_method):
                data.pop(rule.name, None)
        return data

    def __get_child_data(self, item, child_rule):
        name = child_rule.name
        tag = child_rule.tag
        attrs = child_rule.attrs or {}
        display = child_rule.display
        children = child_rule.children or []
        elements = item.find_all(tag, attrs=attrs, **display)
        child_data = [self.process(str(element), child_rule) if children else
                      self.__get_data(element, child_rule).get(name, None) for element in elements]
        if child_data:
            return {name: child_rule.sep.join(child_data) if child_rule.sep else child_data}
        return None

    def process(self, html, rule: Rule):
        rule.establish()
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all(rule.tag, attrs=rule.attrs, **rule.display)
        result = []
        for item in items:
            data = self.__get_data(item, rule)
            if rule.show and DataProcess.default_exclude(data[rule.name], rule.exclude_method):
                data.pop(rule.name, None)
                continue
            for child_rule in rule.children:
                # print(item)
                child_data = self.__get_child_data(item, child_rule)
                # print(child_data)
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
