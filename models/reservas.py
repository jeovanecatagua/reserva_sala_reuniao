class reserva_sala:
    def __init__(self, id, user, sala_reuniao, dt_reuniao, hr_inicio, hr_fim):
        self.id             = id
        self.user           = user
        self.sala_reuniao   = sala_reuniao
        self.dt_reuniao     = dt_reuniao
        self.hr_inicio      = hr_inicio
        self.hr_fim         = hr_fim

class usuario:
    def __init__(self, id, email, senha, perfil):
        self.id     = id
        self.email  = email
        self.senha  = senha
        self.perfil = perfil

class sala_cadastro:
    def __init__(self, id, sala):
        self.id   = id
        self.sala = sala