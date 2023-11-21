from django.urls import path
from .views import v_list_ent, v_create_ent, v_delete_ent, v_update_ent
from .views import v_list_prod, v_create_prod, v_update_prod, v_delete_prod
from .views import v_support, v_logout, v_login, v_home, v_detail_ent
from .views import v_select_user, RegistroUsuarioView #probando para registro de usuarios

urlpatterns = [
    path('', v_home, name="home"),
    path('list', v_list_ent, name='list_ent'),
    path('create', v_create_ent, name='create_ent'),
    path('update/<int:emprendimiento_id>/', v_update_ent, name='update_ent'),
    path('delete/<int:emprendimiento_id>/', v_delete_ent, name='delete_ent'),
    path('list_prod', v_list_prod, name='list_prod'),
    path('create_prod/<int:id_emprendimiento>/',
         v_create_prod, name='create_prod'),
    path('update_prod/<int:emprendimiento_id>/<int:product_id>/',
         v_update_prod, name='update_prod'),
    path('delete_prod/<int:emprendimiento_id>/<int:product_id>/',
         v_delete_prod, name='delete_prod'),
    path('support', v_support, name='support'),
    path('cerrar_sesion', v_logout),
    path('iniciar_sesion', v_login, name='iniciar_sesion'),
    path('detalle_emprendimiento/<int:emprendimiento_id>/', v_detail_ent, name='detalle_emprendimiento'),
    
    #probando para registro de usuarios:
    #primero seleccionar tipo de usuario:
    path('select_user/', v_select_user, name='select_user'),
    path('registro/<str:tipo_usuario>/', RegistroUsuarioView.as_view(), name='registro_usuario'),
]
