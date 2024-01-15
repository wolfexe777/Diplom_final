from .models import Question, Choice, TestResult, FoodbehaviorTestQuestion, FoodbehaviorTestChoice, FoodbehaviorTestResult, AnxietyTestQuestion, AnxietyTestChoice, AnxietyTestResult, ImpulsivityTestQuestion, ImpulsivityTestChoice, ImpulsivityTestResult, SelfcompassionTestQuestion, SelfcompassionTestChoice, SelfcompassionTestResult
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('Agg')
from io import BytesIO
import base64
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'base.html')

def test(request):
    if request.method == 'POST':
        score = 0
        for question in Question.objects.all():
            user_choice_id = request.POST.get(f'question_{question.id}')
            if user_choice_id:
                user_choice = Choice.objects.get(id=user_choice_id)
                score += user_choice.points

        result_message = get_result_message(score)

        # Если пользователь не авторизован, предложить сохранить результаты
        if not request.user.is_authenticated:
            request.session['test_result'] = {'score': score, 'result_message': result_message}
            return render(request, 'PsichologyTest/BeckDepression/offer_save_result.html', {'score': score, 'result_message': result_message})

        # Если пользователь авторизован, сохраняем результаты в базе данных
        TestResult.objects.create(user=request.user, score=score, result_message=result_message)

        # Вместо вызова функции test_results, возвращаем рендеринг страницы с результатами
        return render(request, 'PsichologyTest/BeckDepression/test_results.html', {'score': score, 'result_message': result_message})

    questions = Question.objects.all()
    return render(request, 'PsichologyTest/BeckDepression/test.html', {'questions': questions})

def anxiety_test(request):
    if request.method == 'POST':
        score = 0
        for question in AnxietyTestQuestion.objects.all():
            user_choice_id = request.POST.get(f'question_{question.id}')
            if user_choice_id:
                user_choice = AnxietyTestChoice.objects.get(id=user_choice_id)
                score += user_choice.points

        result_message = anxiety_get_result_message(score)

        # Если пользователь не авторизован, предложить сохранить результаты
        if not request.user.is_authenticated:
            request.session['test_result'] = {'score': score, 'result_message': result_message}
            return render(request, 'PsichologyTest/BeckAnxiety/anxiety_offer_save_result.html', {'score': score, 'result_message': result_message})

        # Если пользователь авторизован, сохраняем результаты в базе данных
        AnxietyTestResult.objects.create(user=request.user, score=score, result_message=result_message)

        # Вместо вызова функции test_results, возвращаем рендеринг страницы с результатами
        return render(request, 'PsichologyTest/BeckAnxiety/anxiety_test_results.html', {'score': score, 'result_message': result_message})

    questions = AnxietyTestQuestion.objects.all()
    return render(request, 'PsichologyTest/BeckAnxiety/anxiety_test.html', {'questions': questions})


def impulsivity_test(request):
    if request.method == 'POST':
        score = 0
        for question in ImpulsivityTestQuestion.objects.all():
            user_choice_id = request.POST.get(f'question_{question.id}')
            if user_choice_id:
                user_choice = ImpulsivityTestChoice.objects.get(id=user_choice_id)
                # Добавляем или вычитаем баллы в соответствии с формулой
                if question.id in [1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 18, 22, 23, 24, 25, 27, 28, 29, 30]:
                    score += user_choice.points
                else:
                    score -= user_choice.points

        # Добавляем фиксированные 55 баллов в конце
        score += 55

        result_message = impulsivity_get_result_message(score)

        # Если пользователь не авторизован, предложить сохранить результаты
        if not request.user.is_authenticated:
            request.session['test_result'] = {'score': score, 'result_message': result_message}
            return render(request, 'PsichologyTest/Impulsivity/impulsivity_offer_save_result.html', {'score': score, 'result_message': result_message})

        # Если пользователь авторизован, сохраняем результаты в базе данных
        ImpulsivityTestResult.objects.create(user=request.user, score=score, result_message=result_message)

        # Вместо вызова функции test_results, возвращаем рендеринг страницы с результатами
        return render(request, 'PsichologyTest/Impulsivity/impulsivity_test_results.html', {'score': score, 'result_message': result_message})

    questions = ImpulsivityTestQuestion.objects.all()
    return render(request, 'PsichologyTest/Impulsivity/impulsivity_test.html', {'questions': questions})


def selfcompassion_test(request):
    if request.method == 'POST':
        kindness_score = 0
        self_blame_score = 0
        human_commonality_score = 0
        isolation_score = 0
        mindfulness_score = 0
        overidentification_score = 0

        # Вопросы для каждой категории
        kindness_questions = [5, 12, 19, 23, 26]
        self_blame_questions = [1, 8, 11, 16, 21]
        human_commonality_questions = [3, 7, 10, 15]
        isolation_questions = [4, 13, 18, 25]
        mindfulness_questions = [9, 14, 17, 22]
        overidentification_questions = [2, 6, 20, 24]

        for question in SelfcompassionTestQuestion.objects.all():
            user_choice_id = request.POST.get(f'question_{question.id}')
            if user_choice_id:
                user_choice = SelfcompassionTestChoice.objects.get(id=user_choice_id)
                if question.id in kindness_questions:
                    kindness_score += user_choice.points
                elif question.id in self_blame_questions:
                    self_blame_score += user_choice.points
                elif question.id in human_commonality_questions:
                    human_commonality_score += user_choice.points
                elif question.id in isolation_questions:
                    isolation_score += user_choice.points
                elif question.id in mindfulness_questions:
                    mindfulness_score += user_choice.points
                elif question.id in overidentification_questions:
                    overidentification_score += user_choice.points

        # Рассчитываем средний балл для каждой категории
        kindness_average = round(kindness_score / len(kindness_questions), 1)
        self_blame_average = round(self_blame_score / len(self_blame_questions), 1)
        human_commonality_average = round(human_commonality_score / len(human_commonality_questions), 1)
        isolation_average = round(isolation_score / len(isolation_questions), 1)
        mindfulness_average = round(mindfulness_score / len(mindfulness_questions), 1)
        overidentification_average = round(overidentification_score / len(overidentification_questions), 1)

        # Общий балл
        total_score = round((kindness_average + self_blame_average + human_commonality_average +
                             isolation_average + mindfulness_average + overidentification_average) / 6, 1)

        result_message = selfcompassion_get_result_message(total_score)

        # Если пользователь не авторизован, предложить сохранить результаты
        if not request.user.is_authenticated:
            request.session['selfcompassion_test_result'] = {
                'kindness_average': kindness_average,
                'self_blame_average': self_blame_average,
                'human_commonality_average': human_commonality_average,
                'isolation_average': isolation_average,
                'mindfulness_average': mindfulness_average,
                'overidentification_average': overidentification_average,
                'total_score': total_score,
                'result_message': result_message
            }
            return render(request, 'PsichologyTest/Selfcompassion/selfcompassion_offer_save_result.html', {
                'kindness_average': kindness_average,
                'self_blame_average': self_blame_average,
                'human_commonality_average': human_commonality_average,
                'isolation_average': isolation_average,
                'mindfulness_average': mindfulness_average,
                'overidentification_average': overidentification_average,
                'total_score': total_score,
                'result_message': result_message
            })

        # Если пользователь авторизован, сохраняем результаты в базе данных
        SelfcompassionTestResult.objects.create(
            user=request.user,
            kindness_score=kindness_average,
            self_blame_score=self_blame_average,
            human_commonality_score=human_commonality_average,
            isolation_score=isolation_average,
            mindfulness_score=mindfulness_average,
            overidentification_score=overidentification_average,
            total_score=total_score,
            result_message=result_message
        )
        # Вместо вызова функции test_results, возвращаем рендеринг страницы с результатами
        return render(request, 'PsichologyTest/Selfcompassion/selfcompassion_test_results.html', {
            'kindness_average': kindness_average,
            'self_blame_average': self_blame_average,
            'human_commonality_average': human_commonality_average,
            'isolation_average': isolation_average,
            'mindfulness_average': mindfulness_average,
            'overidentification_average': overidentification_average,
            'total_score': total_score,
            'result_message': result_message
        })

    questions = SelfcompassionTestQuestion.objects.all()
    return render(request, 'PsichologyTest/Selfcompassion/selfcompassion_test.html', {'questions': questions})


def calculate_stenain(score, score_ranges):
    # Ищем соответствующий диапазон и возвращаем соответствующий стенайн
    for score_range, stenain in score_ranges.items():
        if isinstance(score_range, tuple) and score_range[0] <= score <= score_range[1]:
            return stenain
        elif score == score_range:
            return stenain
    # В случае, если балл не входит в заданные интервалы
    return 0
def foodbehavior_test(request):
    if request.method == 'POST':
        # Инициализация переменных для баллов по категориям
        thinness_striving_score = 0
        bulimia_score = 0
        body_dissatisfaction_score = 0
        ineffectiveness_score = 0
        perfectionism_score = 0
        interpersonal_distrust_score = 0
        interoceptive_incompetence_score = 0

        # Вопросы для каждой категории
        thinness_striving_questions = [1, 8, 12, 18, 25]
        bulimia_questions = [3, 4, 21, 30, 37, 41, 48, 51]
        body_dissatisfaction_questions = [2, 6, 9, 14, 24, 36, 43, 46, 49]
        ineffectiveness_questions = [7, 15, 20, 29, 32, 33, 44]
        perfectionism_questions = [10, 22, 28, 34, 40, 50]
        interpersonal_distrust_questions = [11, 13, 17, 23, 27, 42, 45]
        interoceptive_incompetence_questions = [5, 16, 19, 26, 31, 35, 38, 39, 47]

        for question in FoodbehaviorTestQuestion.objects.all():
            user_choice_id = request.POST.get(f'question_{question.id}')
            if user_choice_id:
                user_choice = FoodbehaviorTestChoice.objects.get(id=user_choice_id)
                if question.id in thinness_striving_questions:
                    thinness_striving_score += user_choice.points
                elif question.id in bulimia_questions:
                    bulimia_score += user_choice.points
                elif question.id in body_dissatisfaction_questions:
                    body_dissatisfaction_score += user_choice.points
                elif question.id in ineffectiveness_questions:
                    ineffectiveness_score += user_choice.points
                elif question.id in perfectionism_questions:
                    perfectionism_score += user_choice.points
                elif question.id in interpersonal_distrust_questions:
                    interpersonal_distrust_score += user_choice.points
                elif question.id in interoceptive_incompetence_questions:
                    interoceptive_incompetence_score += user_choice.points

        # Вычисляем стенайны для каждой категории
        thinness_striving_stenain = calculate_stenain(thinness_striving_score, {
            (1, 2): 5,
            (3, 5): 6,
            (6, 8): 7,
            (9, 11): 8,
            (12, float('inf')): 9,
        })
        bulimia_stenain = calculate_stenain(bulimia_score, {
            (1, 2): 6,
            (3, 6): 7,
            (6, 8): 7,
            (7, 13): 8,
            (14, float('inf')): 9,
        })
        body_dissatisfaction_stenain = calculate_stenain(body_dissatisfaction_score, {
            1: 4,
            (2, 4): 5,
            (5, 7): 6,
            (8, 12): 7,
            (13, 18): 8,
            (19, float('inf')): 9,
        })

        ineffectiveness_stenain = calculate_stenain(ineffectiveness_score, {
            (1, 2): 5,
            (3, 4): 6,
            (5, 7): 7,
            (8, 9): 8,
            (10, float('inf')): 9,
        })

        perfectionism_stenain = calculate_stenain(perfectionism_score, {
            (1, 2): 3,
            3: 4,
            (4, 5): 5,
            (6, 8): 6,
            (9, 10): 7,
            (11, 12): 8,
            (13, float('inf')): 9,
        })

        interpersonal_distrust_stenain = calculate_stenain(interpersonal_distrust_score, {
            1: 4,
            2: 5,
            (3, 4): 6,
            (5, 7): 7,
            (8, 10): 8,
            (11, float('inf')): 9,
        })

        interoceptive_incompetence_stenain = calculate_stenain(interoceptive_incompetence_score, {
            1: 5,
            (2, 4): 6,
            (5, 8): 7,
            (9, 11): 8,
            (12, float('inf')): 9,
        })
        result_message = foodbehavior_get_result_message()

        if not request.user.is_authenticated:
            request.session['foodbehavior_test_result'] = {
                'thinness_striving_score': thinness_striving_score,
                'thinness_striving_stenain': thinness_striving_stenain,
                'bulimia_score': bulimia_score,
                'bulimia_stenain': bulimia_stenain,
                'body_dissatisfaction_score': body_dissatisfaction_score,
                'body_dissatisfaction_stenain': body_dissatisfaction_stenain,
                'ineffectiveness_score': ineffectiveness_score,
                'ineffectiveness_stenain': ineffectiveness_stenain,
                'perfectionism_score': perfectionism_score,
                'perfectionism_stenain': perfectionism_stenain,
                'interpersonal_distrust_score': interpersonal_distrust_score,
                'interpersonal_distrust_stenain': interpersonal_distrust_stenain,
                'interoceptive_incompetence_score': interoceptive_incompetence_score,
                'interoceptive_incompetence_stenain': interoceptive_incompetence_stenain,
                'result_message': result_message
            }

            return render(request, 'PsichologyTest/FoodBehavior/foodbehavior_offer_save_results.html', {
                'thinness_striving_score': thinness_striving_score,
                'thinness_striving_stenain': thinness_striving_stenain,
                'bulimia_score': bulimia_score,
                'bulimia_stenain': bulimia_stenain,
                'body_dissatisfaction_score': body_dissatisfaction_score,
                'body_dissatisfaction_stenain': body_dissatisfaction_stenain,
                'ineffectiveness_score': ineffectiveness_score,
                'ineffectiveness_stenain': ineffectiveness_stenain,
                'perfectionism_score': perfectionism_score,
                'perfectionism_stenain': perfectionism_stenain,
                'iinterpersonal_distrust_score': interpersonal_distrust_score,
                'interpersonal_distrust_stenain': interpersonal_distrust_stenain,
                'interoceptive_incompetence_score': interoceptive_incompetence_score,
                'interoceptive_incompetence_stenain': interoceptive_incompetence_stenain,
                'result_message': result_message
            })

        # Если пользователь авторизован, сохраняем результаты в базе данных
        FoodbehaviorTestResult.objects.create(
            user=request.user,
            thinness_striving_score=thinness_striving_score,
            thinness_striving_stenain=thinness_striving_stenain,
            bulimia_score=bulimia_score,
            bulimia_stenain=bulimia_stenain,
            body_dissatisfaction_score=body_dissatisfaction_score,
            body_dissatisfaction_stenain=body_dissatisfaction_stenain,
            ineffectiveness_score=ineffectiveness_score,
            ineffectiveness_stenain=ineffectiveness_stenain,
            perfectionism_score=perfectionism_score,
            perfectionism_stenain=perfectionism_stenain,
            interpersonal_distrust_score=interpersonal_distrust_score,
            interpersonal_distrust_stenain=interpersonal_distrust_stenain,
            interoceptive_incompetence_score=interoceptive_incompetence_score,
            interoceptive_incompetence_stenain=interoceptive_incompetence_stenain
        )
        return render(request, 'PsichologyTest/FoodBehavior/foodbehavior_test_results.html', {
            'thinness_striving_score': thinness_striving_score,
            'thinness_striving_stenain': thinness_striving_stenain,
            'bulimia_score': bulimia_score,
            'bulimia_stenain': bulimia_stenain,
            'body_dissatisfaction_score': body_dissatisfaction_score,
            'body_dissatisfaction_stenain': body_dissatisfaction_stenain,
            'ineffectiveness_score': ineffectiveness_score,
            'ineffectiveness_stenain': ineffectiveness_stenain,
            'perfectionism_score': perfectionism_score,
            'perfectionism_stenain': perfectionism_stenain,
            'iinterpersonal_distrust_score': interpersonal_distrust_score,
            'interpersonal_distrust_stenain': interpersonal_distrust_stenain,
            'interoceptive_incompetence_score': interoceptive_incompetence_score,
            'interoceptive_incompetence_stenain': interoceptive_incompetence_stenain,
            'result_message': result_message
        })

    questions = FoodbehaviorTestQuestion.objects.all()
    return render(request, 'PsichologyTest/FoodBehavior/foodbehavior_test.html', {'questions': questions})


def offer_save_result(request):
    if request.method == 'POST':
        save_result_choice = request.POST.get('save_result_choice')

        if save_result_choice == 'yes':
            pass # Отрабатывает скрипт вход в аккаунт или регистрация
        if save_result_choice == 'no':
            # Если пользователь отказывается, перенаправляем на главную страницу
            return redirect('home')
        elif save_result_choice == 'send_email':
            # Если пользователь хочет отправить результаты на электронную почту, перенаправляем на страницу ввода адреса
            return redirect('enter_email')

    return render(request, 'PsichologyTest/BeckDepression/offer_save_result.html')

def anxiety_offer_save_result(request):
    if request.method == 'POST':
        save_result_choice = request.POST.get('save_result_choice')

        if save_result_choice == 'yes':
            pass # Отрабатывает скрипт вход в аккаунт или регистрация
        elif save_result_choice == 'no':
            # Если пользователь отказывается, перенаправляем на главную страницу
            return redirect('home')
        elif save_result_choice == 'send_email':
            # Если пользователь хочет отправить результаты на электронную почту, перенаправляем на страницу ввода адреса
            return redirect('anxiety_enter_email')

    return render(request, 'PsichologyTest/BeckAnxiety/anxiety_offer_save_result.html')


def impulsivity_offer_save_result(request):
    if request.method == 'POST':
        save_result_choice = request.POST.get('save_result_choice')

        if save_result_choice == 'yes':
            pass  # Отрабатывает скрипт вход в аккаунт или регистрация
        elif save_result_choice == 'no':
            # Если пользователь отказывается, перенаправляем на главную страницу
            return redirect('home')
        elif save_result_choice == 'send_email':
            # Если пользователь хочет отправить результаты на электронную почту, перенаправляем на страницу ввода адреса
            return redirect('impulsivity_enter_email')

    return render(request, 'PsichologyTest/Impulsivity/impulsivity_offer_save_result.html')

def selfcompassion_offer_save_result(request):
    if request.method == 'POST':
        save_result_choice = request.POST.get('save_result_choice')

        if save_result_choice == 'yes':
            pass  # Отрабатывает скрипт вхрод в аккаунт или регистрация
        elif save_result_choice == 'no':
            # Если пользователь отказывается, перенаправляем на главную страницу
            return redirect('home')
        elif save_result_choice == 'send_email':
            # Если пользователь хочет отправить результаты на электронную почту, перенаправляем на страницу ввода адреса
            return redirect('selfcompassion_enter_email')

    return render(request, 'PsichologyTest/Selfcompassion/selfcompassion_offer_save_result.html')

def foodbehavior_offer_save_result(request):
    if request.method == 'POST':
        save_result_choice = request.POST.get('save_result_choice')

        if save_result_choice == 'yes':
            pass  # Отрабатывает скрипт вход в аккаунт или регистрация
        elif save_result_choice == 'no':
            # Если пользователь отказывается, перенаправляем на главную страницу
            return redirect('home')
        elif save_result_choice == 'send_email':
            # Если пользователь хочет отправить результаты на электронную почту, перенаправляем на страницу ввода адреса
            return redirect('foodbehavior_enter_email')

    return render(request, 'PsichologyTest/FoodBehavior/foodbehavior_offer_save_result.html')

def get_result_message(score):
    if score <= 9:
        return "Отсутствие депрессивных симптомов."
    elif 10 <= score <= 18:
        return "Легкая депрессия, астено-субдепрессивная симптоматика, м.б. у соматических больных или невротический уровень."
    elif 19 <= score <= 29:
        return "Умеренная депрессия, критический уровень."
    elif 30 <= score <= 63:
        return "Явно выраженная депрессивная симптоматика, не исключена эндогенность."
    else:
        return "Некорректные баллы для оценки."

def anxiety_get_result_message(score):
    if score <= 21:
        return "Незначительный уровень тревоги."
    elif 22 <= score <= 35:
        return "Cредняя выраженность тревоги."
    elif 36 <= score <= 63:
        return "Очень высокий уровень тревоги."
    else:
        return "Некорректные баллы для оценки."

def impulsivity_get_result_message(score):
    if 70 <= score <= 75:
        return "Патологическая импульсивность."
    elif score > 75:
        return "Cерьезные расстройства контроля над импульсивностью."
    else:
        return "Низкая степень импульсивности."

def selfcompassion_get_result_message(score):
    if 0 <= score < 2.5:
        return "Низкий балл."
    elif 2.5 <= score < 3.5:
        return "Cредний балл."
    elif 3.5 <= score <= 5:
        return "Высокий балл."
    else:
        return "Некорректные баллы для оценки."

def foodbehavior_get_result_message():
    return 'За расшифровкой результатов теста обратитесь к психологу'


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Проверяем, есть ли результаты теста в сессии
            if 'test_result' in request.session:
                test_result_data = request.session['test_result']
                TestResult.objects.create(user=user, score=test_result_data['score'],
                                          result_message=test_result_data['result_message'])

            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'PsichologyTest/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'test_result' in request.session:
                    test_result_data = request.session['test_result']
                    TestResult.objects.create(user=user, score=test_result_data['score'], result_message=test_result_data['result_message'])
                    # Используем временную переменную для сообщения
                    success_message = 'Результат успешно сохранен!'
                    messages.success(request, success_message)
                    del request.session['test_result']
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль. Попробуйте снова.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль. Попробуйте снова.')
    else:
        form = AuthenticationForm()
    return render(request, 'PsichologyTest/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def view_results(request):
    # Получаем результаты теста для текущего пользователя
    test_results = TestResult.objects.filter(user=request.user).order_by('date_completed')

    # Получаем данные для построения графика
    dates = [result.date_completed.strftime('%d-%m-%Y') if result.date_completed else 'N/A' for result in test_results]
    scores = [result.score for result in test_results]

    # Создаем массив индексов для баров
    bar_width = 0.4
    x = np.arange(len(dates))

    # Строим гистограмму
    fig, ax = plt.subplots()
    bars = ax.bar(x, scores, color='#3CB371', width=bar_width)

    plt.title('')
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(x, dates, rotation='horizontal')

    # Добавляем метки с целыми баллами внутри столбцов
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height / 2, str(int(score)),
                ha='center', va='center', fontsize=10, color='black')

    # Убираем линии справа и сверху
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('gray')

    # Устанавливаем размер шрифта для оси X
    ax.tick_params(axis='x', labelsize=8)

    # Сохраняем график в байтовом объекте с прозрачностью
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', transparent=True)
    plt.close()

    # Кодируем изображение в base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Отправляем изображение и результаты в шаблон
    return render(request, 'PsichologyTest/BeckDepression/view_results.html',
                  {'test_results': test_results, 'image_base64': image_base64})

def anxiety_view_results(request):
    # Получаем результаты теста для текущего пользователя
    test_results = AnxietyTestResult.objects.filter(user=request.user).order_by('date_completed')

    # Получаем данные для построения графика
    dates = [result.date_completed.strftime('%d-%m-%Y') if result.date_completed else 'N/A' for result in test_results]
    scores = [result.score for result in test_results]

    # Создаем массив индексов для баров
    bar_width = 0.4
    x = np.arange(len(dates))

    # Строим гистограмму
    fig, ax = plt.subplots()
    bars = ax.bar(x, scores, color='#3CB371', width=bar_width)

    plt.title('')
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(x, dates, rotation='horizontal')

    # Добавляем метки с целыми баллами внутри столбцов
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height / 2, str(int(score)),
                ha='center', va='center', fontsize=10, color='black')

    # Убираем линии справа и сверху
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('gray')

    # Устанавливаем размер шрифта для оси X
    ax.tick_params(axis='x', labelsize=8)

    # Сохраняем график в байтовом объекте
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', transparent=True)
    plt.close()

    # Кодируем изображение в base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Отправляем изображение и результаты в шаблон
    return render(request, 'PsichologyTest/BeckAnxiety/anxiety_view_results.html',
                  {'test_results': test_results, 'image_base64': image_base64})


def impulsivity_view_results(request):
    # Получаем результаты теста для текущего пользователя
    test_results = ImpulsivityTestResult.objects.filter(user=request.user).order_by('date_completed')

    # Получаем данные для построения графика
    dates = [result.date_completed.strftime('%d-%m-%Y') if result.date_completed else 'N/A' for result in test_results]
    scores = [result.score for result in test_results]

    # Создаем массив индексов для баров
    bar_width = 0.4
    x = np.arange(len(dates))

    # Строим гистограмму
    fig, ax = plt.subplots()
    bars = ax.bar(x, scores, color='#3CB371', width=bar_width)

    plt.title('')
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(x, dates, rotation='horizontal')

    # Добавляем метки с целыми баллами внутри столбцов
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height / 2, str(int(score)),
                ha='center', va='center', fontsize=10, color='black')

    # Убираем линии справа и сверху
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('gray')

    # Устанавливаем размер шрифта для оси X
    ax.tick_params(axis='x', labelsize=8)

    # Сохраняем график в байтовом объекте
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', transparent=True)
    plt.close()

    # Кодируем изображение в base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Отправляем изображение и результаты в шаблон
    return render(request, 'PsichologyTest/Impulsivity/impulsivity_view_results.html',
                  {'test_results': test_results, 'image_base64': image_base64})


def selfcompassion_view_results(request):
    # Получаем результаты теста для текущего пользователя
    test_results = SelfcompassionTestResult.objects.filter(user=request.user).order_by('date_completed')

    # Получаем данные для построения графика
    dates = [result.date_completed.strftime('%d-%m-%Y') if result.date_completed else 'N/A' for result in test_results]

    # Используйте соответствующие атрибуты для баллов
    kindness_score = [result.kindness_score for result in test_results]
    self_blame_score = [result.self_blame_score for result in test_results]
    human_commonality_score = [result.human_commonality_score for result in test_results]
    isolation_score = [result.isolation_score for result in test_results]
    mindfulness_score = [result.mindfulness_score for result in test_results]
    overidentification_score = [result.overidentification_score for result in test_results]
    total_score = [result.total_score for result in test_results]

    # Создаем массив индексов для баров
    bar_width = 0.3
    x = np.arange(len(dates))

    # Строим гистограмму
    fig, ax = plt.subplots()

    # Добавляем остальные столбцы
    bars_data = [
        (kindness_score, 'Доброта к себе', '#22c55e'),
        (self_blame_score, 'Самоосуждение', '#ef4444'),
        (human_commonality_score, 'Человеческая общность', '#3b82f6'),
        (isolation_score, 'Изоляция', '#eab308'),
        (mindfulness_score, 'Осознанность', '#a855f7'),
        (overidentification_score, 'Сверхидентификация', '#ec4899'),
        (total_score, 'Общий балл', '#6b7280'),
    ]

    for i, (score, label, color) in enumerate(bars_data):
        bars_list = ax.bar(x + i * bar_width, score, width=bar_width, label=label, color=color)

        # Добавляем метки с целыми баллами внутри столбцов
        for bar, score_value in zip(bars_list, score):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height / 2, str(int(score_value)),
                    ha='center', va='center', fontsize=10, color='black')

    # Убираем линии справа и сверху
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('gray')

    # Устанавливаем размер шрифта для оси X
    ax.tick_params(axis='x', labelsize=8)

    # Сохраняем график в байтовом объекте
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', transparent=True)
    plt.close()

    # Кодируем изображение в base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Отправляем изображение и результаты в шаблон
    return render(request, 'PsichologyTest/Selfcompassion/selfcompassion_view_results.html',
                  {'test_results': test_results, 'image_base64': image_base64})


def foodbehavior_view_results(request):
    # Получаем результаты теста для текущего пользователя
    test_results = FoodbehaviorTestResult.objects.filter(user=request.user).order_by('date_completed')

    # Получаем данные для построения графика
    dates = [result.date_completed.strftime('%d-%m-%Y') if result.date_completed else 'N/A' for result in test_results]

    # Используйте соответствующие атрибуты для баллов
    thinness_striving_stenain = [result.thinness_striving_stenain for result in test_results]
    bulimia_stenain = [result.bulimia_stenain for result in test_results]
    body_dissatisfaction_stenain = [result.body_dissatisfaction_stenain for result in test_results]
    ineffectiveness_stenain = [result.ineffectiveness_stenain for result in test_results]
    perfectionism_stenain = [result.perfectionism_stenain for result in test_results]
    interpersonal_distrust_stenain = [result.interpersonal_distrust_stenain for result in test_results]
    interoceptive_incompetence_stenain = [result.interoceptive_incompetence_stenain for result in test_results]

    # Создаем массив индексов для баров
    bar_width = 0.3
    x = np.arange(len(dates))

    # Строим гистограмму
    fig, ax = plt.subplots()

    # Добавляем остальные столбцы
    bars_data = [
        (thinness_striving_stenain, 'Стремление к худобе', '#3CB371'),
        (bulimia_stenain, 'Булимия', '#FF6347'),
        (body_dissatisfaction_stenain, 'Неудовлетворенность телом', '#1E90FF'),
        (ineffectiveness_stenain, 'Неэффективность', '#FFD700'),
        (perfectionism_stenain, 'Перфекционизм', '#8A2BE2'),
        (interpersonal_distrust_stenain, 'Недоверие в межличностных отношениях', '#00CED1'),
        (interoceptive_incompetence_stenain, 'Интероцептивная некомпетентность', 'gray'),
    ]

    for i, (stenain, label, color) in enumerate(bars_data):
        bars_list = ax.bar(x + i * bar_width, stenain, width=bar_width, label=label, color=color)

        # Добавляем метки с целыми баллами внутри столбцов
        for bar, stenain_value in zip(bars_list, stenain):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height / 2, str(int(stenain_value)),
                    ha='center', va='center', fontsize=10, color='black')

    # Убираем линии
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('gray')

    # Устанавливаем размер шрифта для оси X
    ax.tick_params(axis='x', labelsize=8)

    # Сохраняем график в байтовом объекте
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', transparent=True)
    plt.close()

    # Кодируем изображение в base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Отправляем изображение и результаты в шаблон
    return render(request, 'PsichologyTest/FoodBehavior/foodbehavior_view_results.html',
                  {'test_results': test_results, 'image_base64': image_base64})


def enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                send_email(email, request.user, request.session['test_result']['score'], request.session['test_result']['result_message'])
                del request.session['test_result']
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect('enter_email')
            except Exception as e:
                print(e)  # Выводим ошибку в консоль для отладки
                messages.error(request, 'Ошибка отправки письма. Пожалуйста, попробуйте еще раз.')
                return redirect('enter_email')

    return render(request, 'PsichologyTest/BeckDepression/enter_email.html')

def anxiety_enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                send_email(email, request.user, request.session['test_result']['score'], request.session['test_result']['result_message'])
                del request.session['test_result']
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect('anxiety_enter_email')
            except Exception as e:
                print(e)  # Выводим ошибку в консоль для отладки
                messages.error(request, 'Ошибка отправки письма. Пожалуйста, попробуйте еще раз.')
                return redirect('anxiety_enter_email')

    return render(request, 'PsichologyTest/BeckAnxiety/anxiety_enter_email.html')

def impulsivity_enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                send_email(email, request.user, request.session['test_result']['score'], request.session['test_result']['result_message'])
                del request.session['test_result']
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect('impulsivity_enter_email')
            except Exception as e:
                print(e)  # Выводим ошибку в консоль для отладки
                messages.error(request, 'Ошибка отправки письма. Пожалуйста, попробуйте еще раз.')
                return redirect('impulsivity_enter_email')

    return render(request, 'PsichologyTest/Impulsivity/impulsivity_enter_email.html')

def selfcompassion_enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                result = request.session['selfcompassion_test_result']
                scores = {
                    'kindness_average': result['kindness_average'],
                    'self_blame_average': result['self_blame_average'],
                    'human_commonality_average': result['human_commonality_average'],
                    'isolation_average': result['isolation_average'],
                    'mindfulness_average': result['mindfulness_average'],
                    'overidentification_average': result['overidentification_average'],
                    'total_score': result['total_score'],
                }
                selfcompassion_send_email(email, request.user, result['result_message'], scores)
                del request.session['selfcompassion_test_result']
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect('selfcompassion_enter_email')
            except Exception as e:
                print(e)  # Выводим ошибку в консоль для отладки
                messages.error(request, 'Ошибка отправки письма. Пожалуйста, попробуйте еще раз.')
                return redirect('selfcompassion_enter_email')

    return render(request, 'PsichologyTest/Selfcompassion/selfcompassion_enter_email.html')
def foodbehavior_enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                result = request.session['foodbehavior_test_result']
                foodbehavior_send_email(email, request.user, result['result_message'], result=result)
                del request.session['foodbehavior_test_result']
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect('foodbehavior_enter_email')
            except Exception as e:
                print(e)  # Выводим ошибку в консоль для отладки
                messages.error(request, 'Ошибка отправки письма. Пожалуйста, попробуйте еще раз.')
                return redirect('foodbehavior_enter_email')
    return render(request, 'PsichologyTest/FoodBehavior/foodbehavior_enter_email.html')


def send_email(email, user, score, result_message):
    subject = 'Результаты теста'
    message = f'Ваш результат: {score}\nСообщение: {result_message}'
    html_message = render_to_string('PsichologyTest/BeckDepression/email_template.html', {'user': user, 'score': score, 'result_message': result_message})
    plain_message = strip_tags(html_message)
    from_email = 'wolfexe@yandex.ru'
    recipient_list = [email]

    # Отправляем электронное письмо
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

def anxiety_send_email(email, user, score, result_message):
    subject = 'Результаты теста'
    message = f'Ваш результат: {score}\nСообщение: {result_message}'
    html_message = render_to_string('PsichologyTest/BeckAnxiety/anxiety_email_template.html', {'user': user, 'score': score, 'result_message': result_message})
    plain_message = strip_tags(html_message)
    from_email = 'wolfexe@yandex.ru'
    recipient_list = [email]

    # Отправляем электронное письмо
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

def impulsivity_send_email(email, user, score, result_message):
    subject = 'Результаты теста'
    message = f'Ваш результат: {score}\nСообщение: {result_message}'
    html_message = render_to_string('PsichologyTest/Impulsivity/impulsivity_email_template.html', {'user': user, 'score': score, 'result_message': result_message,})
    plain_message = strip_tags(html_message)
    from_email = 'wolfexe@yandex.ru'
    recipient_list = [email]

    # Отправляем электронное письмо
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

def selfcompassion_send_email(email, user, result_message, scores):
    subject = 'Результаты теста'
    html_message = render_to_string('PsichologyTest/Selfcompassion/selfcompassion_email_template.html', {
        'user': user,
        'result_message': result_message,
        'scores': scores  # Передаем оценки в виде словаря
    })
    plain_message = strip_tags(html_message)
    from_email = 'wolfexe@yandex.ru'
    recipient_list = [email]

    # Отправляем электронное письмо
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

def foodbehavior_send_email(email, user, result_message, result):
    subject = 'Результаты теста'
    result_message = f'Ваш результат: {result_message}'
    html_message = render_to_string('PsichologyTest/FoodBehavior/foodbehavior_email_template.html', {'user': user, 'result_message': result_message, 'result': result})
    plain_message = strip_tags(html_message)
    from_email = 'wolfexe@yandex.ru'
    recipient_list = [email]

    # Отправляем электронное письмо
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Введите адрес электронной почты')
            return render(request, 'PsichologyTest/PasswordReset/password_reset_form.html')

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким адресом электронной почты не найден.')
            return render(request, 'PsichologyTest/PasswordReset/password_reset_form.html')

        # Генерация токена для сброса пароля
        token = default_token_generator.make_token(user)

        # Формирование URL для сброса пароля
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"http://{request.get_host()}/reset/{uidb64}/{token}/"

        # Текст сообщения с ссылкой на сброс пароля
        message = f'Ваш запрос на изменение пароля был получен. Пройдите по ссылке {reset_url} для сброса пароля.'

        # Отправка письма с инструкциями по сбросу пароля
        subject = 'Инструкция по сбросу пароля'
        from_email = 'Wolfexe@yandex.ru'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return render(request, 'PsichologyTest/PasswordReset/password_reset_done.html')

    return render(request, 'PsichologyTest/PasswordReset/password_reset_form.html')