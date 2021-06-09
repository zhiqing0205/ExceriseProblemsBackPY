from django.urls import path,include
from one import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(prefix="viewsets", viewset=views.ProblemViewSet)

urlpatterns = [
    # Function Based View
    path("problem/list/" , views.problem_list ,  name="test-list"),
    path("problem/detail/<int:id>" , views.problem_detail ,  name="test-detail"),
    path("problem/" , views.problem_type ,  name="test-type"),

    # Class Based View
    path("cproblem/list/", views.ProblemList.as_view(), name="test-list"),
    path("cproblem/detail/<int:id>", views.ProblemDetail.as_view(), name="test-detail"),

    # Generic Class Based View
    path("gproblem/list/", views.GProblemList.as_view(), name="test-list"),
    path("gproblem/detail/<int:id>", views.GProblemDetail.as_view(), name="test-detail"),

    # DRF viewsets
    path("viewsets/", views.ProblemViewSet.as_view(
        {"get": "list", "post": "create"}
    ), name="viewsets-list"),
    path("viewsets/<int:pk>", views.ProblemViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    ), name="viewsets-detail"),

    path("" , include(router.urls))
]