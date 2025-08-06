import clips

env = clips.Environment()

env.build("(deftemplate rendimiento (slot promedio (type FLOAT)) (slot materias_perdidas (type INTEGER)))")
env.build("(deftemplate evaluacion (slot resultado (type STRING)))")

env.build('''
(defrule excelente
  (rendimiento (promedio ?p&:(>= ?p 4.5)) (materias_perdidas ?m&:(= ?m 0)))
  =>
  (assert (evaluacion (resultado "Excelente")))
)
''')

env.build('''
(defrule aprobado
  (rendimiento (promedio ?p&:(and (>= ?p 3.0) (< ?p 4.5))) (materias_perdidas ?m&:(<= ?m 1)))
  =>
  (assert (evaluacion (resultado "Aprobado")))
)
''')

env.build('''
(defrule requiere_tutoria
  (rendimiento (promedio ?p&:(and (>= ?p 2.5) (< ?p 3.0))) (materias_perdidas ?m&:(<= ?m 2)))
  =>
  (assert (evaluacion (resultado "Requiere tutoría")))
)
''')

env.build('''
(defrule en_riesgo
  (rendimiento (promedio ?p&:(and (>= ?p 2.0) (< ?p 2.5))) (materias_perdidas ?m&:(<= ?m 3)))
  =>
  (assert (evaluacion (resultado "En riesgo académico")))
)
''')

env.build('''
(defrule reprobado
  (rendimiento (promedio ?p&:(< ?p 2.0)) (materias_perdidas ?m&:(>= ?m 3)))
  =>
  (assert (evaluacion (resultado "Reprobado el curso")))
)
''')

try:
    promedio = float(input("Ingrese el promedio del estudiante (0.0 a 5.0): "))
    materias = int(input("Ingrese el número de materias perdidas: "))

    if not (0.0 <= promedio <= 5.0):
        raise ValueError("El promedio debe estar entre 0.0 y 5.0")

    if materias < 0:
        raise ValueError("El número de materias no puede ser negativo.")

    env.reset()
    env.assert_string(f'(rendimiento (promedio {promedio}) (materias_perdidas {materias}))')
    env.run()

    resultado_encontrado = False
    for fact in env.facts():
        if fact.template.name == "evaluacion":
            resultado = fact["resultado"]
            resultado_encontrado = True

            if resultado == "Excelente":
                mensaje = "¡Felicitaciones!."
            elif resultado == "Aprobado":
                mensaje = "Buen trabajo, sigue así."
            elif resultado == "Requiere tutoría":
                mensaje = "Te recomendamos asistir a tutorías académicas."
            elif resultado == "En riesgo académico":
                mensaje = "Debes hablar con un orientador académico."
            elif resultado == "Reprobado el curso":
                mensaje = "Has reprobado el curso. Se debe repetir."

            print(f"\n Resultado: {resultado}")
            print(f" Recomendación: {mensaje}")
            break

    if not resultado_encontrado:
        print("No se pudo determinar una evaluación con los datos proporcionados.")

except ValueError as ve:
    print(f" Error: {ve}")
