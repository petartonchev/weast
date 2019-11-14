import environ


class SentimentRouter:
    env = environ.Env()
    database = "moodstock_nosql_db"

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'sentiment':
            return self.database
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'sentiment':
            return self.database
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'sentiment':
            return db == self.database
        elif db == self.database:
            # Ensure that all other apps don't get migrated on this database.
            return False
        return None
