from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Question(models.Model):
    name = models.CharField(max_length=255)
    question_text = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")


@python_2_unicode_compatible
class ProductQuestion(models.Model):
    question = models.ForeignKey(Question, related_name="product_questions")
    product = models.ForeignKey("catalogue.Product", related_name="questions")
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return " - ".join([self.question, self.product, self.order])

    class Meta:
        verbose_name = _("Product question")
        verbose_name_plural = _("Product questions")
