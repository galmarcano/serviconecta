from django.urls import path
from .views import v_list_ent, v_create_ent, v_delete_ent, v_update_ent
from .views import v_list_prod, v_create_prod, v_update_prod, v_delete_prod
from .views import v_support, v_logout, v_login, v_home, v_detail_ent
from .views import v_registro_usuario #probando para registro de usuarios
from .views import v_datos_usuario,v_mis_emprendimientos, v_mis_productos
from .views import v_mi_cuenta_det_emprend, v_mi_cuenta_create_prod, v_mi_cuenta_act_emprend, v_mi_cuenta_delete_emprend
from .views import v_mi_cuenta_delete_prod #para mi cuenta

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
    path('registro/', v_registro_usuario, name='registro_usuario'),

    #para mi cuenta:
    path('datos_usuario/', v_datos_usuario, name="datos_usuario"),
    path('mis_emprendimientos/', v_mis_emprendimientos, name="mis_emprendimientos"),
    path('mis_productos/', v_mis_productos, name="mis_productos"),
    path('mi_cuenta_det_emprend/<int:emprendimiento_id>/', v_mi_cuenta_det_emprend, name='mi_cuenta_det_emprend'),
    path('mi_cuenta_create_prod/', v_mi_cuenta_create_prod, name="mi_cuenta_create_prod"),
    path('mi_cuenta_act_emprend/<int:emprendimiento_id>/', v_mi_cuenta_act_emprend, name="mi_cuenta_act_emprend"),
    path('mi_cuenta_delete_emprend/<int:emprendimiento_id>/', v_mi_cuenta_delete_emprend, name="mi_cuenta_delete_emprend"),
    path('mi_cuenta_delete_prod/<int:emprendimiento_id>/<int:product_id>/', v_mi_cuenta_delete_prod, name="mi_cuenta_delete_prod"),


]
