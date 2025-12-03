class Expansor:
    def __init__(self):
        pass
    
    def expandir(self, ramo):
        for i, (f, valor) in enumerate(ramo):
            tipo = f['type']

            if tipo == 'prop':
                continue

            if valor:
                return self.__expandir_verdadeira(ramo, i)
            else:
                return self.__expandir_falsa(ramo, i)
        
        return [ramo]

    def __expandir_verdadeira(self, ramo, i):
        f, valor = ramo[i]
        tipo = f['type']

        if tipo == 'and':
            novo_ramo = ramo[:i] + [(f['left'], True), (f['right'], True)] + ramo[i+1:]
            return self.expandir(novo_ramo)
        
        elif tipo == 'or':
            ramo1 = ramo[:i] + [(f['left'], True)] + ramo[i+1:]
            ramo2 = ramo[:i] + [(f['right'], True)] + ramo[i+1:]
            return self.expandir(ramo1) + self.expandir(ramo2)
        
        elif tipo == 'conditional':
            ramo1 = ramo[:i] + [(f['left'], False)] + ramo[i+1:]
            ramo2 = ramo[:i] + [(f['right'], True)] + ramo[i+1:]
            return self.expandir(ramo1) + self.expandir(ramo2)
        
        elif tipo == 'not':
            novo_ramo = ramo[:i] + [(f['child'], False)] + ramo[i+1:]
            return self.expandir(novo_ramo)

    def __expandir_falsa(self, ramo, i):
        f, valor = ramo[i]
        tipo = f['type']

        if tipo == 'and':
            ramo1 = ramo[:i] + [(f['left'], False)] + ramo[i+1:]
            ramo2 = ramo[:i] + [(f['right'], False)] + ramo[i+1:]
            return self.expandir(ramo1) + self.expandir(ramo2)
        
        elif tipo == 'or':
            novo_ramo = ramo[:i] + [(f['left'], False), (f['right'], False)] + ramo[i+1:]
            return self.expandir(novo_ramo)
        
        elif tipo == 'conditional':
            novo_ramo = ramo[:i] + [(f['left'], True), (f['right'], False)] + ramo[i+1:]
            return self.expandir(novo_ramo)
        
        elif tipo == 'not':
            novo_ramo = ramo[:i] + [(f['child'], True)] + ramo[i+1:]
            return self.expandir(novo_ramo)