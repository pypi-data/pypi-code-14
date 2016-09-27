import json
import re

from django.template import Library, Context
from django.template.loader import get_template


register = Library()


@register.simple_tag(takes_context=True)
def ads_targeting(context):
    return get_template(
        "ads/ads-targeting.html"
    ).render(
        Context({
            "targeting": context.get("targeting")
        })
    )


@register.simple_tag
def dfp_ad(ad_unit, **kwargs):

    template = get_template("ads/dfp.html")

    context = {
        "ad_unit": ad_unit,
    }

    if "css_class" in kwargs:
        context["css_class"] = kwargs["css_class"]

    if kwargs:
        context["targeting"] = json.dumps(kwargs)

    html = template.render(Context(context))

    # This next line just removes extra whitespace: http://stackoverflow.com/a/1546245/931098
    return " ".join(re.sub(r'\n', ' ', html).split())


@register.simple_tag(takes_context=True)
def targeting(context):
    targeting_template = "<script>var TARGETING={};</script>"  # Cute, huh?

    if "targeting" not in context:
        return targeting_template

    return targeting_template.format(json.dumps(context["targeting"]))
