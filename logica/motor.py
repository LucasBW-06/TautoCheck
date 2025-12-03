from .erros import ErroDeSintaxe
from .parser import ParserLogico
from .expansor import Expansor


class TableauAnaltitco:

    def resolver(self, expressao):
        expressao = expressao.replace(" ", "")

        if expressao.count('=') > 1:
            raise ErroDeSintaxe(expressao, "Estrutura de sintaxe incorreta")
        elif '=' in expressao:
            prem, conc = expressao.split('=')
            if prem == "" or conc == "":
                raise ErroDeSintaxe(expressao, "Estrutura de sintaxe incorreta")

        prem = self.__premissas(expressao)
        ramos = Expansor().expandir(prem)
        return self.__verificar(ramos)

    def __premissas(self, expressao):
        resultado = []

        if '=' in expressao:
            partes = expressao.split('=')
            premissas_texto, conclusao_texto = partes
            premissas_lista = premissas_texto.split(',')

            self.__tratamento([conclusao_texto] + premissas_lista)

            resultado = (
                [(ParserLogico(conclusao_texto).parse(), False)] +
                [(ParserLogico(f).parse(), True) for f in premissas_lista]
            )
        else:
            self.__tratamento([expressao])
            resultado = [(ParserLogico(expressao).parse(), False)]

        return resultado

    def __verificar(self, ramos):
        fechados = 0

        for r in ramos:
            vistos = {}

            for atomo, flag in r:
                nome = atomo['value']

                if nome in vistos and vistos[nome] != flag:
                    fechados += 1
                    break

                vistos[nome] = flag

        return fechados == len(ramos)

    def __tratamento(self, lista):
        conectivos = {">", "&", "|"}

        for formula in lista:
            if formula == "":
                raise ErroDeSintaxe(formula)
            pilha = 0
            n = len(formula)

            for i, c in enumerate(formula):
                prox = formula[i+1] if i+1 < n else None
                ant  = formula[i-1] if i-1 >= 0 else None

                if c not in conectivos and c not in "()":
                    if prox == '(':
                        raise ErroDeSintaxe(formula)

                if c == ')':
                    pilha -= 1
                    if pilha < 0:
                        raise ErroDeSintaxe(formula)
                    if prox and prox not in conectivos and prox not in ["(", ")"]:
                        raise ErroDeSintaxe(formula)

                if c == '(' and prox == ')':
                    raise ErroDeSintaxe(formula)

                if c == '(' and prox in conectivos:
                    raise ErroDeSintaxe(formula)

                if c in conectivos and prox == ')':
                    raise ErroDeSintaxe(formula)

                if c in conectivos and prox in conectivos:
                    raise ErroDeSintaxe(formula)

                if c == '(':
                    pilha += 1

            if pilha > 0:
                raise ErroDeSintaxe(formula)

            if formula[-1] in conectivos:
                raise ErroDeSintaxe(formula)
