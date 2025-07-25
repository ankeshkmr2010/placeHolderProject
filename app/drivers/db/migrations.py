from yoyo import read_migrations, get_backend

from app.drivers.configs.config import Config


def run_migration():
    be = get_backend(Config.YOYO_POSTGRES)
    migrations = read_migrations("app/migrations")
    with be.lock():
        be.apply_migrations(be.to_apply(migrations))
