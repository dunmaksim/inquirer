u"""Админка для моделей ядра."""


from django.contrib.admin import ModelAdmin
from django.contrib.admin import BooleanFieldListFilter
from django.contrib.admin import site

from core.models import Interrogation
from core.models import AskWithOneAnswer
from core.models import AskWithMultipleAnswers
from core.models import AskWithTextAnswer
from core.models import AnswerForAskWithOneAnswer
from core.models import AnswerForAskWithMultipleAnswers
from core.models import UserAnswersForAskWithOneAnswer
from core.models import UserAnswersForAskWithMultipleAnswers
from core.models import UserTextAnswer


class InterrogationAdmin(ModelAdmin):
    list_display = (
        "name",
        "date_begin",
        "date_end",
        "is_active",
    )

    list_filter = (
        "date_begin",
        "date_end",
        "is_active",
    )

    search_fields = ("name__icontains",)

    list_filter = (("is_active", BooleanFieldListFilter),)


class AskWithOneAnswerAdmin(ModelAdmin):
    list_display = ("text",)


class AskWithMultipleAnswersAdmin(ModelAdmin):
    pass


class AskWithTextAnswerAdmin(ModelAdmin):
    pass


class AnswerForAskWithOneAnswerAdmin(ModelAdmin):
    pass


class AnswerForAskWithMultipleAnswersAdmin(ModelAdmin):
    pass


class UserAnswersForAskWithOneAnswersAdmin(ModelAdmin):
    pass


class UserAnswersForAskWithMultipleAnswersAdmin(ModelAdmin):
    pass


class UserTextAnswersAdmin(ModelAdmin):
    pass


site.register(Interrogation, InterrogationAdmin)
site.register(AskWithOneAnswer, AskWithOneAnswerAdmin)
site.register(AskWithMultipleAnswers, AskWithMultipleAnswersAdmin)
site.register(AskWithTextAnswer, AskWithTextAnswerAdmin)
site.register(AnswerForAskWithOneAnswer, AnswerForAskWithOneAnswerAdmin)
site.register(AnswerForAskWithMultipleAnswers, AnswerForAskWithMultipleAnswersAdmin)
site.register(UserAnswersForAskWithOneAnswer, UserAnswersForAskWithOneAnswersAdmin)
site.register(
    UserAnswersForAskWithMultipleAnswers, UserAnswersForAskWithMultipleAnswersAdmin
)
site.register(UserTextAnswer, UserTextAnswersAdmin)
