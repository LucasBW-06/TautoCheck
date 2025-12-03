class ParserLogico:
    def __init__(self, formula):
        self.formula = formula

    def parse(self):
        f, _ = self.__parser_parens(self.formula)
        return self.__estruturar(f)

    def __parser_parens(self, formula, i=0):
        resultado = []
        texto = ""

        def desempacotar():
            nonlocal texto, resultado
            if texto:
                resultado.extend(self.__tokenizar(texto))
                texto = ""

        while i < len(formula):
            c = formula[i]
            if c == "(":
                desempacotar()
                sub, i = self.__parser_parens(formula, i + 1)
                resultado.append(sub)
            elif c == ")":
                desempacotar()
                return resultado, i
            else:
                texto += c
            i += 1

        desempacotar()
        return resultado, i

    def __tokenizar(self, formula):
        conectivos = {"&", "|", ">", "~"}
        tokens = []
        texto = ""
        for c in formula:
            if c in conectivos:
                if texto:
                    tokens.append(texto)
                    texto = ""
                tokens.append(c)
            else:
                texto += c
        if texto:
            tokens.append(texto)
        return tokens

    def __estruturar(self, formula):
        if isinstance(formula, str):
            return {"type": "prop", "value": formula}

        if isinstance(formula, list):

            for op, tipo in [(">", "conditional"), ("|", "or"), ("&", "and")]:
                for i in range(len(formula)-1, -1, -1):
                    if formula[i] == op:
                        return {
                            "type": tipo,
                            "left": self.__estruturar(formula[:i]),
                            "right": self.__estruturar(formula[i+1:])
                        }

            if formula[0] == "~":
                return {
                    "type": "not",
                    "child": self.__estruturar(formula[1])
                }

        if len(formula) == 1:
            return self.__estruturar(formula[0])
