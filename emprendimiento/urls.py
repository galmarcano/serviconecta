from django.urls import path
from .views import v_list_ent, v_create_ent, v_delete_ent, v_update_ent
from .views import v_list_prod, v_create_prod, v_update_prod, v_delete_prod

urlpatterns = [
    path('', v_list_ent),
    path('create', v_create_ent),
    path('update/<int:emprendimiento_id>/', v_update_ent),
    path('delete/<int:emprendimiento_id>/', v_delete_ent),
    path('list_prod', v_list_prod),
    path('create_prod/<int:id_emprendimiento>/', v_create_prod),
    path('update_prod/<int:emprendimiento_id>/<int:product_id>/', v_update_prod),
    path('delete_prod/<int:emprendimiento_id>/<int:product_id>/', v_delete_prod),
]