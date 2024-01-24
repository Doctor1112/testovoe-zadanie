from project.settings import settings

config = {
    'connections': {
        'default': f'postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
                   f'@db:5432/{settings.POSTGRES_DB}'
    },
    'apps': {
        'models': {
            'models': ['project.db.models', 'aerich.models'],
            'default_connection': 'default'
        }
    }
}
