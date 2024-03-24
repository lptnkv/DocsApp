from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('note', views.creator_view, name='creator'),
    path('note/<uuid:document_uid>', views.editor_view, name='editor'),
]