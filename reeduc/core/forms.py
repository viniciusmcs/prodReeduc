"""Forms for core app.

Use ModelForms to keep validation close to the model (DRY).
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.conf import settings
import re

from .models import Agendamento, Atendimento, Cadastro, Familiar, Lembrete, SetorJuridico, UserProfile


def _validate_image_upload(uploaded_file):
    """Validate uploaded image by content type, size and binary signature."""
    if not uploaded_file:
        return uploaded_file

    from io import BytesIO
    from PIL import Image, UnidentifiedImageError

    max_size = getattr(settings, "MAX_IMAGE_UPLOAD_SIZE", 5 * 1024 * 1024)
    if uploaded_file.size > max_size:
        raise forms.ValidationError("A imagem excede o limite permitido (5 MB).")

    if uploaded_file.content_type not in {"image/jpeg", "image/png"}:
        raise forms.ValidationError("Envie apenas imagens PNG ou JPEG.")

    try:
        raw = uploaded_file.read()
        image = Image.open(BytesIO(raw))
        image.verify()
        image_format = (image.format or "").upper()
    except (UnidentifiedImageError, OSError, ValueError):
        raise forms.ValidationError("Arquivo de imagem inválido.")
    finally:
        uploaded_file.seek(0)

    if image_format not in {"JPEG", "PNG"}:
        raise forms.ValidationError("Envie apenas imagens PNG ou JPEG.")

    return uploaded_file


def _validate_pdf_upload(uploaded_file):
    """Validate uploaded PDF by extension, content-type and size."""
    if not uploaded_file:
        return uploaded_file

    max_size = 10 * 1024 * 1024
    if uploaded_file.size > max_size:
        raise forms.ValidationError("O arquivo PDF excede o limite permitido (10 MB).")

    file_name = (uploaded_file.name or "").lower()
    if not file_name.endswith(".pdf"):
        raise forms.ValidationError("Envie apenas arquivo no formato PDF.")

    content_type = (uploaded_file.content_type or "").lower()
    valid_types = {"application/pdf", "application/x-pdf"}
    if content_type and content_type not in valid_types:
        raise forms.ValidationError("Envie apenas arquivo no formato PDF.")

    return uploaded_file


class CadastroForm(forms.ModelForm):
    """Form for creating a Cadastro."""

    def __init__(self, *args, **kwargs):
        """Configure widget placeholders and empty labels."""
        super().__init__(*args, **kwargs)
        select_fields = [
            "sexo_biologico",
            "identidade_genero",
            "identidade_sexual",
            "religiao",
            "identidade_etnico_racial",
            "estado_civil",
            "status_ocupacional",
            "grau_instrucao",
            "fez_ensino_superior",
            "estuda_atualmente",
            "procedencia",
            "encaminhamento",
            "zona_cidade",
        ]
        for name in select_fields:
            self.fields[name].empty_label = "Selecione uma opção"

    class Meta:
        model = Cadastro
        fields = [
            # Dados pessoais
            "nome",
            "nome_social",
            "sexo_biologico",
            "identidade_genero",
            "identidade_sexual",
            "pessoa_transexual",
            # Dados complementares
            "data_nascimento",
            "data_cadastro",
            "naturalidade",
            "religiao",
            "religiao_desde_quando",
            "identidade_etnico_racial",
            "estado_civil",
            "nome_mae",
            "nome_pai",
            "status_ocupacional",
            "grau_instrucao",
            "serie_concluida",
            "fez_ensino_superior",
            "curso_superior",
            "experiencia_escolar",
            "estuda_atualmente",
            "horario_turno_estudo",
            # Documentação apresentada
            "doc_certidao_nascimento",
            "doc_rg",
            "doc_cpf",
            "doc_ctps",
            "doc_titulo_eleitor",
            "doc_cert_escolaridade",
            "doc_documento_militar",
            "doc_cnh",
            # Documentação ausente
            "doc_ausente_certidao_1",
            "doc_ausente_certidao_2",
            "doc_ausente_rg_1",
            "doc_ausente_rg_2",
            "doc_ausente_cpf_1",
            "doc_ausente_cpf_2",
            "doc_ausente_ctps_1",
            "doc_ausente_ctps_2",
            "doc_ausente_titulo_1",
            "doc_ausente_titulo_2",
            "doc_ausente_documento_militar_1",
            "doc_ausente_documento_militar_2",
            # Dados de documentos
            "cpf_numero",
            "rg_numero",
            "titulo_eleitor_numero",
            "numero_processo_pep",
            "cnh_categoria",
            # Informações de atendimento
            "procedencia",
            "procedencia_outro",
            "motivo_procura",
            "orientado_escritorio_social",
            "encaminhamento",
            "encaminhamento_detalhe",
            # Endereço e contatos
            "endereco",
            "bairro",
            "cidade",
            "estado_uf",
            "ponto_referencia",
            "zona_cidade",
            "telefone_numero",
            "telefone_contato",
            "email_contato",
            "foto",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
            "data_cadastro": forms.DateInput(attrs={"type": "date"}),
            "motivo_procura": forms.Textarea(attrs={"rows": 3}),
            "encaminhamento_detalhe": forms.Textarea(attrs={"rows": 3}),
            "experiencia_escolar": forms.Textarea(attrs={"rows": 3}),
            "cnh_categoria": forms.RadioSelect,
            "cpf_numero": forms.TextInput(attrs={"maxlength": "14"}),
            "rg_numero": forms.TextInput(attrs={"maxlength": "12"}),
            "titulo_eleitor_numero": forms.TextInput(attrs={"maxlength": "12"}),
            "numero_processo_pep": forms.TextInput(attrs={"maxlength": "30"}),
        }
        help_texts = {
            "sexo_biologico": "Informação para fins estatísticos.",
            "identidade_genero": "Respeita a identidade declarada pela pessoa.",
            "identidade_sexual": "Use conforme autodeclaração.",
            "pessoa_transexual": "Marque se a pessoa se identifica como trans/travesti.",
            "religiao": "Qual a sua religião, de acordo com o seu modo de pensar?",
            "religiao_desde_quando": "Informe o período, se aplicável.",
            "procedencia": "Chegou ao serviço por meio de qual procedência?",
            "procedencia_outro": "Descreva a procedência quando selecionar 'Outro'.",
            "orientado_escritorio_social": "Foi orientado(a) sobre o Escritório Social na Unidade Prisional?",
        }

    def clean(self):
        """Custom validations for conditional fields."""
        cleaned_data = super().clean()

        procedencia = cleaned_data.get("procedencia")
        procedencia_outro = cleaned_data.get("procedencia_outro")
        if procedencia == "outro" and not procedencia_outro:
            self.add_error("procedencia_outro", "Informe a procedência.")

        return cleaned_data



    def clean_foto(self):
        return _validate_image_upload(self.cleaned_data.get("foto"))

class AtendimentoForm(forms.ModelForm):
    """Form for creating an Atendimento."""

    def __init__(self, *args, user=None, **kwargs):
        """Configure widget placeholders, empty labels, and defaults."""
        super().__init__(*args, **kwargs)
        for name in [
            "local_atendimento",
            "tipo_atendimento",
            "perfil_pessoa_atendida",
            "motivo_procura",
        ]:
            self.fields[name].empty_label = "Escolha uma opção"

        if user and not self.instance.pk:
            self.fields["profissional_responsavel"].initial = user.get_username()

        self.fields["profissional_responsavel"].widget.attrs.update(
            {"readonly": "readonly", "aria-readonly": "true"}
        )

    class Meta:
        model = Atendimento
        fields = [
            "nome_pessoa_atendida",
            "data_atendimento",
            "local_atendimento",
            "tipo_atendimento",
            "perfil_pessoa_atendida",
            "motivo_procura",
            "objetivo_atendimento",
            "profissional_responsavel",
            "outras_pessoas_participantes",
            "descricao_atendimento",
        ]
        widgets = {
            "data_atendimento": forms.DateInput(attrs={"type": "date"}),
            "descricao_atendimento": forms.Textarea(attrs={"rows": 4}),
        }


class AgendamentoForm(forms.ModelForm):
    """Form for creating an Agendamento."""

    class Meta:
        model = Agendamento
        fields = [
            "nome_atendido",
            "tipo_agendamento",
            "data_agendamento",
            "horario_atendimento",
            "observacoes",
        ]
        widgets = {
            "data_agendamento": forms.DateInput(attrs={"type": "date"}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        """Configure widget placeholders and empty labels."""
        super().__init__(*args, **kwargs)
        self.fields["tipo_agendamento"].empty_label = "Selecione uma opção"
        self.fields["horario_atendimento"].empty_label = "Selecione uma opção"


class LembreteForm(forms.ModelForm):
    """Form for creating/updating a lembrete."""

    class Meta:
        model = Lembrete
        fields = [
            "titulo",
            "urgencia",
            "anotacao",
        ]


class FamiliarForm(forms.ModelForm):
    """Form for creating/editing a Familiar."""

    DOCUMENTOS_CHOICES = [
        ("Certidão de Nascimento", "Certidão de Nascimento"),
        ("RG", "RG"),
        ("CPF", "CPF"),
        ("Carteira de Trabalho", "Carteira de Trabalho"),
        ("Título de Eleitor", "Título de Eleitor"),
        ("Certificado de Escolaridade", "Certificado de Escolaridade"),
        ("Documento Militar", "Documento Militar"),
        ("CNH", "CNH"),
    ]

    DOCUMENTOS_AUSENTES_CHOICES = [
        ("Certidão de Nascimento", "Certidão de Nascimento"),
        ("Certidão de Nascimento (2ª Via)", "Certidão de Nascimento (2ª Via)"),
        ("RG", "RG"),
        ("RG (2ª Via)", "RG (2ª Via)"),
        ("CPF", "CPF"),
        ("CPF (2ª Via)", "CPF (2ª Via)"),
        ("Carteira de Trabalho", "Carteira de Trabalho"),
        ("Carteira de Trabalho (2ª Via)", "Carteira de Trabalho (2ª Via)"),
        ("Título de Eleitor", "Título de Eleitor"),
        ("Título de Eleitor (2ª Via)", "Título de Eleitor (2ª Via)"),
        ("Documento Militar", "Documento Militar"),
        ("Documento Militar (2ª Via)", "Documento Militar (2ª Via)"),
        ("CNH", "CNH"),
    ]

    documentos_possui = forms.MultipleChoiceField(
        required=False,
        choices=DOCUMENTOS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    documentos_ausentes = forms.MultipleChoiceField(
        required=False,
        choices=DOCUMENTOS_AUSENTES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Familiar
        fields = [
            "nome",
            "nome_social",
            "data_nascimento",
            "sexo_biologico",
            "identidade_etnico_racial",
            "pessoa_transexual",
            "cpf_numero",
            "nis_numero",
            "documentos_possui",
            "documentos_ausentes",
            "parentesco",
            "perfil_referencia_egresso",
            "perfil_referencia_pre_egresso",
            "nome_interno_referencia",
            "encaminhamento",
            "encaminhamento_detalhe",
            "bairro",
            "telefone_numero",
            "telefone_contato",
            "telefone_observacao",
            "email_contato",
            "foto",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
            "cpf_numero": forms.TextInput(
                attrs={
                    "maxlength": "14",
                    "placeholder": "000.000.000-00",
                    "inputmode": "numeric",
                }
            ),
            "nis_numero": forms.TextInput(attrs={"maxlength": "11"}),
            "encaminhamento_detalhe": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sexo_biologico"].empty_label = "Selecione uma opcao"
        self.fields["identidade_etnico_racial"].empty_label = "Selecione uma opcao"
        self.fields["encaminhamento"].empty_label = "Selecione uma opcao"
        if self.instance and self.instance.documentos_possui:
            self.fields["documentos_possui"].initial = [
                item.strip()
                for item in self.instance.documentos_possui.split(",")
                if item.strip()
            ]
        if self.instance and self.instance.documentos_ausentes:
            self.fields["documentos_ausentes"].initial = [
                item.strip()
                for item in self.instance.documentos_ausentes.split(",")
                if item.strip()
            ]

        is_avulso = not getattr(self.instance, "cadastro_id", None)
        self.fields["nome_interno_referencia"].required = is_avulso

    def clean_cpf_numero(self):
        cpf = (self.cleaned_data.get("cpf_numero") or "").strip()
        if not cpf:
            return cpf

        digits = re.sub(r"\D", "", cpf)
        if len(digits) != 11:
            raise forms.ValidationError("Informe o CPF no formato 000.000.000-00.")

        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"

    def clean_foto(self):
        return _validate_image_upload(self.cleaned_data.get("foto"))

    def clean(self):
        cleaned_data = super().clean()
        is_avulso = not getattr(self.instance, "cadastro_id", None)

        nome_interno_referencia = (cleaned_data.get("nome_interno_referencia") or "").strip()
        perfil_referencia_egresso = cleaned_data.get("perfil_referencia_egresso")
        perfil_referencia_pre_egresso = cleaned_data.get("perfil_referencia_pre_egresso")

        if is_avulso and not nome_interno_referencia:
            self.add_error("nome_interno_referencia", "Informe o nome do interno da família.")

        if is_avulso:
            selecionados = int(bool(perfil_referencia_egresso)) + int(bool(perfil_referencia_pre_egresso))
            if selecionados != 1:
                message = "Marque somente uma opção: Egresso ou Pré-egresso."
                self.add_error("perfil_referencia_egresso", message)
                self.add_error("perfil_referencia_pre_egresso", message)

        cleaned_data["nome_interno_referencia"] = nome_interno_referencia
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.documentos_possui = ", ".join(self.cleaned_data.get("documentos_possui", []))
        instance.documentos_ausentes = ", ".join(self.cleaned_data.get("documentos_ausentes", []))
        if commit:
            instance.save()
        return instance


class SetorJuridicoForm(forms.ModelForm):
    """Form for creating setor juridico records."""

    situacao_juridica_atual = forms.MultipleChoiceField(
        required=False,
        choices=SetorJuridico.SITUACAO_JURIDICA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    encaminhamentos_setor = forms.MultipleChoiceField(
        required=False,
        choices=SetorJuridico.ENCAMINHAMENTO_SETOR_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = SetorJuridico
        fields = [
            "numero_processo",
            "vara_comarca",
            "tipo_processo",
            "situacao_juridica_atual",
            "situacao_juridica_outro",
            "encaminhamentos_setor",
            "encaminhamentos_setor_outro",
            "documento_pdf",
            "observacoes",
        ]
        widgets = {
            "observacoes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.situacao_juridica_atual:
            self.fields["situacao_juridica_atual"].initial = [
                item.strip()
                for item in self.instance.situacao_juridica_atual.split(",")
                if item.strip()
            ]
        if self.instance and self.instance.encaminhamentos_setor:
            self.fields["encaminhamentos_setor"].initial = [
                item.strip()
                for item in self.instance.encaminhamentos_setor.split(",")
                if item.strip()
            ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.situacao_juridica_atual = ", ".join(self.cleaned_data.get("situacao_juridica_atual", []))
        instance.encaminhamentos_setor = ", ".join(self.cleaned_data.get("encaminhamentos_setor", []))
        if commit:
            instance.save()
        return instance

    def clean_documento_pdf(self):
        return _validate_pdf_upload(self.cleaned_data.get("documento_pdf"))


class AdminUserCreateForm(forms.Form):
    """Form to create a system user (admin area)."""

    nome_completo = forms.CharField(label="Nome Completo", max_length=150)
    username = forms.CharField(label="Nome de Usuário (Username)", max_length=150)
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)
    senha_confirmacao = forms.CharField(label="Repita a Senha", widget=forms.PasswordInput)
    email = forms.EmailField(label="E-mail")
    cargo_es = forms.ChoiceField(label="Cargo no ES", choices=UserProfile.CARGO_CHOICES)

    def clean(self):
        """Validate password confirmation and unique username."""
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_confirmacao = cleaned_data.get("senha_confirmacao")

        if senha and senha_confirmacao and senha != senha_confirmacao:
            self.add_error("senha_confirmacao", "As senhas não conferem.")
        elif senha:
            try:
                validate_password(senha)
            except DjangoValidationError as exc:
                self.add_error("senha", " ".join(exc.messages))

        username = cleaned_data.get("username")
        if username:
            username = username.strip()
            cleaned_data["username"] = username
            User = get_user_model()
            if User.objects.filter(username__iexact=username).exists():
                self.add_error("username", "Nome de usuário já existe.")

        return cleaned_data

    def save(self):
        """Create and return a new user with profile."""
        User = get_user_model()
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["senha"],
        )
        user.first_name = self.cleaned_data["nome_completo"].split(" ")[0]
        user.last_name = " ".join(self.cleaned_data["nome_completo"].split(" ")[1:])
        user.is_staff = self.cleaned_data["cargo_es"] == "gerencia_administracao"
        user.save()

        UserProfile.objects.create(user=user, cargo_es=self.cleaned_data["cargo_es"])
        return user



