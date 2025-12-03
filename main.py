from logica.motor import TableauAnaltitco

expressao = input("Informe a expressão (φ ou Γ⊢φ): ")

try:
    resultado = TableauAnaltitco().resolver(expressao)
    if resultado:
        print("É uma tautologia!")
    else:
        print("Não é uma tautologia.")
except Exception as e:
    print("Erro:", e)
