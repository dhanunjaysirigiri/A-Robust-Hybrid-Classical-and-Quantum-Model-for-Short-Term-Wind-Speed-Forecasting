"""
WSGI config for a_robust_hybrid_classical_and_quantum_model.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_robust_hybrid_classical_and_quantum_model.settings')
application = get_wsgi_application()
