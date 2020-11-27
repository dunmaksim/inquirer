u"""
Модели приложения.

У многих из них есть поле creation_date - это для сортировки, потому что
СУБД может выдавать данные безо всякой сортировки, в случайном порядке.
"""

from django.db import models

from django.db.models import Model
from django.db.models import CharField
from django.db.models import BooleanField, DateField, TextField, DateTimeField
from django.db.models import ForeignKey
from django.db.models import CASCADE


class Interrogation(Model):

    u"""Класс опроса.

    name - название
    active - поле типа BooleanField, показывающее, что этот опрос активен
    и может быть пройден. По умолчанию опрос не доступен для прохождения.
    date_begin - дата, с которой можно начинать проходить опрос. Требуется формат
    YYYY-MM-DD
    date_end - дата окончания
    """

    name = CharField(
        u'Название опроса',
        max_length=300,
        unique=True,
        db_index=True
    )

    active = BooleanField(default=False, verbose_name='Активен')

    date_begin = DateField(u"Дата начала")

    date_end = DateField(u"Дата окончания")

    creation_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        u"""Пусть хранятся в таблице interrogation."""

        db_table = 'interrogation'
        verbose_name = u'опрос'
        verbose_name_plural = u'опросы'
        ordering = (
            'creation_date',
            'date_begin',
            'date_end',
        )


class Ask(Model):

    u"""
    Абстрактная модель вопроса. Наследники могут иметь дополнительные свойства,
    но вот эти базовые должны быть там в любом случае.

    text - текст вопроса
    creation_date - дата и время создания вопроса
    interogation - ссылка на опрос, к которому вопрос относится
    """

    text = TextField(u'Текст вопроса')

    creation_date = DateTimeField(auto_now_add=True)

    interrogation = ForeignKey(
        Interrogation,
        on_delete=CASCADE,
        verbose_name='опрос',
    )

    def __str__(self):
        return self.text

    class Meta:
        abstract = True
        verbose_name = u'вопрос'
        verbose_name_plural = u'вопросы'


class AskWithOneAnswer(Ask):

    u"""Модель вопроса с одним правильным ответом."""

    class Meta:
        db_table = 'asks_with_one_answer'
        verbose_name = u'вопрос с одним правильным ответом'
        verbose_name_plural = u'вопросы с одним правильным ответом'
        ordering = ('creation_date',)


class AskWithMultipleAnswers(Ask):

    u"""Модель вопроса, подразумевающего несколько ответов."""

    class Meta:
        db_table = 'asks_with_multiple_answers'
        verbose_name = u'вопрос с множеством ответов'
        verbose_name_plural = u'вопросы с множеством ответов'
        ordering = ('creation_date',)


class AskWithTextAnswer(Ask):

    u"""Модель вопроса, подразумевающего свободный ответ (текстом)."""

    class Meta:
        db_table = 'asks_with_text_answer'
        verbose_name = u'вопрос с текстовым ответом'
        verbose_name_plural = u'вопросы с текстовым ответом'
        ordering = ('creation_date',)


class AbstractAnswer(Model):

    text = CharField(u'Ответ на вопрос', max_length=300)

    creation_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        abstract = True

class AnswerForAskWithOneAnswer(AbstractAnswer):

    u"""Модель ответа на вопрос с одним ответом."""

    ask = ForeignKey(AskWithOneAnswer, on_delete=CASCADE, related_name='answers')

    class Meta:
        db_table = 'answers_to_ask_with_one_answer'
        verbose_name = u'ответ на вопрос с одним ответом'
        verbose_name_plural = u'ответы на вопрос с одним ответом'


class AnswerForAskWithMultipleAnswers(AbstractAnswer):

    u"""Модель ответа на вопрос с множеством доступных ответов."""

    ask = ForeignKey(AskWithMultipleAnswers, on_delete=CASCADE, related_name='answers')

    class Meta:
        db_table = 'answers_to_ask_with_multiple_answers'
        verbose_name = u'ответ на вопрос с множеством ответов'
        verbose_name_plural = u'ответы на вопрос с множеством ответов'
