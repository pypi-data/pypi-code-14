from nodeconductor.core.permissions import StaffPermissionLogic


PERMISSION_LOGICS = (
    ('nodeconductor_auth_valimo.AuthResult', StaffPermissionLogic(any_permission=True)),
)
