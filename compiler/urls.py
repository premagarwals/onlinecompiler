from django.urls import path
from . import views
 
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),

    ## test endpoints
    path('', views.Welcome, name='root'),
    path('gettestcases',views.getTestcases, name='testcases'),
    path('getusers/', views.getUsers, name='users'),
    path('getproblems/',views.getProblems, name='problems'),
    path('jwtdata/', views.decodeJWT, name='JWTdata'),
    path('getsolutions', views.getSolutions, name='solutions'),
    path('ide/', views.coderunner, name='code runner'),
    path('addproblem/', views.addproblem, name='add problem'),
    path('testcode/', views.testcode, name='test your code'),
]