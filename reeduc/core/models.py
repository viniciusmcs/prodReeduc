"""Database models for core features.

Keep models as the single source of truth for business data.
"""

from django.conf import settings
from django.utils import timezone
from django.db import models


class Cadastro(models.Model):
    """Cadastro principal (identificação e dados complementares)."""

    STATUS_CHOICES = [
        ("ativo", "Ativo"),
        ("arquivado", "Arquivado"),
    ]

    # --- Dados pessoais ---
    SEXO_BIOLOGICO_CHOICES = [
        ("masculino", "Masculino"),
        ("feminino", "Feminino"),
        ("intersexo", "Intersexo"),
        ("nao_informado", "Prefiro não informar"),
    ]

    IDENTIDADE_GENERO_CHOICES = [
        ("mulher_cis", "Mulher cis"),
        ("homem_cis", "Homem cis"),
        ("mulher_trans", "Mulher trans"),
        ("homem_trans", "Homem trans"),
        ("nao_binario", "Não binário"),
        ("outro", "Outro"),
        ("nao_informado", "Prefiro não informar"),
    ]

    IDENTIDADE_SEXUAL_CHOICES = [
        ("heterossexual", "Heterossexual"),
        ("homossexual", "Homossexual"),
        ("bissexual", "Bissexual"),
        ("assexual", "Assexual"),
        ("outro", "Outro"),
        ("nao_informado", "Prefiro não informar"),
    ]

    RELIGIAO_CHOICES = [
        ("cristao" , "Cristão"),
        ("catolica", "Católica"),
        ("evangelica", "Evangélica"),
        ("espirita", "Espírita"),
        ("umbanda", "Umbanda"),
        ("candomble", "Candomblé"),
        ("outra", "Outra"),
        ("nao_possui", "Não possui"),
    ]

    ETNIA_CHOICES = [
        ("branca", "Branca"),
        ("preta", "Preta"),
        ("parda", "Parda"),
        ("amarela", "Amarela"),
        ("indigena", "Indígena"),
        ("nao_informado", "Prefiro não informar"),
    ]

    ESTADO_CIVIL_CHOICES = [
        ("solteiro", "Solteiro(a)"),
        ("casado", "Casado(a)"),
        ("uniao_estavel", "União estável"),
        ("divorciado", "Divorciado(a)"),
        ("viuvo", "Viúvo(a)"),
        ("nao_informado", "Prefiro não informar"),
    ]

    nome = models.CharField(max_length=255)
    nome_social = models.CharField(max_length=255, blank=True)
    sexo_biologico = models.CharField(max_length=20, choices=SEXO_BIOLOGICO_CHOICES, blank=True)
    identidade_genero = models.CharField(max_length=20, choices=IDENTIDADE_GENERO_CHOICES, blank=True)
    identidade_sexual = models.CharField(max_length=20, choices=IDENTIDADE_SEXUAL_CHOICES, blank=True)
    pessoa_transexual = models.BooleanField(default=False)

    # --- Dados complementares ---
    data_nascimento = models.DateField(null=True, blank=True)
    naturalidade = models.CharField(max_length=120, blank=True)
    data_cadastro = models.DateField(default=timezone.localdate)
    religiao = models.CharField(max_length=20, choices=RELIGIAO_CHOICES, blank=True)
    religiao_desde_quando = models.CharField(max_length=120, blank=True)
    identidade_etnico_racial = models.CharField(max_length=20, choices=ETNIA_CHOICES, blank=True)
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, blank=True)
    nome_mae = models.CharField(max_length=255, blank=True)
    nome_pai = models.CharField(max_length=255, blank=True)

    STATUS_OCUPACIONAL_CHOICES = [
        ("desempregado", "Desempregado"),
        ("sem_informacao", "Sem informação"),
        ("trabalhando_nm_es", "Trabalhando via NM/ES"),
        ("trabalhando_ocupado", "Trabalhando/Ocupado"),
        ("impedido_indisponivel", "Impedido/Indisponível"),
        ("ja_trabalhou_nm_es", "Já trabalhou via NM/ES"),
        ("outro", "Outro"),
    ]

    status_ocupacional = models.CharField(max_length=30, choices=STATUS_OCUPACIONAL_CHOICES, blank=True)

    GRAU_INSTRUCAO_CHOICES = [
        ("nao_informado", "Não informado"),
        ("fundamental_incompleto", "Ensino Fundamental Incompleto"),
        ("fundamental_completo", "Ensino Fundamental Completo"),
        ("medio_incompleto", "Ensino Médio Incompleto"),
        ("medio_completo", "Ensino Médio Completo"),
        ("superior_incompleto", "Ensino Superior Incompleto"),
        ("superior_completo", "Ensino Superior Completo"),
    ]

    grau_instrucao = models.CharField(max_length=30, choices=GRAU_INSTRUCAO_CHOICES, blank=True)
    serie_concluida = models.CharField(max_length=120, blank=True)
    fez_ensino_superior = models.CharField(max_length=3, choices=[("sim", "Sim"), ("nao", "Não")], blank=True)
    curso_superior = models.CharField(max_length=255, blank=True)
    experiencia_escolar = models.TextField(blank=True)
    estuda_atualmente = models.CharField(max_length=3, choices=[("sim", "Sim"), ("nao", "Não")], blank=True)
    horario_turno_estudo = models.CharField(max_length=120, blank=True)

    # --- Documentação apresentada ---
    doc_certidao_nascimento = models.BooleanField(default=False)
    doc_rg = models.BooleanField(default=False)
    doc_cpf = models.BooleanField(default=False)
    doc_ctps = models.BooleanField(default=False)
    doc_titulo_eleitor = models.BooleanField(default=False)
    doc_cert_escolaridade = models.BooleanField(default=False)
    doc_documento_militar = models.BooleanField(default=False)
    doc_cnh = models.BooleanField(default=False)

    # --- Documentação ausente ---
    doc_ausente_certidao_1 = models.BooleanField(default=False)
    doc_ausente_certidao_2 = models.BooleanField(default=False)
    doc_ausente_rg_1 = models.BooleanField(default=False)
    doc_ausente_rg_2 = models.BooleanField(default=False)
    doc_ausente_cpf_1 = models.BooleanField(default=False)
    doc_ausente_cpf_2 = models.BooleanField(default=False)
    doc_ausente_ctps_1 = models.BooleanField(default=False)
    doc_ausente_ctps_2 = models.BooleanField(default=False)
    doc_ausente_titulo_1 = models.BooleanField(default=False)
    doc_ausente_titulo_2 = models.BooleanField(default=False)
    doc_ausente_documento_militar_1 = models.BooleanField(default=False)
    doc_ausente_documento_militar_2 = models.BooleanField(default=False)

    # --- Dados de documentos ---
    cpf_numero = models.CharField(max_length=20, blank=True)
    rg_numero = models.CharField(max_length=20, blank=True)
    titulo_eleitor_numero = models.CharField(max_length=30, blank=True)
    numero_processo_pep = models.CharField(max_length=30, blank=True)

    CNH_CATEGORIA_CHOICES = [
        ("acc", "ACC"),
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
        ("d", "D"),
        ("e", "E"),
    ]
    cnh_categoria = models.CharField(max_length=3, choices=CNH_CATEGORIA_CHOICES, blank=True)

    # --- Informações de atendimento ---
    PROCEDENCIA_CHOICES = [
        ("unidade_prisional", "Unidade prisional"),
        ("encaminhamento", "Encaminhamento externo"),
        ("busca_espontanea", "Busca espontânea"),
        ("outro", "Outro"),
    ]
    procedencia = models.CharField(max_length=30, choices=PROCEDENCIA_CHOICES, blank=True)
    procedencia_outro = models.CharField(max_length=120, blank=True)
    motivo_procura = models.TextField(blank=True)
    orientado_escritorio_social = models.BooleanField(default=False)

    ENCAMINHAMENTO_CHOICES = [
        ("politica_publica", "Política Pública"),
        ("mercado_trabalho", "Mercado de Trabalho"),
        ("cursos_capacitacoes", "Cursos e Capacitações"),
    ]
    encaminhamento = models.CharField(max_length=30, choices=ENCAMINHAMENTO_CHOICES, blank=True)
    encaminhamento_detalhe = models.TextField(blank=True)

    # --- Endereço e contatos ---
    endereco = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=120, blank=True)
    cidade = models.CharField(max_length=120, blank=True)
    estado_uf = models.CharField(max_length=2, blank=True)
    ponto_referencia = models.CharField(max_length=255, blank=True)

    ZONA_CIDADE_CHOICES = [
        ("norte", "Norte"),
        ("sul", "Sul"),
        ("leste", "Leste"),
        ("oeste", "Oeste"),
        ("rural", "Rural"),
    ]
    zona_cidade = models.CharField(max_length=10, choices=ZONA_CIDADE_CHOICES, blank=True)

    telefone_numero = models.CharField(max_length=20, blank=True)
    telefone_contato = models.CharField(max_length=120, blank=True)
    email_contato = models.EmailField(blank=True)

    # Status do cadastro (ativo/arquivado)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ativo")
    
    # Foto do cadastro
    foto = models.ImageField(upload_to='cadastros/', null=True, blank=True)

    def __str__(self) -> str:
        """Readable representation for admin and logs."""
        return self.nome


class Familiar(models.Model):
    """Cadastro de familiares vinculados ao egresso."""
    ENCAMINHAMENTO_CHOICES = Cadastro.ENCAMINHAMENTO_CHOICES

    cadastro = models.ForeignKey(
        Cadastro,
        on_delete=models.CASCADE,
        related_name="familiares",
        null=True,
        blank=True,
    )
    nome = models.CharField(max_length=255)
    nome_social = models.CharField(max_length=255, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo_biologico = models.CharField(max_length=20, choices=Cadastro.SEXO_BIOLOGICO_CHOICES, blank=True)
    identidade_etnico_racial = models.CharField(max_length=20, choices=Cadastro.ETNIA_CHOICES, blank=True)
    pessoa_transexual = models.BooleanField(default=False)
    cpf_numero = models.CharField(max_length=20, blank=True)
    nis_numero = models.CharField(max_length=30, blank=True)
    documentos_possui = models.TextField(blank=True)
    documentos_ausentes = models.TextField(blank=True)
    parentesco = models.CharField(max_length=120, blank=True)
    perfil_referencia_egresso = models.BooleanField(default=False)
    perfil_referencia_pre_egresso = models.BooleanField(default=False)
    nome_interno_referencia = models.CharField(max_length=255, blank=True)
    encaminhamento = models.CharField(max_length=30, choices=ENCAMINHAMENTO_CHOICES, blank=True)
    encaminhamento_detalhe = models.TextField(blank=True)
    bairro = models.CharField(max_length=120, blank=True)
    telefone_numero = models.CharField(max_length=20, blank=True)
    telefone_contato = models.CharField(max_length=120, blank=True)
    telefone_observacao = models.CharField(max_length=255, blank=True)
    email_contato = models.EmailField(blank=True)
    foto = models.ImageField(upload_to="familiares/", null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Familiar - {self.nome}"


class Lembrete(models.Model):
    """Lembrete/anotação vinculada ao cadastro."""

    URGENCIA_CHOICES = [
        ("baixa", "Baixa"),
        ("media", "Média"),
        ("alta", "Alta"),
    ]

    cadastro = models.ForeignKey(
        Cadastro,
        on_delete=models.CASCADE,
        related_name="lembretes",
        null=True,
        blank=True,
    )
    titulo = models.CharField(max_length=255)
    anotacao = models.TextField(blank=True)
    urgencia = models.CharField(max_length=10, choices=URGENCIA_CHOICES, default="media")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lembretes_criados",
    )
    atualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lembretes_atualizados",
    )

    def __str__(self) -> str:
        """Readable representation for admin and logs."""
        return f"Lembrete - {self.titulo}"


class Atendimento(models.Model):
    """Registro de atendimento a egresso ou familiar não cadastrado."""

    LOCAL_ATENDIMENTO_CHOICES = [
        ("escritorio_social", "Escritório Social"),
        ("unidade_prisional", "Unidade Prisional"),
        ("outro", "Outro"),
    ]

    TIPO_ATENDIMENTO_CHOICES = [
        ("presencial", "Presencial"),
        ("online", "On-line"),
        ("grupal", "Grupal"),
        ("outro", "Outro"),
    ]

    PERFIL_PESSOA_CHOICES = [
        ("reeducando", "Egresso"),
        ("familiar", "Familiar"),
        ("nao_cadastrado", "Não cadastrado"),
        ("outro", "Outro"),
    ]

    MOTIVO_PROCURA_CHOICES = [
        ("documentacao", "Documentação"),
        ("trabalho", "Trabalho"),
        ("assistencia", "Assistência social"),
        ("saude", "Saúde"),
        ("outro", "Outro"),
    ]

    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("realizado", "Realizado"),
    ]

    nome_pessoa_atendida = models.CharField(max_length=255)
    data_atendimento = models.DateField()
    local_atendimento = models.CharField(max_length=30, choices=LOCAL_ATENDIMENTO_CHOICES, blank=True)
    tipo_atendimento = models.CharField(max_length=20, choices=TIPO_ATENDIMENTO_CHOICES, blank=True)
    perfil_pessoa_atendida = models.CharField(max_length=20, choices=PERFIL_PESSOA_CHOICES, blank=True)
    motivo_procura = models.CharField(max_length=20, choices=MOTIVO_PROCURA_CHOICES, blank=True)
    objetivo_atendimento = models.CharField(max_length=255, blank=True)
    profissional_responsavel = models.CharField(max_length=120, blank=True)
    outras_pessoas_participantes = models.CharField(max_length=255, blank=True)
    descricao_atendimento = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pendente")

    def __str__(self) -> str:
        """Readable representation for admin and logs."""
        return f"Atendimento - {self.nome_pessoa_atendida}"


class Agendamento(models.Model):
    """Registro de agendamentos do sistema."""

    TIPO_AGENDAMENTO_CHOICES = [
        ("acompanhamento", "Acompanhamento"),
        ("atendimento", "Atendimento"),
        ("cadastro", "Cadastro"),
        ("retorno", "Retorno"),
        ("outro", "Outro"),
    ]

    HORARIO_CHOICES = [
        ("07:00", "7:00"),
        ("07:30", "7:30"),
        ("08:00", "8:00"),
        ("08:30", "8:30"),
        ("09:00", "9:00"),
        ("09:30", "9:30"),
        ("10:00", "10:00"),
        ("10:30", "10:30"),
        ("11:00", "11:00"),
        ("11:30", "11:30"),
        ("12:00", "12:00"),
        ("12:30", "12:30"),
        ("13:00", "13:00"),
        ("13:30", "13:30"),
        ("14:00", "14:00"),
        ("14:30", "14:30"),
        ("15:00", "15:00"),
        ("15:30", "15:30"),
        ("16:00", "16:00"),
    ]

    nome_atendido = models.CharField(max_length=255)
    tipo_agendamento = models.CharField(max_length=20, choices=TIPO_AGENDAMENTO_CHOICES, blank=True)
    data_agendamento = models.DateField()
    horario_atendimento = models.CharField(max_length=5, choices=HORARIO_CHOICES, blank=True)
    observacoes = models.TextField(blank=True)

    def __str__(self) -> str:
        """Readable representation for admin and logs."""
        return f"Agendamento - {self.nome_atendido}"


class UserProfile(models.Model):
    """Perfil de usuário com cargo/função no sistema."""

    CARGO_CHOICES = [
        ("apoio_adm_estagiario", "Apoio Administrativo/Estagiário"),
        ("assistente_tecnico_direito", "Assistente Técnico – Bacharel em Direito"),
        ("assistente_tecnico_pedagogo", "Assistente Técnico – Pedagogo(a)"),
        ("assistente_tecnico_assistente_social", "Assistente Técnico – Assistente Social"),
        ("assistente_tecnico_psicologo", "Assistente Técnico – Psicólogo(a)"),
        ("tj_apoio_adm_estagiario", "TJ - Apoio Administrativo/Estagiário"),
        ("tj_assistente_tecnico_assistente_social", "TJ - Assistente Técnico – Assistente Social"),
        ("tj_assistente_tecnico_psicologo", "TJ - Assistente Técnico – Psicólogo(a)"),
        ("gerencia_administracao", "Gerência/Administração"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cargo_es = models.CharField(max_length=50, choices=CARGO_CHOICES, blank=True)

    def __str__(self) -> str:
        """Readable representation for admin and logs."""
        return f"Perfil - {self.user.username}"
