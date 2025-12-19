from django.urls import path
from . import views

app_name = "upload_book_app"

urlpatterns = [
    path("", views.upload_book, name="upload_book"),
    path("my-books/", views.my_books, name="my_books"),
    path("start-quiz/<int:book_id>/", views.start_quiz, name="start_quiz"),
    path("quiz/<int:session_id>/", views.take_quiz, name="take_quiz"),
    path("submit-answer/<int:session_id>/", views.submit_answer, name="submit_answer"),
    path("submit-quiz/<int:session_id>/", views.submit_quiz, name="submit_quiz"),
    path("results/<int:session_id>/", views.quiz_results, name="quiz_results"),
]
