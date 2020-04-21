class MyAppRouter(object):
    """A router to control all database operations on models in
    the my_site application"""

    def db_for_read(self, model, **hints):
        "Point admin read operations on my_site to 'default'"
        if model._meta.app_label == 'my_site' :
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        "Point admin write operations on my_site to 'default'"
        
        print model._meta.app_label
        if model._meta.app_label == 'my_site':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in my_site is involved"
        if obj1._meta.app_label == 'my_site' or obj2._meta.app_label == 'my_site':
            return True
        return None

    def allow_syncdb(self, db, model):
        return None