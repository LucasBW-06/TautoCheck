class ErroDeSintaxe(Exception):
    def __init__(self, formula, msg="Formula logica invalida"):
        super().__init__("\n\n" + 100 * "=" + f"\n\n{msg}: '{formula}'\n\n" + 100 * "=")
        self.formula = formula