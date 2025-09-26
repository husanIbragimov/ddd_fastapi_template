from sqladmin import ModelView

from infrastructure.persistence.models import UserModel
from presentation.admin.admin import admin


class UserAdmin(ModelView, model=UserModel):
    column_list = (UserModel.uuid, UserModel.first_name, UserModel.last_name)


admin.add_view(UserAdmin)
