import tkinter as tk
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


def evaluar():
    try:
        promedio = float(entry_promedio.get())
        materias = int(entry_materias.get())

        if not (0.0 <= promedio <= 5.0):
            raise ValueError("El promedio debe estar entre 0.0 y 5.0")
        if materias < 0:
            raise ValueError("Las materias perdidas no pueden ser negativas")

        env.reset()
        env.assert_string(f'(rendimiento (promedio {promedio}) (materias_perdidas {materias}))')
        env.run()

        resultado_texto = "No se encontró una evaluación."
        mensaje = ""

        for fact in env.facts():
            if fact.template.name == "evaluacion":
                resultado = fact["resultado"]

                if resultado == "Excelente":
                    mensaje = "¡Felicitaciones! Puedes aplicar a una beca."
                elif resultado == "Aprobado":
                    mensaje = "Buen trabajo, sigue así."
                elif resultado == "Requiere tutoría":
                    mensaje = "Te recomendamos asistir a tutorías."
                elif resultado == "En riesgo académico":
                    mensaje = "Debes mejorar urgentemente, busca ayuda."
                elif resultado == "Reprobado el curso":
                    mensaje = "Has reprobado, debes repetir el curso."

                resultado_texto = f"Resultado: {resultado}\nRecomendación: {mensaje}"
                break

        label_resultado.config(text=resultado_texto)

    except ValueError as e:
        label_resultado.config(text=f"Error: {e}")


root = tk.Tk()
root.title("Sistema Experto - Evaluación Académica")
root.geometry("450x250")

tk.Label(root, text="Promedio del estudiante (0.0 - 5.0):").pack(pady=5)
entry_promedio = tk.Entry(root)
entry_promedio.pack()

tk.Label(root, text="Número de materias perdidas:").pack(pady=5)
entry_materias = tk.Entry(root)
entry_materias.pack()

tk.Button(root, text="Evaluar", command=evaluar).pack(pady=10)


label_resultado = tk.Label(root, text="", fg="blue", font=("Arial", 12), justify="left")
label_resultado.pack(pady=10)

root.mainloop()
