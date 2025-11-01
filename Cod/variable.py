class Variable:
    def __init__(self, valor='0', dominio=None):
        self.valor = valor
        self.fijo = valor != '0'
        if self.fijo:
            self.dominio = [valor]
        else:
            self.dominio = dominio or [str(i) for i in range(1, 10)]

    def asignar(self, v):
        if not self.fijo:
            self.valor = v

    def desasignar(self):
        if not self.fijo:
            self.valor = '0'

    def get_valor(self):
        return self.valor
    

    def __repr__(self):
        return f"Variable(valor={self.valor}, dominio={self.dominio})"
