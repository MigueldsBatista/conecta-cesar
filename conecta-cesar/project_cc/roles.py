from rolepermissions.roles import AbstractUserRole

class Professor(AbstractUserRole):
    available_permissions={'ver_avisos':True, 'gerenciar_notas': True, 'ver_notas':True, 'gerenciar_diarios': True, 'ver_diarios':True, 'ver_avisos' :True, 'ver_calendario':True}

class Aluno(AbstractUserRole):
    available_permissions={'ver_notas': True, 'ver_diarios': True, 'ver_avisos':True}