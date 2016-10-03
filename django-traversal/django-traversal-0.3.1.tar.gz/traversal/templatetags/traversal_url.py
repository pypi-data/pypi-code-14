# coding=utf-8
from django import template
from traversal.router import Router
register = template.Library()



@register.simple_tag
def turl(context):
    """
    Шаблонный тег, для формирования URL по контексту
    :param context: ресурс, в контексте которого находится искомый URL
    :param params: имя view, последовательно параметры в URL
    :return: возвращает URL
    """
    abs_url = context.get_absolute_url()

    return abs_url

@register.simple_tag
def turl_add(context, str_res_class_name_or_array, *res_slug_or_slugs):
    """
    Добавляет ресурс в первое возможное место в контексте справа
    :param context:
    :param resource_class_name:
    :param resource_slug:
    :param params:
    :return: возвращает URL
    """
    res_classes_names = str_res_class_name_or_array.split('.')
    url = context.add(res_classes_names, res_slug_or_slugs)

    return url

@register.simple_tag
def turl_add_hierarchy(context, hierarchy_parent_slug, str_res_class_name_or_array, *res_slug_or_slugs):
    """
    Добавляет ресурс в первое возможное место в контексте справа, с использованием иерархий
    :param context:
    :param hierarchy_parent_slug: слаг иерархического родителя, None - если имеет место корень иерархии
    :param resource_class_name:
    :param resource_slug:
    :param params:
    :return: возвращает URL
    """
    res_classes_names = str_res_class_name_or_array.split('.')
    url = context.add(res_classes_names, res_slug_or_slugs, hierarchy_parent_slug=hierarchy_parent_slug)

    return url

@register.simple_tag
def turl_replace(context, str_res_class_name_or_array, *res_slug_or_slugs):
    """
    Заменяет ресурсы заданных классов в URL
    :param context:
    :param resource_class_name:
    :param resource_slug:
    :param params:
    :return: возвращает URL с новыми ресурсами из списка
    """
    # TODO добавить работу с иерархиями

    res_classes_names = str_res_class_name_or_array.split('.')
    url = context.replace(res_classes_names, res_slug_or_slugs)

    return url

@register.simple_tag
def turl_replace_all(context, str_res_class_name_or_array, str_no_replace_res_class_name_or_array, *res_slug_or_slugs):
    """
    Заменяет ресурсы всех классов, на указанные в str_res_class_name_or_array на значения, указанные в res_slug_or_slugs за исключением ресурсов, указанных в str_no_replace_res_class_name_or_array
    :param context:
    :param str_res_class_name_or_array:
    :param str_no_replace_res_class_name_or_array:
    :param res_slug_or_slugs:
    :return: возвращает URL с ресурсами из списков: str_res_class_name_or_array и str_no_replace_res_class_name_or_array
    """

    res_classes_names = str_res_class_name_or_array.split('.')
    no_replace_res_class_names = str_no_replace_res_class_name_or_array.split('.')

    url = context.replace_all(res_classes_names, no_replace_res_class_names, res_slug_or_slugs)

    return url


@register.simple_tag
def turl_soft_replace(context, str_res_class_name_or_array, str_full_replace_res_class_name_or_array, *res_slug_or_slugs):
    """
    Заменяет ресурсы с проверкой на существование полученого URL, если url не существует, последовательно убирает ресурсы из adv_classes_names пока не дойдёт до активного URL
    :param context:
    :param str_res_class_name_or_array:
    :param str_full_replace_res_class_name_or_array: абсолютно точно убирает данные ресурсы
    :param res_slug_or_slugs:
    :return: возвращает URL
    """
    test_router = Router(context.request)
    res_slugs_count = len(res_slug_or_slugs)
    res_classes_names = str_res_class_name_or_array.split('.')
    full_replace_res_class_names = str_full_replace_res_class_name_or_array.split('.')

    # В любом случае заменяются классы
    minimal_classes_names = res_classes_names[0: res_slugs_count]
    # так-же добавим туда классы, подлежащие 100% замене, если такие есть
    minimal_classes_names.extend(full_replace_res_class_names)

    # В случае невозможности заменить только minimal, так-же последовательно исключаются ресурсы из adv_classes_names
    adv_classes_names = res_classes_names[res_slugs_count:]
    url = None
    try:
        url = context.replace(minimal_classes_names, res_slug_or_slugs)
    except:
        pass
    for class_name in adv_classes_names:
        if not test_router.is_exist(url): # проверяет сущеcтвование URL
            minimal_classes_names.append(class_name)
            try:
                url = context.replace(minimal_classes_names, res_slug_or_slugs)
            except:
                pass
        else:
            break # выходим из цикла
    if url:
        return url
    else:
        raise Exception(u'Не удаётся вставить в контекст классы: %s' % res_classes_names)


@register.simple_tag
def turl_sub(context, str_res_class_name_or_array, *res_slugs):
    """
    Удаляет из URL определённые ресурсы
    :param context:
    :param res_classes_names: перечень удаляемых ресурсов, в порядке их появления в URL слева на право
    :param res_slugs: перечень имён удаляевых ресурсов
    :return: возвращает URL без указанных выше ресурсов
    """
    res_classes_names = str_res_class_name_or_array.split('.')
    res_slugs = list(res_slugs)
    res_classes_names, res_slugs = context.add_hierarchy_child(res_classes_names, res_slugs)
    url = context.sub(res_slugs) #res_classes_names,

    return url

@register.simple_tag
def turl_sub_all(context, str_res_class_name_or_array):
    """
    Удаляет из URL определённые классы ресурсов
    :param context:
    :param resource_class_name_array: перечень удаляемых ресурсов, в порядке их появления в URL слева на право
    :param resource_slugs_array: перечень имён удаляевых ресурсов
    :return: возвращает URL без указанных выше ресурсов
    """
    res_classes_names = str_res_class_name_or_array.split('.')
    url = context.sub_all(res_classes_names)

    return url

@register.simple_tag
def turl_for_path(path):
    """
    Практически ручное формирование URL
    :param path: путь к искомому рессурсу, или часть пути. понимает разделение через точку
    :param params: любые динамические параметры, которые требуется присоединить к URL, списком
    :return: возвращает URL
    Пример:
    {% turl_for_path 'blog.list' post.id %}
    """
    path_list = path.split('.')
    url = u'/' + u'/'.join(path_list)

    return url

@register.simple_tag
def show_get_params(get_params):
    """
    Добавляет в ссылку GET параметры прошлого запроса (возможно это велосипед, но пусть будет)
    :param get_params:
    :return:возвращает часть URL с GET параметрами
    """

    get_params_url_part = "?"
    for get_param in get_params.items():
        get_params_url_part = "".join([get_params_url_part, get_param[0], "=", get_param[1], "&"])
    # убираем последний лишний знак &
    get_params_url_part = get_params_url_part[:-1]
    return get_params_url_part

@register.simple_tag
def update_get_params(get_params, new_param, new_value):
    """
    Добавляет в список GET параметров новый параметр, или меняет его знаечение, если такой параметр уже есть
    :param get_params:
    :param new_param:
    :return: возвращает часть URL с GET параметрами
    """
    dict_get_params = {}
    for get_param in get_params:
        dict_get_params[get_param] = get_params[get_param]
    dict_get_params[new_param] = unicode(new_value)
    return show_get_params(dict_get_params)
