from django.db import models
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import pgettext_lazy, ugettext_lazy as _


@python_2_unicode_compatible
class Question(models.Model):
    name = models.CharField(
        max_length=255, verbose_name=pgettext_lazy("Inanimate object", "Name"))
    question_text = models.TextField(verbose_name=_("Question text"))
    answer = models.TextField(verbose_name=_("Answer"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")


@python_2_unicode_compatible
class ProductQuestion(models.Model):
    question = models.ForeignKey(
        Question, related_name="product_questions", verbose_name=_("Question"))
    product = models.ForeignKey("catalogue.Product", related_name="questions",
                                verbose_name=_("Product"))
    order = models.IntegerField(
        null=True, blank=True, verbose_name=pgettext_lazy("As in ordering", "Order"))

    def __str__(self):
        return " - ".join([force_text(self.question),
                           self.product,
                           self.order])

    class Meta:
        verbose_name = _("Product question")
        verbose_name_plural = _("Product questions")
