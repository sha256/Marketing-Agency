from django.forms.models import modelformset_factory
from var_dump import var_dump
from apps.auth.forms.roleform import RoleMatrixForm
from apps.auth.models.role import Role

__author__ = 'sha256'
from core.views import SecuredView
from apps.auth.forms.addrole import AddRoleForm


class RolesView(SecuredView):

    def get(self, request, *args, **kwargs):
        return self.render(request, "auth/roles.html", {})

    def get_common_data(self, request):
        data = {}
        roleadd = AddRoleForm(request.POST or None)
        foo = modelformset_factory(Role, form=RoleMatrixForm, extra=0)
        matrix = foo(request.POST if "updatematrix" in request.POST else None, prefix="role", queryset=Role.objects.all())
        if "updatematrix" in request.POST and matrix.is_valid():
            matrix.save()
            return self.redirect(self.reverse('auth-roles'))
        if "addrole" in request.POST and roleadd.is_valid():
            roleadd.save()
            return self.redirect(request.path)

        data['form'] = roleadd
        data['roleset'] = matrix
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        return self.render(request, "auth/roles.html", data)



