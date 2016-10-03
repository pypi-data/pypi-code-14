# coding=utf-8


class TraverseFactory(object):
    """
    Фабрика построения путей. Принимает:
    :param context: ресурс-контекст
    :param view_name: имя функции представления
    :return: Возвращает функцию представления, если она удовлетворяет поступившему запросу или None, если по данному запросу функция не найдена

    EXAMPLE:

    app_resource_tree = {
        PostListResource: {'': post_list_view,},
        PostDetailResource: {'': post_detail_view,}
    }
    """
    app_resource_tree = {}

    def __init__(self, context, view_name):
        self.context = context
        self.view_name = view_name

    def traverse_factory(self):
        try:
            # "наследование" view, чтобы дочерние ресурсы получали все вьюшки родителей
            for resource_class in self.context.__class__.__mro__:
                if resource_class.__name__ in self.app_resource_tree:
                    if self.view_name in self.app_resource_tree[resource_class.__name__]:
                        return self.app_resource_tree[resource_class.__name__][self.view_name]
        except:
            # если дерево ресурсов будет оформленно неправильно, травёрсал просто вернёт 404)
            return None
