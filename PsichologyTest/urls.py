from django.urls import path
from .views import home, test, signup, user_login, user_logout, impulsivity_enter_email,\
anxiety_enter_email, impulsivity_offer_save_result, view_results,impulsivity_view_results,\
impulsivity_test, anxiety_offer_save_result, anxiety_view_results,\
offer_save_result,anxiety_test, enter_email, selfcompassion_test, selfcompassion_enter_email, selfcompassion_offer_save_result, selfcompassion_view_results, foodbehavior_test, foodbehavior_offer_save_result, foodbehavior_enter_email, foodbehavior_view_results
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

base_html_path = os.path.join(BASE_DIR, 'templates', 'base.html')

urlpatterns = [
    path('', home, name='home'),
    path('test/', test, name='test'),
    # path('test_results/', test_results, name='test_results'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('view_results/', view_results, name='view_results'),
    path('offer_save_result/', offer_save_result, name='offer_save_result'),
    path('enter_email/', enter_email, name='enter_email'),
    path('anxiety_test/', anxiety_test, name='anxiety_test'),
    # path('anxiety_test_results', anxiety_test_results, name='anxiety_test_results'),
    path('anxiety_view_results/', anxiety_view_results, name='anxiety_view_results'),
    path('anxiety_offer_save_result/', anxiety_offer_save_result, name='anxiety_offer_save_result'),
    path('anxiety_enter_email/', anxiety_enter_email, name='anxiety_enter_email'),
    path('impulsivity_test/', impulsivity_test, name='impulsivity_test'),
    # path('impulsivity_test_results', impulsivity_test_results, name='impulsivity_test_results'),
    path('impulsivity_view_results/', impulsivity_view_results, name='impulsivity_view_results'),
    path('impulsivity_offer_save_result/', impulsivity_offer_save_result, name='impulsivity_offer_save_result'),
    path('impulsivity_enter_email/', impulsivity_enter_email, name='impulsivity_enter_email'),
    path('selfcompassion_test/', selfcompassion_test, name='selfcompassion_test'),
    path('selfcompassion_view_results/', selfcompassion_view_results, name='selfcompassion_view_results'),
    path('selfcompassion_offer_save_result/', selfcompassion_offer_save_result, name='selfcompassion_offer_save_result'),
    path('selfcompassion_enter_email/', selfcompassion_enter_email, name='selfcompassion_enter_email'),
    path('foodbehavior_test/', foodbehavior_test, name='foodbehavior_test'),
    path('foodbehavior_view_results/', foodbehavior_view_results, name='foodbehavior_view_results'),
    path('foodbehavior_offer_save_result/', foodbehavior_offer_save_result, name='foodbehavior_offer_save_result'),
    path('foodbehavior_enter_email/', foodbehavior_enter_email, name='foodbehavior_enter_email'),
]