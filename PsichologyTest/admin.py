from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Question, Choice, CustomUser, TestResult, AnxietyTestQuestion, AnxietyTestChoice, AnxietyTestResult, ImpulsivityTestQuestion, ImpulsivityTestChoice, ImpulsivityTestResult, SelfcompassionTestQuestion, SelfcompassionTestChoice, SelfcompassionTestResult, FoodbehaviorTestChoice, FoodbehaviorTestQuestion, FoodbehaviorTestResult


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class AnxietyTestChoiceInline(admin.TabularInline):
    model = AnxietyTestChoice
    extra = 0


class ImpulsivityTestChoiceInline(admin.TabularInline):
    model = ImpulsivityTestChoice
    extra = 0

class SelfcompassionTestChoiceInline(admin.TabularInline):
    model = SelfcompassionTestChoice
    extra = 0

class FoodbehaviorTestChoiceInline(admin.TabularInline):
    model = FoodbehaviorTestChoice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    actions = ['delete_with_choices']

    def delete_with_choices(self, request, queryset):
        for question in queryset:
            question.delete()

    delete_with_choices.short_description = "Удалить с ответами"

admin.site.register(Question, QuestionAdmin)


class AnxietyTestQuestionAdmin(admin.ModelAdmin):
    inlines = [AnxietyTestChoiceInline]
    actions = ['delete_with_choices']

    def delete_with_choices(self, request, queryset):
        for question in queryset:
            question.delete()

    delete_with_choices.short_description = "Удалить с ответами"

admin.site.register(AnxietyTestQuestion, AnxietyTestQuestionAdmin)


class ImpulsivityTestQuestionAdmin(admin.ModelAdmin):
    inlines = [ImpulsivityTestChoiceInline]
    actions = ['delete_with_choices']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # При сохранении вопроса создаем варианты ответов, если их еще нет
        if not obj.impulsivitytestchoice_set.exists():
            # Присваиваем баллы в порядке добавления вариантов ответов к вопросу
            for i, choice_text in enumerate(["Редко или никогда.", "Иногда.", "Часто.", "Всегда или почти всегда."]):
                ImpulsivityTestChoice.objects.create(question=obj, choice_text=choice_text, points=i+1)


    def delete_with_choices(self, request, queryset):
        for question in queryset:
            question.delete()

    delete_with_choices.short_description = "Удалить с ответами"

admin.site.register(ImpulsivityTestQuestion, ImpulsivityTestQuestionAdmin)

class SelfcompassionTestQuestionAdmin(admin.ModelAdmin):
    inlines = [SelfcompassionTestChoiceInline]
    actions = ['delete_with_choices']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.selfcompassiontestchoice_set.exists():
            for i, choice_text in enumerate(["Почти никогда.", "Редко.", "Обычно.", "Часто", "Почти всегда."]):
                SelfcompassionTestChoice.objects.create(question=obj, choice_text=choice_text, points=i+1)

    def delete_with_choices(self, request, queryset):
        for question in queryset:
            question.delete()

    delete_with_choices.short_description = "Удалить с ответами"

admin.site.register(SelfcompassionTestQuestion, SelfcompassionTestQuestionAdmin)


class FoodbehaviorTestQuestionAdmin(admin.ModelAdmin):
    inlines = [FoodbehaviorTestChoiceInline]
    actions = ['delete_with_choices']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.foodbehaviortestchoice_set.exists():
            points_mapping = [0, 0, 0, 1, 2, 3]
            for i, choice_text in enumerate(["Никогда.", "Редко.", "Иногда.", "Часто", "Обычно", "Всегда."]):
                FoodbehaviorTestChoice.objects.create(question=obj, choice_text=choice_text, points=points_mapping[i])

    def delete_with_choices(self, request, queryset):
        for question in queryset:
            question.delete()

    delete_with_choices.short_description = "Удалить с ответами"

admin.site.register(FoodbehaviorTestQuestion, FoodbehaviorTestQuestionAdmin)


class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 0
    fields = ('score', 'result_message', 'date_completed')
    readonly_fields = ('score', 'result_message', 'date_completed')

class AnxietyTestResultInline(admin.TabularInline):
    model = AnxietyTestResult
    extra = 0
    fields = ('score', 'result_message', 'date_completed')
    readonly_fields = ('score', 'result_message', 'date_completed')

class ImpulsivityTestResultInline(admin.TabularInline):
    model = ImpulsivityTestResult
    extra = 0
    fields = ('score', 'result_message', 'date_completed')
    readonly_fields = ('score', 'result_message', 'date_completed')

class SelfcompassionTestResultInline(admin.TabularInline):
    model = SelfcompassionTestResult
    extra = 0
    fields = ('score', 'result_message', 'date_completed')
    readonly_fields = ('score', 'result_message', 'date_completed')

class FoodbehaviorTestResultInline(admin.TabularInline):
    model = FoodbehaviorTestResult
    extra = 0
    fields = (
        'thinness_striving_stenain',
        'bulimia_stenain',
        'body_dissatisfaction_stenain',
        'ineffectiveness_stenain',
        'perfectionism_stenain',
        'interpersonal_distrust_stenain',
        'interoceptive_incompetence_stenain',
        'date_completed'
    )
    readonly_fields = (
        'thinness_striving_stenain',
        'bulimia_stenain',
        'body_dissatisfaction_stenain',
        'ineffectiveness_stenain',
        'perfectionism_stenain',
        'interpersonal_distrust_stenain',
        'interoceptive_incompetence_stenain',
        'date_completed'
    )
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('display_username', 'display_score', 'display_result_message', 'display_date_completed')
    search_fields = ('user__username', 'score', 'date_completed')

    def display_username(self, obj):
        return obj.user.username

    def display_score(self, obj):
        return obj.score

    def display_result_message(self, obj):
        return obj.result_message

    def display_date_completed(self, obj):
        return obj.date_completed

    display_username.short_description = 'Ник клиента'
    display_score.short_description = 'Баллы'
    display_result_message.short_description = 'Результаты теста'
    display_date_completed.short_description = 'Дата прохождения'

admin.site.register(TestResult, TestResultAdmin)

class AnxietyTestResultAdmin(admin.ModelAdmin):
    list_display = ('display_username', 'display_score', 'display_result_message', 'display_date_completed')
    search_fields = ('user__username', 'score', 'date_completed')

    def display_username(self, obj):
        return obj.user.username

    def display_score(self, obj):
        return obj.score

    def display_result_message(self, obj):
        return obj.result_message

    def display_date_completed(self, obj):
        return obj.date_completed

    display_username.short_description = 'Ник клиента'
    display_score.short_description = 'Баллы'
    display_result_message.short_description = 'Результаты теста'
    display_date_completed.short_description = 'Дата прохождения'

admin.site.register(AnxietyTestResult, AnxietyTestResultAdmin)


class ImpulsivityTestResultAdmin(admin.ModelAdmin):
    list_display = ('display_username', 'display_score', 'display_result_message', 'display_date_completed')
    search_fields = ('user__username', 'score', 'date_completed')

    def display_username(self, obj):
        return obj.user.username

    def display_score(self, obj):
        return obj.score

    def display_result_message(self, obj):
        return obj.result_message

    def display_date_completed(self, obj):
        return obj.date_completed

    display_username.short_description = 'Ник клиента'
    display_score.short_description = 'Баллы теста'
    display_result_message.short_description = 'Сообщение о результате теста'
    display_date_completed.short_description = 'Дата прохождения теста'

admin.site.register(ImpulsivityTestResult, ImpulsivityTestResultAdmin)

class SelfcompassionTestResultAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'kindness_average',
        'self_blame_average',
        'human_commonality_average',
        'isolation_average',
        'mindfulness_average',
        'overidentification_average',
        'total_score',
        'result_message',
        'display_date_completed'
    )
    search_fields = ('user__username', 'user__email')

    def kindness_average(self, obj):
        return (obj.kindness_score) if obj.kindness_score else None

    def self_blame_average(self, obj):
        return (obj.self_blame_score) if obj.self_blame_score else None

    def human_commonality_average(self, obj):
        return (obj.human_commonality_score) if obj.human_commonality_score else None

    def isolation_average(self, obj):
        return (obj.isolation_score) if obj.isolation_score else None

    def mindfulness_average(self, obj):
        return (obj.mindfulness_score) if obj.mindfulness_score else None

    def overidentification_average(self, obj):
        return (obj.overidentification_score) if obj.overidentification_score else None

    def total_score(self, obj):
        return (obj.total_score) if obj.total_score else None

    def display_date_completed(self, obj):
        return obj.date_completed

    kindness_average.short_description = 'Доброта к себе'
    self_blame_average.short_description = 'Самоосуждение'
    human_commonality_average.short_description = 'Человеческая общность'
    isolation_average.short_description = 'Изоляция'
    mindfulness_average.short_description = 'Осознанность'
    overidentification_average.short_description = 'Сверхидентификация'
    total_score.short_description = 'Общий балл'
    display_date_completed.short_description = 'Дата прохождения теста'

admin.site.register(SelfcompassionTestResult, SelfcompassionTestResultAdmin)

class FoodbehaviorTestResultAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'thinness_striving_stenain',
        'bulimia_stenain',
        'body_dissatisfaction_stenain',
        'ineffectiveness_stenain',
        'perfectionism_stenain',
        'interpersonal_distrust_stenain',
        'interoceptive_incompetence_stenain',
        'date_completed'
    )
    search_fields = ('user__username', 'user__email')

    def display_date_completed(self, obj):
        return obj.date_completed

    display_date_completed.short_description = 'Дата прохождения теста'

admin.site.register(FoodbehaviorTestResult, FoodbehaviorTestResultAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'second_name', 'middle_name','date_of_birth',
        'phone_number', 'score', 'result_message', 'date_completed'
    )
    search_fields = ('username', 'email', 'first_name', 'second_name', 'phone_number')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональные данные', {'fields': ('email', 'first_name', 'second_name', 'middle_name', 'phone_number','date_of_birth')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    inlines = [TestResultInline, AnxietyTestResultInline, ImpulsivityTestResultInline, SelfcompassionTestResultInline, FoodbehaviorTestResultInline]

    def score(self, obj):
        return obj.test_results.first().score if obj.test_results.first() else ''

    def result_message(self, obj):
        return obj.test_results.first().result_message if obj.test_results.first() else ''

    def date_completed(self, obj):
        return obj.test_results.first().date_completed if obj.test_results.first() else ''

    score.admin_order_field = 'test_results__score'
    result_message.admin_order_field = 'test_results__result_message'
    date_completed.admin_order_field = 'test_results__date_completed'

    score.short_description = 'Баллы теста'
    result_message.short_description = 'Результаты теста'
    date_completed.short_description = 'Дата прохождения теста'

    actions = ['delete_with_results']

    def delete_with_results(self, request, queryset):
        for user in queryset:
            user.delete()

    delete_with_results.short_description = "Удалить с результатами тестов"

admin.site.register(CustomUser, CustomUserAdmin)