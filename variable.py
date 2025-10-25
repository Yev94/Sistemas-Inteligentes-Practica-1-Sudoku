class Variable:
    def __init__(self, valor='0', dominio=None):
        self.valor = valor
        self.fijo = valor != '0'

        if self.fijo:
            # 🔹 Si la celda tiene un valor fijo, su dominio es solo ese valor
            self.dominio = [valor]
        else:
            # 🔹 Si está vacía, su dominio inicial es 1..9 o el que le pases
            self.dominio = dominio or [str(i) for i in range(1, 10)]

    def esta_asignado(self):
        """Devuelve True si la variable ya tiene valor esta_asignado."""
        return self.valor != '0'

    def asignar(self, v):
        """Asigna un valor """
        self.valor = v

    def desasignar(self):
        """Desasigna el valor y restaura el dominio completo."""
        self.valor = '0'
    
    def resetearDominio(self):
        """Desasigna el valor y restaura el dominio completo."""
        self.dominio = [str(i) for i in range(1, 10)]

    def getvalor(self):
        """Devuelve el valor actual de la variable."""
        return self.valor

    def __repr__(self):
        return f"Variable(valor={self.valor}, dominio={self.dominio})"
