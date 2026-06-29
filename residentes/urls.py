from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("residentes/", views.residentes, name="residentes"),
    path("residentes/nuevo/", views.nuevo_residente, name="nuevo_residente"),
    path("residentes/editar/<int:id>/", views.editar_residente, name="editar_residente"),
    path("residentes/eliminar/<int:id>/", views.eliminar_residente, name="eliminar_residente"),

    path("viviendas/", views.viviendas, name="viviendas"),
    path("viviendas/nueva/", views.nueva_vivienda, name="nueva_vivienda"),
    path("viviendas/editar/<int:id>/", views.editar_vivienda, name="editar_vivienda"),
    path("viviendas/eliminar/<int:id>/", views.eliminar_vivienda, name="eliminar_vivienda"),

   path("visitas/", views.visitas, name="visitas"),
   path("visitas/nueva/", views.nueva_visita, name="nueva_visita"),
   path("visitas/editar/<int:id>/", views.editar_visita, name="editar_visita"),
   path("visitas/eliminar/<int:id>/", views.eliminar_visita, name="eliminar_visita"),
   path("reportes/", views.reportes, name="reportes"),
]