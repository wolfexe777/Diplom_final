from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name='Имя', blank=True, null=True)
    second_name = models.CharField(max_length=255, verbose_name='Фамилия', blank=True, null=True)
    middle_name = models.CharField(max_length=255, verbose_name='Отчество', blank=True, null=True)
    email = models.EmailField(unique=True, null=False, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Номер телефона')
    date_of_birth = models.DateField(max_length=15, blank=True, null=True, verbose_name='Дата рождения')
    groups = models.ManyToManyField(Group, related_name='custom_users', blank=True, verbose_name='Группы')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_users', blank=True, verbose_name='Права пользователя'
    )
    def __str__(self):
        return self.username

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Вопрос', null=True, blank=True)


    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос теста "Шкала депрессии Бэка"'
        verbose_name_plural = 'Вопросы теста "Шкала депрессии Бэка"'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    choice_text = models.CharField(max_length=300, null=True, verbose_name='Варианты ответов')
    points = models.IntegerField(default=0, verbose_name='Баллы')

    def __str__(self):
        return self.choice_text

class TestResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='test_results',  null=True, blank=True, verbose_name='Имя')
    score = models.IntegerField(verbose_name='Баллы')
    result_message = models.CharField(max_length=255, null=True, blank=True, verbose_name='Описание результата')
    date_completed = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата прохождения')
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Результаты {self.user.username}"

    class Meta:
        verbose_name = 'Результат клиента "Шкала депресии Бэка"'
        verbose_name_plural = 'Результат клиента "Шкала депресии Бэка"'

        # ТЕСТ шкалы тревоги БЭКА

class AnxietyTestQuestion(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Вопрос', null=True, blank=True)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос теста "Шкала тревоги Бэка"'
        verbose_name_plural = 'Вопросы теста "Шкала тревоги Бэка"'

class AnxietyTestChoice(models.Model):
    question = models.ForeignKey(AnxietyTestQuestion, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Вопрос')
    choice_text = models.CharField(max_length=300, null=True, verbose_name='Варианты ответов "Шкала тревоги Бэка"')
    points = models.IntegerField(default=0, verbose_name='Баллы "Шкала тревоги Бэка"')

    def __str__(self):
        return self.choice_text

class AnxietyTestResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='anxiety_test_results',  null=True, blank=True, verbose_name='Имя')
    score = models.IntegerField(verbose_name='Баллы')
    result_message = models.CharField(max_length=255, null=True, blank=True, verbose_name='Описание результата')
    date_completed = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата прохождения')
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Результаты {self.user.username}"

    class Meta:
        verbose_name = 'Результат клиета "Шкала тревоги Бэка"'
        verbose_name_plural = 'Результаты клиетов "Шкала тревоги Бэка"'


# Тест шкалы импульсивности Баррета

class ImpulsivityTestQuestion(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Вопрос', null=True, blank=True)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос теста "Шкала импульсивности Барратта"'
        verbose_name_plural = 'Вопросы теста "Шкала импульсивности Барратта"'

class ImpulsivityTestChoice(models.Model):
    question = models.ForeignKey(ImpulsivityTestQuestion, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Вопросы')
    choice_text = models.CharField(max_length=300, null=True, verbose_name='Варианты ответов')
    points = models.IntegerField(default=0, verbose_name='Баллы')

    def __str__(self):
        return self.choice_text

class ImpulsivityTestResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='impulsivity_test_results',  null=True, blank=True, verbose_name='Имя')
    score = models.IntegerField(verbose_name='Баллы')
    result_message = models.CharField(max_length=255, null=True, blank=True, verbose_name='Описание результата')
    date_completed = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата прохождения')
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Результаты {self.user.username}"

    class Meta:
        verbose_name = 'Результат клиета "Шкала импульсивности Барратта"'
        verbose_name_plural = 'Результаты клиетов "Шкала импульсивности Барратта"'

    # Тест шкалы самосотрадания Кристин Нефф

class SelfcompassionTestQuestion(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Вопрос', null=True, blank=True)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос теста "Шкала самосострадания Кристин Нефф"'
        verbose_name_plural = 'Вопросы теста "Шкала самосострадания Кристин Нефф"'

class SelfcompassionTestChoice(models.Model):
    question = models.ForeignKey(SelfcompassionTestQuestion, on_delete=models.CASCADE, null=True, blank=True)
    choice_text = models.CharField(max_length=300, null=True, verbose_name='Варианты ответов')
    points = models.IntegerField(default=0, verbose_name='Баллы')

    def __str__(self):
        return self.choice_text

class SelfcompassionTestResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='selfcompassion_test_results',  null=True, blank=True, verbose_name='Имя')
    score = models.FloatField(null=True, blank=True, verbose_name='Баллы')
    result_message = models.CharField(max_length=255, null=True, blank=True, verbose_name='Описание результата')
    date_completed = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата прохождения')
    email = models.EmailField(null=True, blank=True)

    kindness_score = models.FloatField(verbose_name='Доброта к себе')
    self_blame_score = models.FloatField(verbose_name='Самоосуждение')
    human_commonality_score = models.FloatField(verbose_name='Человеческая общность')
    isolation_score = models.FloatField(verbose_name='Изоляция')
    mindfulness_score = models.FloatField(verbose_name='Осознанность')
    overidentification_score = models.FloatField(verbose_name='Сверхидентификация')
    total_score = models.FloatField(verbose_name='Общий балл')
    def __str__(self):
        return f"Результаты {self.user.username}"

    class Meta:
        verbose_name = 'Результат клиета "Шкала самосострадания Кристин Нефф"'
        verbose_name_plural = 'Результаты клиетов "Шкала самосострадания Кристин Нефф"'

        # ТЕСТ ПИЩЕВОЕ ПОВЕДЕНИЕ
class FoodbehaviorTestQuestion(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Вопрос', null=True, blank=True)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос теста "Шкала пищевого поведения"'
        verbose_name_plural = 'Вопросы теста "Шкала пищевого поведения"'

class FoodbehaviorTestChoice(models.Model):
    question = models.ForeignKey(FoodbehaviorTestQuestion, on_delete=models.CASCADE, null=True, blank=True)
    choice_text = models.CharField(max_length=300, null=True, verbose_name='Варианты ответов')
    points = models.IntegerField(default=0, verbose_name='Баллы')

    def __str__(self):
        return self.choice_text

class FoodbehaviorTestResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='food_behavior_results', null=True, blank=True, verbose_name='Имя')
    date_completed = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата прохождения')
    email = models.EmailField(null=True, blank=True)

    # Добавление поля для каждой категории
    thinness_striving_score = models.IntegerField(verbose_name='Стремление к худобе')
    thinness_striving_stenain = models.IntegerField(default=0, verbose_name='Стенайн "Стремление к худобе"')
    bulimia_score = models.IntegerField(verbose_name='Булимия')
    bulimia_stenain = models.IntegerField(default=0, verbose_name='Стенайн "Булимия"')
    body_dissatisfaction_score = models.IntegerField(verbose_name='Неудовлетворенность телом')
    body_dissatisfaction_stenain = models.IntegerField(default=0, verbose_name='Стенайн "Неудовлетворенность телом"')
    ineffectiveness_score = models.IntegerField(verbose_name='Неэффективность')
    ineffectiveness_stenain = models.IntegerField(default=0, verbose_name='Стенайн "Неэффективность"')
    perfectionism_score = models.IntegerField(verbose_name='Перфекционизм')
    perfectionism_stenain = models.IntegerField(default=0, verbose_name='Стенайн "Перфекционизм"')
    interpersonal_distrust_score = models.IntegerField(verbose_name='Недоверие в межличностных отношениях')
    interpersonal_distrust_stenain = models.IntegerField(default=0, verbose_name='Стенайн "Недоверие в межличностных отношениях"')
    interoceptive_incompetence_score = models.IntegerField(verbose_name='Интероцептивная некомпетентность')
    interoceptive_incompetence_stenain = models.IntegerField(default=0, verbose_name='Стенайн "Интероцептивная некомпетентность"')
    result_message = models.CharField(max_length=255, null=True, blank=True, verbose_name='Описание результата')

    def __str__(self):
        return f"Результаты {self.user.username if self.user else 'No User'}"
    class Meta:
        verbose_name = 'Результат клиента "Шкала пищевого поведения"'
        verbose_name_plural = 'Результаты клиентов "Шкала пищевого поведения"'