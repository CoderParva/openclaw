from django.urls import path
from chat import views

urlpatterns = [
    path('', views.index),
    path('api/chats/', views.chat_list),
    path('api/chats/create/', views.chat_create),
    path('api/chats/<uuid:chat_id>/', views.chat_detail),
    path('api/chats/<uuid:chat_id>/stream/', views.chat_stream),
    path('api/chats/<uuid:chat_id>/export/', views.export_chat),
    path('api/messages/<int:message_id>/pin/', views.pin_message),
]
