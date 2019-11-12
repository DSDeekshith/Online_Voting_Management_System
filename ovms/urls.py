

from django.urls import path


from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('EC_Login/', views.EC_Login, name="EC_Login"),
    path('Add_Employee/', views.AddEmployeeView, name="Add_Employee"),
    path('EC_Login/Add_Voter/', views.AddVoterView, name="Add_Voter"),
    path('EC_Login/Add_Candidate/', views.AddCandidateView, name="Add_Candidate"),
    path('EC_Login/View_Voters/', views.VotersView, name="View_Voters"),
    path('EC_Login/View_Candidates/',
         views.CandidatesView, name="View_Candidates"),
    path('EC_Login/Vote_Login/', views.VoteLoginView, name="Vote_Login"),
    path('EC_Login/Vote/', views.VoteView, name="Vote"),
    path('EC_Login/Results/', views.ResultsView, name="Results"),
    path('base/', views.baseView),
    path('success/', views.success, name="success"),
    # path('voters/',views.voters_list, name='voters_list'),
    # path('add', views.add,  name='add' ),
    # # path('', voters_list),

    # path('<id>/', voters_detail),
]
