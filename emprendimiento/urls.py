from django.urls import path
from .views import v_list_ent, v_create_ent, v_delete_ent, v_update_ent
from .views import v_list_prod, v_create_prod, v_update_prod, v_delete_prod
from .views import v_support

urlpatterns = [
    path('', v_list_ent, name='list_ent'),
    path('create', v_create_ent, name='create_ent'),
    path('update/<int:emprendimiento_id>/', v_update_ent, name='update_ent'),
    path('delete/<int:emprendimiento_id>/', v_delete_ent, name='delete_ent'),
    path('list_prod', v_list_prod, name='list_prod'),
    path('create_prod/<int:id_emprendimiento>/', v_create_prod, name='create_prod'),
    path('update_prod/<int:emprendimiento_id>/<int:product_id>/', v_update_prod, name='update_prod'),
    path('delete_prod/<int:emprendimiento_id>/<int:product_id>/', v_delete_prod, name='delete_prod'),
    path('support', v_support, name='support'),
]