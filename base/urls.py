from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomLoginView,RegisterPage
# Logout doesnot need any views we can directly work with it
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page = 'login'),name='logout'),
    path('register/',RegisterPage.as_view(),name='register'),
    path('',TaskList.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',TaskDelete.as_view(),name='task-delete'),
    # path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]


# For Documentation and refernces Use "https://ccbv.co.uk/"
# https://docs.djangoproject.com/en/5.0/ref/class-based-views/