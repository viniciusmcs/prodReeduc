"""Tests for the core app."""

from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Agendamento, Atendimento, Cadastro, Familiar
from .views import _report_querysets


class LoginPageTests(TestCase):
    """Smoke tests for the login page."""

    def test_login_page_renders(self):
        """Ensure the login page returns HTTP 200."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)


class ReportFilterTests(TestCase):
    def setUp(self):
        self.matching = Cadastro.objects.create(
            nome="Maria da Silva", data_cadastro=date(2026, 6, 20), status="ativo"
        )
        self.other = Cadastro.objects.create(
            nome="Outra Pessoa", data_cadastro=date(2026, 5, 10), status="arquivado"
        )
        self.matching_relative = Familiar.objects.create(
            nome="Familiar Maria", cadastro=self.matching
        )
        Familiar.objects.create(nome="Familiar Outra", cadastro=self.other)
        Familiar.objects.create(nome="Familiar Avulso")

    def test_filtered_relatives_exclude_nonmatching_and_unlinked_records(self):
        _, familiares, _, _ = _report_querysets({
            "data_inicio": "2026-06-01", "data_fim": "2026-06-30"
        })

        self.assertQuerySetEqual(familiares, [self.matching_relative])

    def test_unfiltered_report_keeps_all_relatives(self):
        _, familiares, _, _ = _report_querysets({})

        self.assertEqual(familiares.count(), 3)

    def test_date_and_name_filter_activity_sections(self):
        matching_atendimento = Atendimento.objects.create(
            nome_pessoa_atendida="Maria da Silva", data_atendimento=date(2026, 6, 25)
        )
        Atendimento.objects.create(
            nome_pessoa_atendida="Maria da Silva", data_atendimento=date(2026, 5, 25)
        )
        matching_agendamento = Agendamento.objects.create(
            nome_atendido="Maria da Silva", data_agendamento=date(2026, 6, 26)
        )
        Agendamento.objects.create(
            nome_atendido="Outra Pessoa", data_agendamento=date(2026, 6, 26)
        )

        _, _, atendimentos, agendamentos = _report_querysets({
            "data_inicio": "2026-06-01",
            "data_fim": "2026-06-30",
            "nome": "Maria",
        })

        self.assertQuerySetEqual(atendimentos, [matching_atendimento])
        self.assertQuerySetEqual(agendamentos, [matching_agendamento])
