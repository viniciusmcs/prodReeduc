"""Core app URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    # Login screen
    path("autenticar/entrar", views.login_view, name="login"),
    # Home/index screen
    path("home/", views.home_view, name="home"),
    # Cadastro add screen
    path("home/cadastro/adicionar", views.cadastro_adicionar_view, name="cadastro-adicionar"),
    # Cadastro list screens
    path("cadastro", views.cadastro_dashboard_view, name="cadastro-dashboard"),
    path("cadastro/perfil/<int:cadastro_id>", views.cadastro_perfil_view, name="cadastro-perfil"),
    path("cadastro/familiares/<int:cadastro_id>", views.cadastro_familiares_view, name="cadastro-familiares"),
    path("cadastro/familiares/<int:familiar_id>/foto", views.familiar_upload_foto_view, name="familiar-upload-foto"),
    path("cadastro/atendimentos/<int:cadastro_id>", views.cadastro_atendimentos_view, name="cadastro-atendimentos"),
    path("cadastro/agendamentos/<int:cadastro_id>", views.cadastro_agendamentos_view, name="cadastro-agendamentos"),
    path("cadastro/familiares/ver/<int:familiar_id>", views.familiar_ver_view, name="familiar-ver"),
    path("cadastro/familiares/editar/<int:familiar_id>", views.familiar_editar_view, name="familiar-editar"),
    path("cadastro/familiares/excluir/<int:familiar_id>", views.familiar_excluir_view, name="familiar-excluir"),
    path("familiares", views.familiares_avulsos_lista_view, name="familiares-avulsos-lista"),
    path("familiares/adicionar", views.familiar_avulso_adicionar_view, name="familiar-avulso-adicionar"),
    path("familiares/<int:familiar_id>/ver", views.familiar_avulso_ver_view, name="familiar-avulso-ver"),
    path("familiares/<int:familiar_id>/editar", views.familiar_avulso_editar_view, name="familiar-avulso-editar"),
    path("familiares/<int:familiar_id>/excluir", views.familiar_avulso_excluir_view, name="familiar-avulso-excluir"),
    path("cadastro/<int:cadastro_id>/foto", views.cadastro_upload_foto_view, name="cadastro-upload-foto"),
    path("anotacoes/editar/", views.anotacoes_editar_view, name="anotacoes-editar"),
    path("home/cadastros", views.cadastro_lista_view, name="cadastro-lista"),
    path("home/cadastros/<str:filtro>", views.cadastro_lista_view, name="cadastro-lista-filtro"),
    path("home/cadastros/<int:cadastro_id>/ver", views.cadastro_detalhe_view, name="cadastro-detalhe"),
    path("home/cadastros/<int:cadastro_id>/editar", views.cadastro_editar_view, name="cadastro-editar"),
    path("home/cadastros/<int:cadastro_id>/excluir", views.cadastro_excluir_view, name="cadastro-excluir"),
    # Atendimento add screen
    path("home/atendimentos", views.atendimentos_dashboard_view, name="atendimentos-dashboard"),
    path("home/atendimentos/adicionar", views.atendimento_adicionar_view, name="atendimento-adicionar"),
    path("atendimentos/adicionar", views.atendimento_adicionar_view),
    path("atendimentos/<int:atendimento_id>/ver", views.atendimento_ver_view, name="atendimento-ver"),
    path("atendimentos/<int:atendimento_id>/editar", views.atendimento_editar_view, name="atendimento-editar"),
    path("atendimentos/<int:atendimento_id>/excluir", views.atendimento_excluir_view, name="atendimento-excluir"),
    path("atendimentos/<int:atendimento_id>/realizar", views.atendimento_realizado_view, name="atendimento-realizar"),
    # Agendamento add screen
    path("agendamentos", views.agendamentos_dashboard_view, name="agendamentos-dashboard"),
    path("agendamentos/buscar", views.api_buscar_cadastros_view, name="api-buscar-cadastros"),
    path("agendamentos/<int:agendamento_id>/ver", views.agendamento_ver_view, name="agendamento-ver"),
    path("agendamentos/<int:agendamento_id>/editar", views.agendamento_editar_view, name="agendamento-editar"),
    path("agendamentos/<int:agendamento_id>/excluir", views.agendamento_excluir_view, name="agendamento-excluir"),
    path("home/agendamentos/adicionar", views.agendamento_adicionar_view, name="agendamento-adicionar"),
    path("agendamentos/adicionar", views.agendamento_adicionar_view),
    # User menu screens
    path("usuario/perfil/<str:username>", views.user_profile_view, name="user-profile"),
    path("usuario/perfil/<str:username>/editar", views.user_profile_update_view, name="user-profile-update"),
    path("usuario/perfil/<str:username>/trocarsenha", views.user_profile_password_view, name="user-profile-password"),
    path("atividades/minhasatividades", views.minhas_atividades_view, name="minhas-atividades"),
    path("sair", views.logout_view, name="logout"),
    # Admin user management
    path("administrar/usuarios", views.admin_users_list_view, name="admin-users-list"),
    path("administrar/adicionarUsuario", views.admin_user_add_view, name="admin-user-add"),
    path("administrar/usuarios/<int:user_id>/detalhes", views.admin_user_detail_view, name="admin-user-detail"),
    path("administrar/usuarios/<int:user_id>/toggle", views.admin_user_toggle_active_view, name="admin-user-toggle"),
    path("administrar/usuarios/<int:user_id>/excluir", views.admin_user_delete_view, name="admin-user-delete"),
    # Relatórios
    path("relatorios", views.relatorios_view, name="relatorios"),
    path("relatorios/pdf", views.relatorios_pdf_view, name="relatorios-pdf"),
    path("relatorios/excel", views.relatorios_excel_view, name="relatorios-excel"),
]
