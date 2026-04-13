# REEDUC

## Requisitos
- Python 3.12+

## Ambiente virtual (venv)
```bash
python -m venv venv
venv\Scripts\activate
```

## Dependências
```bash
pip install -r requirements.txt
```

## Variáveis de ambiente
Copie o arquivo de exemplo e ajuste as credenciais:
```bash
copy .env.example .env
```

## Migrações
```bash
python manage.py migrate
```

## Banco de dados (SQLite padrão)
O projeto está configurado para usar `sqlite3` por padrão:

```python
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}
```

Se quiser PostgreSQL, defina `USE_SQLITE=False` no `.env` e configure `DB_*`.

## Criar superusuario
```bash
python manage.py createsuperuser
```

## Executar
```bash
python manage.py runserver
```

## Acesso na rede interna (HTTP)
O sistema pode ser acessado na rede por:

`http://10.0.125.4:8000`

Para subir escutando no IP da máquina:

```bash
python manage.py runserver 0.0.0.0:8000
```

## Testes
```bash
python manage.py test
```

## Produção
Defina `DJANGO_SETTINGS_MODULE=reeduc.settings_prod` e `DJANGO_DEBUG=False`.

Neste projeto, o `settings_prod` está ajustado para rede interna por HTTP (sem redirecionamento obrigatório para HTTPS).

### Produção com Docker + PostgreSQL (IP 10.0.125.4, porta 8000)

1. Copie o arquivo de ambiente de produção:

```bash
copy .env.prod.example .env
```

2. Edite o `.env` com valores fortes para:
- `DJANGO_SECRET_KEY`
- `DB_PASSWORD`
- `DEFAULT_ADMIN_PASSWORD`

Se estiver sem TLS na rede interna, mantenha `ENABLE_HTTPS=False`. Quando tiver HTTPS, altere para `ENABLE_HTTPS=True`.

3. Suba aplicação e banco com volume persistente:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

4. Acesse:

`http://10.0.125.4:8000`

5. Para ver logs:

```bash
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml logs -f db
```

### Checklist de segurança

- Senhas de usuários Django são armazenadas com hash seguro do Django (PBKDF2 por padrão).
- `DEBUG=False` em produção.
- `SECRET_KEY` fraca/placeholder agora bloqueia a inicialização em `settings_prod`.
- `X_FRAME_OPTIONS=DENY`, `SECURE_CONTENT_TYPE_NOSNIFF=True`, cookies HTTPOnly e SameSite ativados em produção.
- `CSRF_TRUSTED_ORIGINS` inclui `http://10.0.125.4:8000`.

### Go-live (sem vazamento de segredos)

1. Crie o arquivo de ambiente final sem subir no Git:

```bash
copy .env.go-live.example .env.go-live
```

2. Preencha segredos fortes em `.env.go-live`:
- `DJANGO_SECRET_KEY`
- `DB_PASSWORD`

3. Gere certificado TLS para IP interno (self-signed):

```bash
mkdir nginx\certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx\certs\privkey.pem -out nginx\certs\fullchain.pem -subj "/CN=10.0.125.4"
```

4. Suba produção com proxy + app + banco + volumes:

```bash
docker compose -f docker-compose.go-live.yml --env-file .env.go-live up -d --build
```

5. Acesse:
- HTTP: `http://10.0.125.4:8000`
- HTTPS (proxy): `https://10.0.125.4:8443`

6. Firewall (Windows) — liberar apenas o necessário:

```powershell
New-NetFirewallRule -DisplayName "REEDUC-HTTP-8000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000
New-NetFirewallRule -DisplayName "REEDUC-HTTPS-8443" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8443
```

7. Não publique:
- `.env`, `.env.go-live`
- `nginx/certs/*`
- dumps/backup com dados reais
