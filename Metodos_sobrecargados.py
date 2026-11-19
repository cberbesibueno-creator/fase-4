class CalculadoraCostos:

    def calcular_costo(self, costo, impuesto=0, descuento=0):
        try:
            if costo < 0:
                raise ValueError("El costo no puede ser negativo.")

            if not 0 <= impuesto <= 100:
                raise ValueError("El impuesto debe estar entre 0 y 100.")

            if not 0 <= descuento <= 100:
                raise ValueError("El descuento debe estar entre 0 y 100.")

            # Aplicar descuento
            valor_descuento = costo * descuento / 100
            subtotal = costo - valor_descuento

            # Aplicar impuesto
            valor_impuesto = subtotal * impuesto / 100
            total = subtotal + valor_impuesto

            return round(total, 2)

        except ValueError as error:
            print("Error en el cálculo:", error)
            return None


# Crear objeto
calculadora = CalculadoraCostos()

# Diferentes formas de utilizar el método
print("Costo normal:", calculadora.calcular_costo(100000))
print("Costo con impuesto:", calculadora.calcular_costo(100000, 19))
print("Costo con descuento:", calculadora.calcular_costo(100000, 0, 10))
print("Costo con impuesto y descuento:", calculadora.calcular_costo(100000, 19, 10))