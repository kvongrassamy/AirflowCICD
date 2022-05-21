from flask_appbuilder import ModelView
from flask_appbuilder.actions import action
from flask import redirect

class JobView(ModelView):

    def post_add(self, item):
        item.write_dag()

    def post_update(self, item):
        item.update_dag()

    def pre_delete(self, item):
        item.delete_dag()

    @action("muldelete", "Delete", "Delete all jobs?", "fa-trash", single=False)
    def muldelete(self, items):
        for item in items:
            item.delete_dag()
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())

    @action("mulrecreate", "Recreate", "Recreate all jobs?", "fa-gear", single=False)
    def mulrecreate(self, items):
        for item in items:
            item.write_dag()
        self.update_redirect()
        return redirect(self.get_redirect())
