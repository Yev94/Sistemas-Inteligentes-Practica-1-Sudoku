class Variable:
    def __init__(self, value='0', domain=None):
        self.value = value
        # Solo las vacías tienen dominio inicial 1..9
        self.fixed = value != '0'
        self.domain = domain or [str(i) for i in range(1, 10)]
        # if value == '0':
        # else:
        #     self.domain = None  # En vez de lista vacía

    def is_assigned(self):
        """Devuelve True si la variable ya tiene valor asignado."""
        return self.value != '0'

    def assign(self, v):
        """Asigna un valor y reduce el dominio a un único valor."""
        self.value = v

    def unassign(self):
        """Desasigna el valor y restaura el dominio completo."""
        self.value = '0'
        self.domain = [str(i) for i in range(1, 10)]

    def getValue(self):
        """Devuelve el valor actual de la variable."""
        return self.value

    def __repr__(self):
        return f"Variable(value={self.value}, domain={self.domain})"
