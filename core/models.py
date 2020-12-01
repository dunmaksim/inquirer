u"""
Модели приложения.

У многих из них есть поле creation_date - это для сортировки, потому что
СУБД может выдавать данные безо всякой сортировки, в случайном порядке.
"""

from django.db.models import BooleanField
from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Manager
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models import PositiveIntegerField
from django.db.models import TextField
from django.utils import timezone
from django.contrib.auth.models import User


class ActiveInterrogationManager(Manager):
    u"""Класс для работы с активными опросами."""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ActiveRightNowInterrogationManager(Manager):
    u"""Класс для работы с доступными прямо сейчас опросами."""
    def get_queryset(self):

        now = timezone.now()

        return (super().get_queryset().filter(is_active=True).filter(
            date_begin__lt=now).filter(date_end__gt=now))


class Interrogation(Model):
    u"""Класс опроса.

    name - название
    active - поле типа BooleanField, показывающее, что этот опрос активен
    и может быть пройден. По умолчанию опрос не доступен для прохождения.
    date_begin - дата, с которой можно начинать проходить опрос. Требуется формат
    YYYY-MM-DD
    date_end - дата окончания
    """

    name = CharField(u"Название опроса",
                     max_length=300,
                     unique=True,
                     db_index=True)

    is_active = BooleanField(default=False, verbose_name="Активен")

    date_begin = DateField(u"Дата начала")

    date_end = DateField(u"Дата окончания")

    creation_date = DateTimeField(auto_now_add=True)

    only_active = ActiveInterrogationManager()

    active_right_now = ActiveRightNowInterrogationManager()

    description = TextField(u"Описание опроса.", blank=True)

    def __str__(self):
        u"В строковом представлении будет просто выводиться название опроса."
        return self.name

    class Meta:
        u"""Пусть хранятся в таблице interrogation."""

        db_table = "interrogation"
        verbose_name = u"опрос"
        verbose_name_plural = u"опросы"
        ordering = (
            "creation_date",
            "date_begin",
            "date_end",
        )


class Ask(Model):
    u"""
    Абстрактная модель вопроса. Наследники могут иметь дополнительные свойства,
    но вот эти базовые должны быть там в любом случае.

    text - текст вопроса
    creation_date - дата и время создания вопроса
    interogation - ссылка на опрос, к которому вопрос относится
    """

    text = TextField(u"Текст вопроса")

    creation_date = DateTimeField(auto_now_add=True)

    interrogation = ForeignKey(
        Interrogation,
        on_delete=CASCADE,
        verbose_name="опрос",
    )

    def __str__(self):
        return self.text

    class Meta:
        abstract = True
        verbose_name = u"вопрос"
        verbose_name_plural = u"вопросы"


class AskWithOneAnswer(Ask):
    u"""Модель вопроса с одним правильным ответом."""
    class Meta:
        db_table = "asks_with_one_answer"
        verbose_name = u"вопрос с одним правильным ответом"
        verbose_name_plural = u"вопросы с одним правильным ответом"
        ordering = ("creation_date", )


class AskWithMultipleAnswers(Ask):
    u"""Модель вопроса, подразумевающего несколько ответов."""
    class Meta:
        db_table = "asks_with_multiple_answers"
        verbose_name = u"вопрос с множеством ответов"
        verbose_name_plural = u"вопросы с множеством ответов"
        ordering = ("creation_date", )


class AskWithTextAnswer(Ask):
    u"""Модель вопроса, подразумевающего свободный ответ (текстом)."""
    class Meta:
        db_table = "asks_with_text_answer"
        verbose_name = u"вопрос с текстовым ответом"
        verbose_name_plural = u"вопросы с текстовым ответом"
        ordering = ("creation_date", )


class AbstractAnswer(Model):
    u"""Общие свойства ответов."""

    text = CharField(u"Ответ на вопрос", max_length=300)

    creation_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


class AnswerForAskWithOneAnswer(AbstractAnswer):
    u"""Модель ответа на вопрос с одним ответом."""

    ask = ForeignKey(AskWithOneAnswer,
                     on_delete=CASCADE,
                     related_name="answers")

    class Meta:
        db_table = "answers_to_ask_with_one_answer"
        verbose_name = u"ответ на вопрос с одним ответом"
        verbose_name_plural = u"ответы на вопрос с одним ответом"


class AnswerForAskWithMultipleAnswers(AbstractAnswer):
    u"""Модель ответа на вопрос с множеством доступных ответов."""

    ask = ForeignKey(AskWithMultipleAnswers,
                     on_delete=CASCADE,
                     related_name="answers")

    class Meta:
        db_table = "answers_to_ask_with_multiple_answers"
        verbose_name = u"ответ на вопрос с множеством ответов"
        verbose_name_plural = u"ответы на вопрос с множеством ответов"


class AbstractUserAnswer(Model):
    u"""
    Общие свойства ответов на вопросы.

    user_id - берется из данных сессии, нужно для работы с анончиками
    user - ссылка на django.contrib.auth.models.User
    """

    anonymous_user_id = PositiveIntegerField(
        u"id анонимного пользователя",
        blank=True,
        null=True
    )

    user = ForeignKey(User,
                      on_delete=CASCADE,
                      verbose_name=u'Пользователь',
                      blank=True,
                      null=True)

    class Meta:
        u"""Просто укажем, что это полностью абстрактная модель."""
        abstract = True


class UserAnswersForAskWithOneAnswer(AbstractUserAnswer):
    u"""
    Модель для хранения ответов на вопросы с одним ответом.

    answer - ответ, который дал пользователь.
    """

    answer = ForeignKey(AnswerForAskWithOneAnswer, on_delete=CASCADE)

    class Meta:
        db_table = 'user_single_answers'
        verbose_name = u"ответ пользователя на вопрос с одним ответом"
        verbose_name_plural = u"ответы пользователя на вопросы с одним ответом"


class UserAnswersForAskWithMultipleAnswers(AbstractUserAnswer):
    u"""
    Модель ответов на вопросы, подразумевающие несколько правильных
    ответов.
    """

    answers = ManyToManyField(AnswerForAskWithMultipleAnswers)

    class Meta:
        db_table = 'user_multi_answers'
        verbose_name = u"ответ пользователя на вопрос с множеством ответов"


class UserTextAnswer(AbstractUserAnswer):
    u"""
    Модель ответа пользователя на вопрос, подразумевающий развернутый ответ.
    """

    answer = TextField()

    class Meta:
        u"""Отдельная таблица и описание для админки."""

        db_table = 'user_text_answers'
        verbose_name = u"текстовый ответ пользователя"
        verbose_name_plural = u"текстовые ответы пользователя"
