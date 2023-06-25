from django.urls import path
from . import views

urlpatterns = [
    # Funciones de vistas
    path('', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('files', views.my_files, name='files'),
    path('upload', views.upload),
    path('favorites', views.favorites, name='favorites'),
    path('trash', views.trash_bin, name='trash'),

    # Funciones Logicas
    path('file/<int:page_id>/<int:file_id>', views.load_file_info, name='load_file_info'),
    path('download/<path:path>', views.download_file, name='download_file'),
    path('mark_as_favorite/<int:file_id>/<int:page_id>', views.mark_as_favorite, name='mark_as_favorite'),
    path('mark_as_deleted/<int:file_id>/<int:page_id>', views.mark_as_deleted, name='mark_as_deleted'),
    path('deleted_forever/<int:file_id>', views.delete_forever, name='deleted_forever')
]