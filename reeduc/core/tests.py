"""Tests for the core app."""

from datetime import date, datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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
        self.other_relative = Familiar.objects.create(
            nome="Familiar Outra", cadastro=self.other
        )
        self.unlinked_relative = Familiar.objects.create(
            nome="Familiar Avulso", nome_interno_referencia="Egresso Referenciado"
        )

        january = timezone.make_aware(datetime(2026, 1, 15, 12))
        may = timezone.make_aware(datetime(2026, 5, 15, 12))
        Familiar.objects.filter(
            pk__in=[self.matching_relative.pk, self.unlinked_relative.pk]
        ).update(data_criacao=january)
        Familiar.objects.filter(pk=self.other_relative.pk).update(data_criacao=may)

    def test_family_period_uses_its_own_creation_date_and_keeps_unlinked(self):
        _, familiares, _, _ = _report_querysets({
            "data_inicio": "2026-01-01", "data_fim": "2026-01-31"
        })

        self.assertQuerySetEqual(
            familiares,
            [self.unlinked_relative, self.matching_relative],
            ordered=False,
        )

    def test_family_name_searches_familiar_and_referenced_egresso(self):
        _, familiares, _, _ = _report_querysets({"nome": "Referenciado"})

        self.assertQuerySetEqual(familiares, [self.unlinked_relative])

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
