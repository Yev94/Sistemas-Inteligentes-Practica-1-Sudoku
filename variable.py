# variable.py
class Variable:
    
    def __init__(self, valor='0', dominio=None):
        #  valor: número actual como string ('0' si está vacía)
        self.valor = valor 
        # dominio: lista de valores posibles (por defecto 1..9)
        self.dom = dominio or [str(i) for i in range(1, 10)]

    # True si la variable ya tiene un valor distinto de '0'
    def is_assigned(self):
        return self.valor != '0'

    # Asigna un valor y reduce el dominio a ese valor solo durante la siguiente iteración, si no era el que necesitábamos el dom vuelve al anterior original
    def assign(self, v):
        self.valor = v
        self.dom = [v]

    # Deshace la asignación (para hacer backtracking)
    def unassign(self):
        self.valor = '0'

    def __repr__(self):
        return f"Variable(valor={self.valor}, dom={self.dom})"
