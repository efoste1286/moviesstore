from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('<int:id>/toggle-heart/', views.toggle_heart, name='movies.toggle_heart'),
    path('petitions/', views.petitions_index, name='movies.petitions_index'),
    path('petitions/create/', views.petitions_create, name='movies.petitions_create'),
    path('petitions/<int:petition_id>/vote-yes/', views.petitions_vote_yes, name='movies.petitions_vote_yes'),
]