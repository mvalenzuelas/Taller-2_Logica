from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, ttk, messagebox, END
import tkinter.font as font
import modelo_difuso as md # Se importa el modelo de lógica difusa creado en un archivo aparte

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def limpiarInputs():
    input_antiguedad.delete(0,END)
    input_antiguedad.insert(0, "")
    input_escala.delete(0,END)
    input_escala.insert(0, "")
    input_tiempo.delete(0,END)
    input_tiempo.insert(0, "")

def simular():
    # Se verifica que existen valores
    if(input_antiguedad.get() == '' or input_escala.get() == '' or input_tiempo.get() == ''):
        messagebox.showinfo("Error","No pueden haber campos vacios, por favor rellene todos los campos")
        limpiarInputs()
        return 0
    if not (input_antiguedad.get().isdigit() or input_escala.get().isdigit() or input_tiempo.get().isdigit()):
        messagebox.showinfo("Error","Solo puede ingresar números enteros o decimales")
        limpiarInputs()
        return 0
    # Se consiguen los valores
    valor_antiguedad = float(input_antiguedad.get())
    valor_habilidad = float(input_escala.get())
    valor_tiempo = float(input_tiempo.get())
    # Verificación de condiciones
    if valor_antiguedad > 15 or valor_antiguedad < 0:
        messagebox.showinfo("Error","El valor de la antiguedad debe estar entre 0 y 15 años !")
        limpiarInputs()
        return 0
    if valor_habilidad < 0 or valor_habilidad > 10:
        messagebox.showinfo("Error","El valor de la habilidad debe estar entre 0 y 10 !")
        limpiarInputs()
        return 0
    if valor_tiempo < 0 or valor_tiempo > 10:
        messagebox.showinfo("Error","El valor del tiempo debe estar 0 y 10 horas!")
        limpiarInputs()
        return 0
    # Si no hubo errores se ejecuta la simulación
    valor_graficar = combo.get()
    texto_prediccion = modeloDifuso.predecir(valor_antiguedad,valor_habilidad,valor_tiempo,valor_graficar)
    texto_resultado_update = "La categoría de juegos determinada para sus\npreferencias es: " + texto_prediccion
    texto_resultado_update = texto_resultado_update + "\n\n" + "Los juegos recomendados para esta\ncategoría según sus preferencias son:\n"
    texto_resultado_update = texto_resultado_update + "\n" + "   - Aqui van los juegos listados\n"
    texto_resultado_update = texto_resultado_update + "\n" + "Otros juego recomendados son:\n "
    texto_resultado_update = texto_resultado_update + "\n" + "   -Amongus"
    canvas.itemconfigure(texto_resultado, text = texto_resultado_update, font = ("Inter", 16 * -1))

window = Tk()

window.geometry("873x712")
window.configure(bg = "#36103F")
window.title("Recomendador Difuso")

bg = PhotoImage(file=relative_to_assets("gradient.png"))
label1 = Label(image = bg)
label1.place(x = 0, y = 0)

canvas = Canvas(
    window,
    bg = "purple",
    height = 712,
    width = 873,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.create_image(0,0,image=bg,anchor='nw')

canvas.place(x = 0, y = 0)

canvas.create_rectangle(
    466.0,
    69.0,
    856.0,
    585.0,
    fill="#000000",
    outline="yellow")

texto_resultado = canvas.create_text(
    476.0,
    76.0,
    anchor="nw",
    text="Estimado usuario, para comenzar\nresponda a las preguntas del menú de la\nizquierda, posteriormente presione el\nbotón “Buscar Juegos”.",
    fill="#69FF78",
    font=("Inter", 20 * -1)
)

canvas.create_rectangle(
    19.0,
    13.0,
    415.0,
    94.0,
    fill="#424242",
    outline="#000000")

canvas.create_rectangle(
    18.0,
    170.0,
    414.0,
    251.0,
    fill="#424242",
    outline="#000000")

canvas.create_rectangle(
    19.0,
    317.0,
    415.0,
    398.0,
    fill="#424242",
    outline="#000000")

canvas.create_rectangle(
    19.0,
    467.0,
    415.0,
    548.0,
    fill="#424242",
    outline="#000000")

f1 = font.Font(family='Inter', size=12, weight="bold")
button_ejecutar_simulacion = Button(
    bg='#990404',
    borderwidth=3,
    highlightthickness=0,
    command=lambda: simular(),
    relief="raised",
    text='Ejecutar consulta',
    fg='white'
)
button_ejecutar_simulacion.place(
    x=113.0,
    y=643.0,
    width=192.0,
    height=47.0
)
button_ejecutar_simulacion['font'] = f1

f = font.Font(family='Inter', size=12, weight="bold")
button_ver_graficas = Button(
    bg='#2D5FC0',
    borderwidth=3,
    highlightthickness=0,
    command=lambda: modeloDifuso.graficarFuncionesDePertenenciaDifusas(),
    relief="raised",
    text='Ver gráficas de funciones\n de pertenencia de las variables',
    fg='white'
)
button_ver_graficas['font'] = f

button_ver_graficas.place(
    x=602.0,
    y=614.0,
    width=251.0,
    height=76.0
)

canvas.create_text(
    24.0,
    481.0,
    anchor="nw",
    text="¿Desea visualizar la grafica de resultado al\naplicar la desfusificación?",
    fill="#FFFFFF",
    font=("Inter Medium", 18 * -1)
)

canvas.create_text(
    32.0,
    178.0,
    anchor="nw",
    text="En una escala de 0 al 10 ¿Qué tan hábil se\nconsidera en los juegos?\n(Puede usar decimales) ",
    fill="#FFFFFF",
    font=("Inter Medium", 18 * -1)
)


canvas.create_text(
    28.0,
    325.0,
    anchor="nw",
    text="En una escala de 0 al 10 ¿Cuántas horas tiene\ndisponibles semanalmente para jugar?\n(Puede usar decimales)",
    fill="#FFFFFF",
    font=("Inter Medium", 18 * -1)
)

canvas.create_text(
    35.0,
    26.0,
    anchor="nw",
    text="¿Con cuántos años de antigüedad prefiere\n un juego?  Considere un rango de 0 a 15\n años ",
    fill="#FFFFFF",
    font=("Inter Medium", 18 * -1)
)

canvas.create_text(
    117.0,
    643.0,
    anchor="nw",
    text="Buscar Juegos",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 18 * -1)
)


input_antiguedad = Entry(
    bd=0,
    bg="#6B6565",
    highlightthickness=0,
    borderwidth= 3,
    fg='white'
)
input_antiguedad.place(
    x=151.0,
    y=114.0,
    width=118.0,
    height=33.0,
)

input_escala = Entry(
    bd=0,
    bg="#6B6565",
    highlightthickness=0,
    borderwidth= 3,
    fg='white'

)
input_escala.place(
    x=150.0,
    y=270.0,
    width=118.0,
    height=33.0
)

input_tiempo = Entry(
    bd=0,
    bg="#6B6565",
    highlightthickness=0,
    borderwidth= 3,
    fg='white'

)
input_tiempo.place(
    x=150.0,
    y=420.0,
    width=118.0,
    height=33.0
)

combo = ttk.Combobox(state="readonly",
        values=["Si","No"])
combo.place(x=163, y=570)
combo.current(0)

canvas.create_rectangle(
    466.0,
    38.0,
    611.0,
    69.0,
    fill="#000000",
    outline="white")

canvas.create_text(
    498.0,
    41.0,
    anchor="nw",
    text="Terminal",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)


## Se crea un objeto de modelo difuso
modeloDifuso = md.modeloDifuso()
window.resizable(False, False)
window.mainloop()
