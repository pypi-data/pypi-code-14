# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
import importlib
from django.conf import settings


class ResourceRegistrator(object):
    """
    Класс-синглтон, содержит информацию о каждом ресурсе в системе. Служит для связи имени класса ресурса с его экземпляром
    """

    def __init__(self):
        self._registry = {}  # resource_class_name -> resource_class_instance
        # подгружаем файлы resources из всех приложений, там где нет такого файла, или он не правильный - просто не подгружаем
        # for app_name in settings.INSTALLED_APPS:
        #     try:
        #         module = importlib.import_module(".".join([app_name, "resources"]))
        #         print module
        #     except:
        #         pass

    def register(self, resource_class):
        if resource_class.__name__ in self._registry:
            raise Exception(u'Ресурс %s уже зарегистрирован ' % resource_class.__name__)
        self._registry[resource_class.__name__] = resource_class

    def unregister(self, resource_class_name):
        if resource_class_name not in self._registry:
            raise Exception(u'Ресурс %s не был зарегистрирован ' % resource_class_name)
        self._registry.pop(resource_class_name)

    def get_all_res_class_names(self):
        """
        :return: возвращает список имён всех зарегистрированных ресурсов
        """
        return self._registry.keys()

    def get_res_class_by_name(self, class_name):
        if class_name in self._registry:
            return self._registry[class_name]
        return None

    def get_root_resource(self):
        """
        :return: возвращает корень иерархии ресурсов
        """
        return settings.ROOT.split('.')[-1]


resource_registrator = ResourceRegistrator()


class Resource(object):
    """
    Каждый ресурс знает:
    __slug__ - как его зовут
    __parent__ - своего родителя
    children - список всех возможных классов своих детей
    request - имеет доступ к HTTP запросу
    source - имеет основное содержание, формируемое ещё на этапе маршрутизации, посредством метода get_source
    т.к. зачастую путь формируется исходя из возможности сформировать путь.
    В большинстве случаев get_source содержит запрос к БД
    parents - сущнность, для взаимодействия с родителями рессурса
    brothers - рессурс может иметь братьев, т.е. список экземпляров того же класса, связанных с данным рессурсом
    математической операцией ИЛИ, обозначаются в URL как resource+resource


    Продуктом работы ресурса является контекст, который он добавляет к view

    В идеале у ресурсов есть права доступа (ALE) ?ACL
    Несомненно, работа с правами доступа требует повышенного контроля, а значит унификации,
    и в будующем этот вопрос нужно решать, но я ещё не решил, как это сделать лучше всего.
    Однако по сути права доступа - это контекст, а методов для работы с контекстом в классе более чем достаточно

    Алгоритм действия ресурсов:
    1) Роутер передаёт управление корневому ресурсу, он имеет информацию о всех классах cвоих прямых потомков через children
    2) Рессурс добавляет в контекст свою логику (из get_source)
    3) Роутер пытается вызвать дочерний элемент с новым контекстом если у него получается, то повторяются пунты 2,3, иначе
    4) Роутер ищет view с именем ключа
    5) если получается, передаёт управление в view с полученным контекстом, и оставшимися в vpath_list параметрами, иначе обрабатывает исключение 404

    URL всегда соответствует Resource + View + [view_params]

    mixin - добавляет атрибуты и методы в класс

    """

    group = 'nogroup' # группа, в которой состоит рессурс. Нужна например для организации нескольких иерархий хлебных крошек

    source = None  # Основное содержимое ресурса

    children = []  # ресурсы-потомки данного класса

    # Является ли ресурс иерархическим
    # если является, то у него может быть hiererchy_parent_slug - указатель на имя ресурса родителя
    # Если hiererchy_parent_slug не определён, то данный ресурс - вершина иерархии
    hierarchy = False
    hierarchy_parent_slug = None

    def __init__(self, slug, parent=None, request=None):
        self.__slug__ = slug
        self.__parent__ = parent
        self.request = request
        # self.children = self.children_factory()
        self.parents = self.Parents(self)
        self.brothers = [self, ]
        self.full_list = self.__get_full_list()
        self.list = self.full_list
        # self.debug("init %s" % self.__class__.__name__)
        self.source = self.get_source()
        self.brothers_source = self.source

    """
    Абстрактный интерфейс для работы с контекстом
    для взаимодействия с интерфейсом объект должен содержать следующие атрибуты
    list - модифицируемый интерфейсом список рессурсов
    full_list - полный список рессурсов (без фильтрации) для заданного рессурса
    """

    @staticmethod
    def base_all(obj):
        obj.list = obj.full_list
        return obj

    @staticmethod
    def get_classes_for_names(filtered_classes_names):
        """
        Поинимает список имён классов ресурсов
        :return: Возвращает список классов ресурсов
        """
        filtered_classes = []
        for filtered_classes_name in filtered_classes_names:
            filtered_classes.append(resource_registrator.get_res_class_by_name(filtered_classes_name))

        return filtered_classes

    @staticmethod
    def base_filter(obj, filtered_classes_names):
        filtered_classes = obj.get_classes_for_names(filtered_classes_names)

        obj.list = []
        for parent in obj.full_list:
            for filtered_class in filtered_classes:
                if isinstance(parent, filtered_class):
                    obj.list.append(parent)

        return obj

    @staticmethod
    def base_exclude(obj, excluded_classes_names):
        excluded_classes = obj.get_classes_for_names(excluded_classes_names)

        obj.list = []
        for parent in obj.full_list:
            add = True
            for excluded_class in excluded_classes:
                if isinstance(parent, excluded_class):
                    add = False
            if add:
                obj.list.append(parent)
        return obj

    @staticmethod
    def base_group_filter(obj, group='nogroup'):
        """
        метод для фильтации по группам рессурсов (например география)
        по умолчанию без параметров выдаст все рессурсы без группы
        """
        obj.list = []
        for parent in obj.full_list:
            if parent.group == group:
                obj.list.append(parent)

        return obj

    @staticmethod
    def base_group_exclude(obj, group='nogroup'):
        """
        Метод сформирует список всех ресурсов не входящих в группу в его аргументе
        По умолчанию, без аргумента, вернёт все ресурсы с входящие в какую-либо группу (не считая nogroup)
        """
        obj.list = []
        for index, parent in enumerate(obj.full_list):
            if parent.group != group:
                obj.list.append(parent)
        return obj

    @staticmethod
    def base_get_all(obj, attr_name):
        """Возвращает все реализации члена или метода среди ресурсов-родителей по заданному имени атрибута
           Например: get_all('get_title') - вернёт список методов get_title ресурсов родителей, начиная от прямого потомка
        """
        attr_list = []
        for parent in obj.list:
            if attr_name in dir(parent):
                attr_list.append(getattr(parent, attr_name))

        return attr_list

    @staticmethod
    def base_get_and_call_all(obj, attr_name):
        """
        Похож на предыдущий метод, только вызывает каждый из списка возвращаемых методов
        :param attr_name:  имя возвращаемого метода
        :return: список результатов возвращаемых каждым из методов
        """
        attr_list = []
        for parent in obj.list:
            if attr_name in dir(parent):
                attr_list.append(getattr(parent, attr_name)())

        return attr_list

    @staticmethod
    def base_get_first(obj, attr_name):
        """Возвращает первую реализацию метода или члена среди родителей
           Фактически это эквивалент запроса ребёнка: Родители, дайте мне машинку,
           при этом запрос выполнит первый, кто сможет это сделать
           в случае, если никто из родителей не имеет искомого атрибута, вернёт None
        """
        for parent in obj.list:
            if attr_name in dir(parent):
                return getattr(parent, attr_name)
        return None

    @staticmethod
    def base_get_last(obj, attr_name):
        """Возвращает последнюю реализацию метода или члена среди родителей"""
        for parent in reversed(obj.list):
            if attr_name in dir(parent):
                return getattr(parent, attr_name)
        return None

    """
    Интерфейс для работы с контекстом в контексте рессурса
    """

    def __get_full_list(self):
        list = [self, ]
        list += self.parents.get_parents_list(self)
        return list

    def all(self):
        return self.base_all(self)

    def filter(self, filtered_classes_names):
        return self.base_filter(self, filtered_classes_names)

    def exclude(self, excluded_classes_names):
        return self.base_exclude(self, excluded_classes_names)

    def group_filter(self, group='nogroup'):
        return self.base_group_filter(self, group)

    def group_exclude(self, group='nogroup'):
        return self.base_group_exclude(self, group)

    def get_all(self, attr_name):
        return self.base_get_all(self, attr_name)

    def get_and_call_all(self, attr_name):
        return self.base_get_and_call_all(self, attr_name)

    def get_first(self, attr_name):
        return self.base_get_first(self, attr_name)

    def get_last(self, attr_name):
        return self.base_get_last(self, attr_name)

    """
    Группа методов для работы с братскими рессурсами
    """

    def get_brothers_all(self, attr_name):
        """
        Метод возвращает список значений аттрибута для каждого из братьев-рессурсов,
        ВАЖНО, у каждого брата должен быть данный атрибут
        :param attr_name: имя вызываемого метода или члена класса брата-рессурса
        :return:
        """
        attr_list = []
        for brother in self.brothers:
            attr_list.append(getattr(brother,attr_name))
        return attr_list

    def get_and_call_brothers_all(self, attr_name):
        """
        Очень похож на предыдущий метод, с той лишь разницей, что вызывает каждый из полученных методов
        :param attr_name: имя вызываемого метода
        :return:
        """
        attr_list = self.get_brothers_all(attr_name)
        attr_called_list = []
        for attr in attr_list:
            attr_called_list.append(attr())
        return attr_called_list

    def get_brothers_title(self):
        """Примитивный метод, демонстрирует взаимодействие с братскими ресурсами,
        ну и выдаёт перечень title братьев через запятую"""
        return ', '.join(self.get_and_call_brothers_all('get_title'))

    def is_have_brothers(self):
        """Флаг, возвращает истину, если у рессурса есть братья, и ложь, если нет"""
        if len(self.brothers) > 1:
            return True
        else:
            return False

    def get_brothers_source(self):
        """Возвращает queryset совместных данных рессурсов одного уровня (братьев)
        ПЕРЕОПРЕДЕЛИ МЕНЯ если необходима поддержка операции ИЛИ (+) """
        return self.get_source()

    def __get_partical_source(self):
        """Возвращает часть выражения source предназначенную для обработки методом get_brother's source
        Вызывается в методе get_source, для поддержки  операции ИЛИ в рессурсах (+)
        ПЕРЕОПРЕДЕЛИ МЕНЯ В СВОЁМ РЕСУРСЕ, если требуется функционал составных рессурсов (+)"""
        return None

    def get_brothers_slugs(self, without=None):
        """
        Метод возвращает часть иерархие URL для текущего ресурса
        если братьев у ресурса нет, возвращает __slug__
        иначе возвращает сумму slug всех братьев:
        slug1+slug2+slug3
        """
        # учитываем братьев в URL
        if self.is_have_brothers():
            slugs = self.get_brothers_all('__slug__')
            if without and without in slugs:
                slugs.remove(without)
            return '+'.join(slugs)
        else:
            if without:
                return ''
            return self.__slug__

    class Parents():
        def __init__(self, context):
            self.context = context
            self.full_list = self.get_parents_list(self.context)
            self.list = self.full_list

        @staticmethod
        def get_parents_list(context):
            parents_list = []
            while context.__parent__:
                # учитываем братьев рессурса
                for brother in context.__parent__.brothers:
                    parents_list.append(brother)
                context = context.__parent__
            return parents_list

        """
        Интерфейс для работы с контекстом в контексте родителей рессурса
        """

        def all(self):
            return self.context.base_all(self)

        def filter(self, filtered_classes_names):
            return self.context.base_filter(self, filtered_classes_names)

        def exclude(self, excluded_classes_names):
            return self.context.base_exclude(self, excluded_classes_names)

        def group_filter(self, group='nogroup'):
            return self.context.base_group_filter(self, group)

        def group_exclude(self, group='nogroup'):
            return self.context.base_group_exclude(self, group)

        def get_all(self, attr_name):
            return self.context.base_get_all(self, attr_name)

        def get_and_call_all(self, attr_name):
            return self.context.base_get_and_call_all(self, attr_name)

        def get_first(self, attr_name):
            return self.context.base_get_first(self, attr_name)

        def get_last(self, attr_name):
            return self.context.base_get_last(self, attr_name)

    def get_parent(self):
        """
        :return: Возвращает ресурс родитель (в основном для использования в шаблонах, где нельзя применять "__")
        """
        return self.__parent__

    def get_title(self):
        """
        :return: Возвращает заголовок ресурса для поиска, желательно переопределить в своих ресурсах, иначе выводится slug
        """
        return self.__slug__

    def get_source(self):
        """Переопределите метод get_source в своём ресурсе

        :type self: object
        :param parent: класс родитель передаёт свой экземпляр для досутпа к своим source и __parent__
        :param key: имя будущего ресурса
        :return: возвращает source в случае если с данным контекстом, по данному ключу есть результат иначе исключение
        """

        return None

    def get_slug(self):
        return self.__slug__

    """
    Группа методов для работы с URL
    """

    class MetaResource(object):
        """
        Облегчённая версия ресурса, для генерации URL
        """
        __parent__ = None

        def __init__(self, slugs, class_name, hierarchy=False, hierarchy_parent_slug=None):
            self.slugs = slugs           # Список братьев ресурса
            self.class_name = class_name # Имя класса ресурса, мета-копию которого мы делаем
            ResourceClass = resource_registrator.get_res_class_by_name(class_name)
            self.children = ResourceClass.children     # Список имён детей ресурса, мета-копию которого мы делаем
            self.hierarchy = hierarchy   # Флаг, является ли ресурс иерархическим, по умолчанию отключен
            self.hierarchy_parent_slug = hierarchy_parent_slug # slug прямого родителя по иерархии

        def __str__(self):
            return "<Meta %s>" % self.class_name

        def get_brothers_slugs(self):
            return '+'.join(self.slugs)

        def _get_traversal_url(self):
            """
            Метод для внутреннего использования
            :param self: принимает ресурс
            :return: возвращает часть URL, сгенерированную непосредственно django_traversal (без корня)
            """
            path_list = []
            while self:
                path_list.append(self.get_brothers_slugs())
                self = self.__parent__

            #удаляем пустой корень
            del path_list[-1]

            vpath_tuple = reversed(path_list)
            traversal_url = '/'.join(vpath_tuple)
            return traversal_url

        def get_absolute_url(self):
            """
            Дублируем функционал аналогичного метода в классе Resource
            Не DRY конечно, но память мы порядком экономим на этом
            С радостью уберу дублирование, если найдётся способ сделать это лучше
            Как идея - вынести в мета класс, и наследовать от него и класс Resource и MetaContext
            """
            # TODO рефакторинг, вынести общие методы и члены в общий класс-родитель
            traversal_url = self._get_traversal_url()
            url_root = reverse('router_root')
            absolute_url = url_root + traversal_url
            return absolute_url

    def _get_traversal_url(self):
        """
        Метод для внутреннего использования
        :param self: принимает ресурс
        :return: возвращает часть URL, сгенерированную непосредственно django_traversal (без корня)
        """
        path_list = []
        while self:
            path_list.append(self.get_brothers_slugs())
            self = self.__parent__

        #удаляем пустой корень
        del path_list[-1]

        vpath_tuple = reversed(path_list)
        traversal_url = '/'.join(vpath_tuple)
        return traversal_url

    def __breadcrumbs_append(self, current_url, breadcrumbs_list):
        """
        Добавляет значение в список
        :return: Возвращает
        """
        # проверяем, есть ли у текущего рессурса братья
        if self.is_have_brothers():
            left_url_part, right_url_part = self.__get_left_and_right_url_part(current_url)
            brothers_slugs = self.get_brothers_all('__slug__')
            brothers_titles = self.get_and_call_brothers_all('get_title')
            brothers_meta = []
            for i, slug in enumerate(brothers_slugs):
                brothers_meta.append((slug, brothers_titles[i]))
            breadcrumbs_list.append((current_url, self.get_brothers_title(), left_url_part, right_url_part, brothers_meta))
        else:
            breadcrumbs_list.append((current_url, self.get_title()))

        return breadcrumbs_list

    @staticmethod
    def __cut_one_part_from_right(url, url_part):
        """
        Метод убирает из строки URL первое справа вхождение url_part
        """
        pos = url.rfind('/'+url_part)
        length = len(url_part) + 1
        url = url[:pos] + url[pos + length:]
        return url

    @staticmethod
    def __replace_one_part_from_right(url, old_part, new_part):
        """
        Метод заменяет в строке URL первое справа вхождение old_part на new_part
        """
        pos = url.rfind('/' + old_part)
        length = len(old_part) + 1
        url = ''.join((url[:pos], '/', new_part, url[pos + length:]))
        return url

    @staticmethod
    def __cut_url_from_right(url):
        """Метод обрезает URL вплоть до ближайшего справа разделителя, если разделителей нет - вернёт пустую строку
        Нужен для оптимизации, чтобы десять раз не парсить один и тот-же стек рессурсов
        :param url: строка url
        :return: Возвращает
        """
        # удаляем правую часть текущего URL до разделителя
        if url.count('/') > 1:
            return url.rsplit('/', 1)[0]
        else:
            return '/'

    def __get_left_and_right_url_part(self, current_url):
        context_url = self.get_absolute_url()
        right_url_part = current_url.replace(context_url, '')
        left_url_part = self.__cut_url_from_right(context_url)
        if left_url_part == '/':
            left_url_part = ''
        return left_url_part, right_url_part

    def add_hierarchy_child(self, res_classes_names, res_slugs):
        context = self
        right_part = []
        while context:
            if context.__class__.__name__ in res_classes_names:
                for brother in context.brothers:
                    if brother.__slug__ in res_slugs:
                        if brother.hierarchy and right_part:
                            hierarchy_slugs = [brother.__slug__, ]
                            for res in reversed(right_part):
                                for res_brother in res.brothers:
                                    if res_brother.hierarchy_parent_slug in hierarchy_slugs:
                                        res_classes_names.append(res_brother.__class__.__name__)
                                        res_slugs.append(res_brother.__slug__)
                                        hierarchy_slugs.append(res_brother.__slug__)

            right_part.append(context)
            context = context.__parent__

        return res_classes_names, res_slugs

    @staticmethod
    def split_to_syntagmas(str, separators=['/', '+']):
        """
        Метод разбивает строку, в частности URL на список синтагм
        OPTINIZEME Этот метод - хороший кондидат на оптимизацию)))
        :param str: строка, которую будем разбивать
        :param separators: список разделителей, по которым будем разбивать (тоже являются синтагмами и записываются в результат)
        :return: список синтагм
        """
        syntagmas = []
        word = ''
        for litera in str:
            if litera in separators:
                if word:
                    syntagmas.append(word)
                syntagmas.append(litera)
                word = ''
            else:
                word += litera
        if word:
            syntagmas.append(word)
        return syntagmas

    @staticmethod
    def sub_list(list1, list2):
        """
        Метод вычитает из первого листа все элементы второго, возвращает лист-результат
        """
        for item in list1:
            if item in list2:
                list1.remove(item)

        return list1

    @staticmethod
    def clean_url(url):
        """
        Очищает URL от лишних служебных символов // ++ /+ +/ +$
        """
        url = url.replace('++++', '+')
        url = url.replace('+++', '+')
        url = url.replace('++', '+')
        url = url.replace('/+', '/')
        url = url.replace('+/', '/')
        url = url.replace('////', '/')
        url = url.replace('///', '/')
        url = url.replace('//', '/')
        if url[-1] == '+':
            url = url[0:-1]

        return url

    def sub(self, res_slugs):
        """
        Метод вычитает из текущего URL искомый контекст, возвращает url без данного контекста
        по контексту проходим справа на лево
        новая реализация
        """
        # Берём строку URL
        url = self.get_absolute_url()
        # Разделяем её на синтагмы
        syntagmas = self.split_to_syntagmas(url)
        # Удаляем из строки искомые slugs
        syntagmas = self.sub_list(syntagmas, res_slugs)
        # Формируем новый URL
        url = ''.join(syntagmas)
        # Удаляем лишние служебные символы
        url = self.clean_url(url)

        return url

    def sub_all(self, res_classes_names):
        """
        Метод убирает из URL все экземпляры классов, перечисленные в res_classes_names
        :param res_classes_names: список имён экземпляров классов
        :return: возвращает URL без указанных классов
        """

        # Пройдёмся по контексту, исключая из URL лишние классы
        context = self
        url = self.get_absolute_url()
        while context:
            if context.__class__.__name__ in res_classes_names:
                url_part = context.get_brothers_slugs()
                url = self.__cut_one_part_from_right(url, url_part)
            context = context.__parent__
        if not url:
            url = '/'
        return url

    def sub_group(self, group='nogroup'):
        """
        Метод вычитает из текущего URL все ресурсы заданной группы.
        Следует использовать только в том случае, когда можно без повреждения логики приложения убрать всю группу из URL
        :param group: член класса ресурса
        :return: возвращает URL без ссылок на ресурсы
        """
        url = self.get_absolute_url()
        context = self
        while context:
            if context.group == group:
                url = context.sub_context(url)
            context = context.__parent__
        return url

    def sub_context(self, url):
        """
        Метод вычитает из переданного в аргументе url текущий контекст
        :return: возвращает URL
        """
        left_part, right_part = self.__get_left_and_right_url_part(url)
        return left_part + right_part

    def sub_res_classes(self, res_classes_names, meta_context):
        """
        Убирает из мета-контекста все ресурсы заданных классов
        :param res_classes_names: имена классов ресурсов, которые убираем из контекста
        :param meta_context: экземпляр мета-контекста
        :return возвращает мета-контекст
        """
        final_context = meta_context # Итоговая метка на ресурс, который возвращаем в другие методы
        child = None

        while meta_context:
            if meta_context.class_name in res_classes_names:
                # убираем ресурс
                if child:
                    child.__parent__ = meta_context.__parent__
                else:
                    final_context = meta_context.__parent__
                meta_context = meta_context.__parent__
                continue
            child = meta_context
            meta_context = meta_context.__parent__

        return final_context

    def replace_all(self, res_class_name_or_array, no_replace_res_class_name_or_array, res_slug_or_slugs):
        """
        Заменяет ресурсы всех классов, на указанные в res_class_name_or_array на значения, указанные в res_slug_or_slugs за исключением ресурсов, указанных в no_replace_res_class_name_or_array
        :param res_class_name_or_array:
        :param no_replace_res_class_name_or_array:
        :param res_slug_or_slugs:
        :return:
        """

        # список всех ресурсов
        all_res_class_names = resource_registrator.get_all_res_class_names()

        # удаляем из списка всех ресурсов те, что находятся в списках res_class_names и no_replace_res_class_names и корневой ресурс!!!
        res_class_names = [res_class_name for res_class_name in all_res_class_names if not (res_class_name in res_class_name_or_array or res_class_name in no_replace_res_class_name_or_array or (res_class_name == resource_registrator.get_root_resource()))]

        # добавляем в начало списка ресурсы из res_class_names
        res_class_name_or_array.extend(res_class_names)

        # заменяем посредством стандартного replace
        return self.replace(res_class_name_or_array, res_slug_or_slugs)

    def replace(self, res_class_name_or_array, res_slug_or_slugs):
        """
        Заменяет если уже есть или добавляет ресурсы в URL из списка res_classes_names с значениями res_slugs
        :param res_classes_names:
        :param res_slugs:
        :return: возвращает URL
        """
        res_classes_names = self.__convert_res_class_to_array(res_class_name_or_array, len(res_slug_or_slugs))
        res_slugs = self.__convert_slugs_to_str(res_slug_or_slugs)
        current_context = self.__make_meta_res()  # Текущий контекст, метка, указывающая на тот ресурс, с которым мы работаем в данный момент времени.

        # Удаляем из мета-контекста все ресурсы заданных классов
        current_context = self.sub_res_classes(res_classes_names, current_context)

        # Добавляем в мета-контекст новые ресурсы, и возвращаем полученный URL
        return self.add(res_classes_names, res_slugs, current_context=current_context)

    def __make_meta_res(self):
        # Создаём мета-ресурс по текущему контексту (self), чтобы потом безпрепятственно его модифицировать
        context = self
        child = None
        meta_context = None
        final_meta_context = None
        while context:
            if context.hierarchy:
                new_meta_context = self.MetaResource(context.get_brothers_all('__slug__'), context.__class__.__name__, context.hierarchy, context.hierarchy_parent_slug)
            else:
                new_meta_context = self.MetaResource(context.get_brothers_all('__slug__'), context.__class__.__name__)
            if child:
                meta_context.__parent__ = new_meta_context
            else:
                final_meta_context = new_meta_context

            meta_context = new_meta_context
            child = context
            context = context.__parent__

        return final_meta_context

    def __make_added(self, res_class_name_or_array, res_slug_or_slugs):
        """
        Метод создаёт мета-контекст, который мы будем вставлять в наш текущий контекст для формирования url перехода на другие страницы
        :param res_class_name_or_array:
        :param res_slug_or_slugs:
        :return: экземпляр MetaResource -
        """
        res_slugs_array = self.__convert_slug_to_array(res_slug_or_slugs)
        res_classes_names = self.__convert_res_class_to_array(res_class_name_or_array, len(res_slugs_array))
        iter_res_classes_names = iter(res_classes_names)

        added_ress = [] # список вставляемых ресурсов
        for res_slug in res_slugs_array:
            added_ress.append(self.MetaResource([res_slug,], iter_res_classes_names.next()))

        # Для первого ресурса из списка добавляемых вставляем информацию об иерархии
        added_ress[0].hierarchy = resource_registrator.get_res_class_by_name(added_ress[0].class_name).hierarchy
        return added_ress

    def add(self, res_class_name_or_array, res_slug_or_slugs, current_context=None, hierarchy_parent_slug=None):
        """
        TODO желательно провести декомпозицию метода на несколько простых
        Добавляет в URL контекст, заданныйх в res_class_name_or_array классов с заданными в res_slug_or_slugs именами.
        Каждому классу из res_class_name_or_array обязательно должно соответствовать имя из res_class_name_or_array
        :param res_class_name_or_array:
        :param res_slug_or_slugs:
        :return: возвращает URL
        """

        added_ress = self.__make_added(res_class_name_or_array, res_slug_or_slugs)
        # В виду сложности модификации взаимодействие проводится с мета-контекстом
        # Возможно в дальнейшем имеет смысл переписать с мета-контекстом методы replace, sub, sub_all

        if not current_context:
            current_context = self.__make_meta_res()  # Текущий контекст, метка, указывающая на тот ресурс, с которым мы работаем в данный момент времени.
        right_context = []  # Пройденная часть контекста

        while current_context:
            # Если первый из внедряемых ресурсов может быть потомком текущего
            if added_ress[0].class_name in current_context.children:
                # Флаг, поднимающийся при прохождении валидации на иерархию или её отсутствие
                hierarchy_valid = False
                # Если внедряемый ресурс - иерархический
                if hierarchy_parent_slug:
                    # Проверим, соответствует ли его иерархический родитель текущему, или его братьям
                    if hierarchy_parent_slug in current_context.slugs:
                        hierarchy_valid = True
                elif hierarchy_parent_slug == '':
                    # Если первый внедряемый ресурс - вершина иерархии проверим принадлежит ли текущий контекст к этой иерархии
                    if added_ress[0].hierarchy != current_context.hierarchy:
                        # Если ресурсы принадлежат к разным иерархиям, можно внедрять
                        hierarchy_valid = True
                else:
                    hierarchy_valid = True

                if hierarchy_valid:
                    # Если у текущего ресурса есть ребёнок
                    posible = False
                    if right_context:
                        # проверим одного ли класса с ребёнком следующий ресурс, и можно ли добавить его братом
                        # переворачиваем список ресурсов правой части контекста и создаём из него итератор
                        iter_right_context = reversed(right_context)
                        # создаём итераторы из списков
                        iter_added_ress = iter(added_ress)
                        for added_res in iter_added_ress:
                            # Передвигаем current_context
                            try:
                                current_context = iter_right_context.next()
                            except:
                                # 4-ая ветка алгоритма
                                # Если элементы кончились, вероятно надо просто добавить в конец оставшееся
                                # add_here
                                while iter_added_ress:
                                    added_res.__parent__ = current_context
                                    current_context = added_res
                                    try:
                                        added_res = iter_added_ress.next()
                                    except:
                                        return current_context.get_absolute_url()

                            if added_res.class_name == current_context.class_name:
                                # 1-ая ветка алгоритма
                                # Проверяем есть ли ресурс с таким slugs в контексте, если нет - добавляем
                                if not added_res.slugs[0] in current_context.slugs:
                                    current_context.slugs.append(added_res.slugs[0])
                            else:
                                # Если не можем больше добавить ресурсы к существующим
                                # Проверем можно ли поместить их между существующими частями контекста
                                if current_context.class_name in added_ress[-1].children:
                                    # 2-ая ветка алгортима
                                    # вставляем оставшийся контекст перед текущим
                                    parent = current_context.__parent__
                                    while iter_added_ress:
                                        added_res.__parent__ = parent
                                        parent = added_res
                                        try:
                                            added_res = iter_added_ress.next()
                                        except:
                                            break

                                    current_context.__parent__ = added_res
                                    # Перемещаем курсор к младшему из ресурсов контекст
                                    try:
                                        current_context = right_context[0]
                                    # в случае ошибки - мы уже на младшем, ничего делать не нужно
                                    except:
                                        pass
                                    return current_context.get_absolute_url()

                                else:
                                    # Если поместить между существующими ресурсами вставляемый контекст нельзя - то это ошибка, вызовем исключение
                                    raise Exception(u'Не удаётся вставить в контекст классы, начиная с %s' % added_res.class_name)
                        # Если мы вышли из цикла значит внедрение возможно

                    else:
                        # 5-ая ветка алгортима
                        # Мы можем внедрить контекст после существующего
                        for added_res in added_ress:
                            added_res.__parent__ = current_context
                            current_context = added_res
                        return current_context.get_absolute_url()

                    # 3-я ветка алгоритма
                    # Если не попали на внедрение, вероятно мы прошли цикл до конца, значит все части контекста уже вставлены
                    # нужно поместить метку текущего контекста на последний ресурс и вернуть текущий URL

                    if right_context:
                        current_context = right_context[0]
                    return current_context.get_absolute_url()

            right_context.append(current_context)
            current_context = current_context.__parent__

        # Если прошли весь контекс - и не нашли места, куда можно вставить добавляемые ресурсы - выдаём исключение
        raise Exception(u'Не удалось добавить в контекст %s' % added_ress)

    def __convert_slugs_to_str(self, string_or_array):
        """
        Конвертирует массив slugs в готовую к внедрению строку
        """
        # На случай если пришли не строки, а например int, преобразуем всё в строки
        string_or_array = map(unicode, string_or_array)

        if (isinstance(string_or_array, basestring)):
            string = string_or_array
        else:
            string = '/'.join(string_or_array)

        return string

    def __convert_slug_to_array(self, slug_or_array):
        """
        Метод принимает единичный слаг или массив и всегда возвращает массив
        :param slug_or_array: строка слаг или массив строк слаг
        :return: массив слаг
        """
        if (isinstance(slug_or_array, basestring)):
            return [slug_or_array, ]
        else:
            return slug_or_array

    def __convert_res_class_to_array(self, res_class_name_or_array, slugs_count):
        """
        Конвертирует класс ресурса в массив
        Метод примечателен тем, что не просто собирает массив, а проверяет его валидность. Могут ли элементы стоять в такой последовательности,
        и что важно для метода replace - валидность проверяется только для той части списка классов, которой соответствуют элементы slugs, для прочих валидность не проверяется
        это достигается за счёт введения параметра slugs_count
        Иначе выдаст исключение
        :param res_class_name_or_array: имя класса рессурса или массив имён классов ресурсов
        :param slugs_count: количество вставляемых элементов - соответствует классам в массиве классов
        :return: возвращает массив имён классов ресурсов
        """
        # Проверяем что нам пришло массив или одно имя ресурса если пришла строка, то преобразуем её в массив
        if isinstance(res_class_name_or_array, basestring):
            res_classes_names = [res_class_name_or_array, ]
        else:
            # иначе сделаем проверочку, могут ли данные элементы стоять друг за другом
            res_classes_names = res_class_name_or_array
            Parent = None
            for index, resource_name in enumerate(res_classes_names):
                if index < slugs_count:
                    if not Parent or resource_name in Parent.children:
                        Parent = resource_registrator.get_res_class_by_name(resource_name)
                    else:
                        raise Exception(u'Ресурс %s не может быть дочерним элементом %s' % (resource_name, Parent.__name__))

        return res_classes_names

    def insert_context(self, res_classes_names, res_slugs):

        context = self
        child = None
        while context:
            # Если первый из внедряемых ресурсов может быть потомком текущего
            if res_classes_names[0] in context.children:
                # Если у текущего ресурса есть ребёнок
                posible = False
                if child:
                    # Проверем, может ли внедряемый контекст стоять между ресурсами родителем и ребёнком
                    context_class = resource_registrator.get_res_class_by_name(res_classes_names[-1])
                    if child.__class__.__name__ in context_class.children:
                        posible = True
                else:
                    posible = True
                # Если внедрение возможно
                if posible:
                    # Получаем URL текущего контекста
                    curent_url = context.get_absolute_url()
                    # Получаем правую часть URL
                    left_url_part, right_url_part = self.__get_left_and_right_url_part(curent_url)

                    return curent_url + res_slugs + right_url_part

    def get_breadcrumbs(self):
        """
        :return: возвращает список ссылок на всех родителей данного ресурса в формате (url,заголовок, [url-родителя рессурса, [список рессурсов-братьев] ])
        """
        breadcrumbs_list = []
        context = self

        if self.list == self.full_list:
            current_url = self.get_absolute_url()
            while context:
                breadcrumbs_list = context.__breadcrumbs_append(current_url, breadcrumbs_list)
                current_url = self.__cut_url_from_right(current_url)
                context = context.__parent__
        else:
            # если применяем фильтрацию по классам, то экономичный алгоритм создания крошек уже не актуален,
            # создаём их индивидуально для каждого члена списка list:
            current_url = context.get_absolute_url()
            while context:
                if context in self.list:
                    breadcrumbs_list = context.__breadcrumbs_append(current_url, breadcrumbs_list)
                    current_url = context.sub_context(current_url)
                context = context.__parent__

        breadcrumbs_list = breadcrumbs_list[::-1]
        return breadcrumbs_list

    def get_absolute_url(self):
        """
        :return: возвращает путь к текущему ресурсу
        """
        traversal_url = self._get_traversal_url()
        url_root = reverse('router_root')
        absolute_url = url_root + traversal_url
        return absolute_url

    def __get_root(self):
        """
        :return: Возвращает корневой ресурс
        """
        context = self
        while context:
            root = context
            context = context.__parent__
        return root

    # def __search_resource_class_for_name(self, resource_class, resource_class_name):
    #     # Проверем всех детей данного класа на соответствие
    #     for child in resource_class.children:
    #         if child.__name__ == resource_class_name:
    #             return child
    #
    #     # если не нашли, вызовем данную функцию для каждого из них (рекурсия)
    #     for child in resource_class.children:
    #         self.__search_resource_class_for_name(child, resource_class_name)
    #
    # def get_resource_class_for_name(self, resource_class_name):
    #     """
    #     DEPRECATEDВозвращает экземляр класса, по его имени, ищет начиная с корня, и дальше по всем детям
    #     :param resource_class_name:
    #     :return: класс
    #     """
    #     resource = self.__get_root()
    #     # Проверяем, не является ли корневой ресурс искомым
    #     if resource.__class__.__name__ == resource_class_name:
    #         return resource
    #     return self.__search_resource_class_for_name(resource, resource_class_name)

    def get_first_resource_for_class_name(self, resource_class_name):
        """REORGANIZED Возвращает первый экземпляр класса из контекста, по имени класса
        если в контексте нет экземпляров данного класса - вернёт None"""
        for resource in self.full_list:
            if resource.__class__.__name__ == resource_class_name:
                return resource
        return None

    # Внимательно проектируем дерево, помня о возможности выдачи пустых кверисетах
    def __getitem__(self, key):
        """
        В нашей архитектуре потомки определяются в __getitem__ ресурса-родителя, посредством вспомогательного класса
        при этом потомку приходит результат запроса к БД в виде инстанса

        Если не найден потомок - приходит keyError
        Вьюшку уже определяет сам роутер
        а непосредственно работать с основными данными ресурса можно через source

        """
        for child_class_name in self.children:
            try:
                child = resource_registrator.get_res_class_by_name(child_class_name)(key, self, self.request)
                # child.source = child.get_source(self, key)
                # child.brothers_source = child.source
                return child
            except (ObjectDoesNotExist, ValueError, KeyError):
                pass
            except Exception as e:
                raise Exception(e)
        raise KeyError
