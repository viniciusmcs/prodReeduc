"""Production settings.

Security-focused configuration with DEBUG disabled.
"""

from .settings_base import *  # noqa: F401,F403
from .settings_base import get_env_bool, get_env_list, is_weak_secret_key

# Ensure DEBUG is disabled in production.
DEBUG = False

if is_weak_secret_key(SECRET_KEY):
	raise ValueError(
		"DJANGO_SECRET_KEY insegura para produção. Defina uma chave forte (32+ chars) no ambiente."
	)

# Internal HTTP by default; enable strict HTTPS mode with ENABLE_HTTPS=True.
ENABLE_HTTPS = get_env_bool("ENABLE_HTTPS", False)

SECURE_SSL_REDIRECT = ENABLE_HTTPS
SESSION_COOKIE_SECURE = ENABLE_HTTPS
CSRF_COOKIE_SECURE = ENABLE_HTTPS
SECURE_HSTS_SECONDS = 31536000 if ENABLE_HTTPS else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = ENABLE_HTTPS
SECURE_HSTS_PRELOAD = ENABLE_HTTPS
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# Optional: configure trusted origins via env to avoid hardcoding.
CSRF_TRUSTED_ORIGINS = get_env_list(
	"CSRF_TRUSTED_ORIGINS",
	["http://10.0.125.4", "http://10.0.125.4:8000"],
)
