import tkinter as tk
from tkinter import ttk,messagebox
from tkinter import*
import subprocess
from reportlab.lib.pagesizes import A4
import sqlite3
import time
from docx import *
import win32print
import win32api
conexion=sqlite3.connect("finalprog.db")
conexion.row_factory=sqlite3.Row
tabla=conexion.cursor
import os
#INICIO 

ventana=Tk()
ventana.title("Ventas")
ventana.config(bg="grey")
ventana.geometry("800x500")
ventana.resizable(0,0)

def vender():
    frame_vender = Frame(ventana)
    frame_vender.place(x=0,y=0)
    frame_vender.config(bg="#00A2E8",width=800,height=500)

    lista_productos = Listbox(ventana, font=("arial", 14), width=30, height=10)
    lista_productos.place(x=30,y=120)

    lista_ventas = Listbox(frame_vender, font=("arial", 14), width=30, height=10)
    lista_ventas.place(x=450, y=120)

    productos_label = Label(frame_vender,text="Productos",bg="#00A2E8",fg="black",font=("arial",30))
    productos_label.place (x=25,y=75)

    carrito_label = Label(frame_vender,text="Carrito",bg="#00A2E8",fg="black",font=("arial",30))
    carrito_label.place (x=550,y=68)

    tabla = conexion.cursor()
    tabla.execute("SELECT nombre, precio, stock FROM productos ORDER BY nombre")
    conexion.commit()
    datos = tabla.fetchall()
    tabla.close()
    lista_productos.delete(0,END)
    for dato in datos:
        lista_productos.insert(END,str(dato[0])+"                   "+str(dato[1]))

    def mover_objeto():
        seleccion = lista_productos.curselection()
        if seleccion:
            objeto = lista_productos.get(seleccion)
            lista_ventas.insert(tk.END, objeto)
            
    def eliminar_objeto():
        seleccion = lista_ventas.curselection()
        if seleccion:
            lista_ventas.delete(seleccion)

    def guardar_contenido():
        doc = Document()
        elementos = lista_ventas.get(0, tk.END)
        for elemento in elementos:
            doc.add_paragraph(elemento)
        doc.save("ticket.docx")
        os.startfile("ticket.docx")

        tabla = conexion.cursor()
        tabla.execute("SELECT nombre, precio FROM productos ORDER BY nombre")
        datos = tabla.fetchall()
        tabla.close()
        lista_ventas.delete(0,END)

    boton_agregar = Button(frame_vender,text="Agregar a Lista",command=mover_objeto,font=("arial",14),bg="#E6D90F",relief=RAISED,width=30,height=1)
    boton_agregar.place(x=450,y=360)

    boton_eliminar = Button(frame_vender,text="Eliminar de la Lista",command=eliminar_objeto,font=("arial",14),bg="#E6D90F",relief=RAISED,width=30,height=1)
    boton_eliminar.place(x=450,y=410)

    boton_vender = Button(frame_vender,text="Vender Productos",command=guardar_contenido,font=("arial",14),bg="#E6D90F",relief=RAISED,width=30,height=1)
    boton_vender.place(x=450,y=455)

    def volver():
        frame_vender.destroy()
        lista_productos.destroy()
        lista_ventas.destroy()
        
    boton_volver = Button(frame_vender,text="Volver ⬅",command=volver,font=("arial",14),bg="#E6D90F",relief=RAISED,width=10,height=1)
    boton_volver.place(x=1,y=1)

#funciones

#tabla
#agregar producto
def agregarp():
    frame_agregar = Frame(ventana)
    frame_agregar.place(x=230,y=0)
    frame_agregar.config(bg="#00A2E8",width=570,height=500)

    nombre = Label(frame_agregar,text="Nombre:",bg="#00A2E8",fg="black",font=("arial",20))
    nombre.place(x=100,y=100)

    nombre_entry = Entry(frame_agregar,font=("arial",14))
    nombre_entry.place(x=260,y=107)
    
    precio = Label(frame_agregar,text="Precio:",bg="#00A2E8",fg="black",font=("arial",20))
    precio.place(x=100,y=200)

    precio_entry = Entry(frame_agregar,font=("arial",14))
    precio_entry.place(x=258,y=207)

    stock=Label(frame_agregar,text="Stock:",bg="#00A2E8",fg="black",font=("arial",20))
    stock.place(x=100,y=300)

    stock_entry = Entry(frame_agregar,font=("arial",14))
    stock_entry.place(x=256,y=307)

    def aceptar():
        if nombre_entry.get() != "" and precio_entry.get() != "" and stock_entry.get() != "":
            datos=(nombre_entry.get(),precio_entry.get(),stock_entry.get())
            tabla = conexion.cursor()
            tabla.execute("INSERT INTO productos (nombre,precio,stock) VALUES(?,?,?)",datos)
            conexion.commit()
            tabla.close()   
            nombre_entry.delete(0,END)
            precio_entry.delete(0,END)
            stock_entry.delete(0,END)
            messagebox.showinfo("Agregar","Producto guardado correctamente")
        else:
            messagebox.showerror("ERROR", "Debe completar los campos correspondientes")

    boton_aceptar = Button(frame_agregar,text="Aceptar ✓",command=aceptar,font=("arial",14),bg="#3EEC0A",fg="black",relief=RAISED,width=20,height=2)
    boton_aceptar.place(x=150,y=400)

    def volver():
        frame_agregar.destroy()

    boton_volver = Button(frame_agregar,text="Volver ⬅",command=volver,font=("arial",14),bg="#E6D90F",relief=RAISED,width=10,height=1)
    boton_volver.place(x=1,y=1)

#Actualizar
def actualizar():
    frame_actualizar = Frame(ventana)
    frame_actualizar.place(x=230,y=0)
    frame_actualizar.config(bg="#00A2E8",width=570,height=500)

    nombre = Label(frame_actualizar,text="Nombre de Producto:",bg="#00A2E8",fg="black",font=("arial",20))
    nombre.place(x=15,y=40)

    nombre_actualiz_entry = Entry(frame_actualizar,font=("arial",14))
    nombre_actualiz_entry.place(x=300,y=50)

    def buscar():
        if(nombre_actualiz_entry.get() != ""):
            buscar_nombre = (nombre_actualiz_entry.get(),)
            tablame=conexion.cursor()
            tablame.execute("SELECT * FROM productos WHERE nombre=?",(buscar_nombre))
            buscar_datos = tablame.fetchall()
            tablame.close()
            nombre_nuevo_entry.delete(0,END)
            precio_nuevo_entry.delete(0,END)
            stock_nuevo_entry.delete(0,END)
            id_entry.delete(0,END)
        else:
            messagebox.showerror("ERROR", "Debe completar los campos correspondientes")

        for fila in buscar_datos:
            id_entry.insert(END,fila[0])
            nombre_nuevo_entry.insert(END,fila[1])
            precio_nuevo_entry.insert(END,fila[2])
            stock_nuevo_entry.insert(END,fila[3])


    boton_buscar = Button(frame_actualizar,text="Buscar 🔎",command=buscar,font=("arial",14),bg="#3EEC0A",fg="black",relief=RAISED,width=20,height=2)
    boton_buscar.place(x=150,y=140)
   

    nombre_nuevo = Label(frame_actualizar,text="Nombre:",bg="#00A2E8",fg="black",font=("arial",20))
    nombre_nuevo.place(x=80,y=250)

    nombre_nuevo_entry = Entry(frame_actualizar,font=("arial",14))
    nombre_nuevo_entry.place(x=220,y=257)

    precio=Label(frame_actualizar,text="Precio:",bg="#00A2E8",fg="black",font=("arial",20))
    precio.place(x=80,y=300)

    precio_nuevo_entry = Entry(frame_actualizar,font=("arial",14))
    precio_nuevo_entry.place(x=220,y=307)

    stock_nuevo=Label(frame_actualizar,text="Stock:",bg="#00A2E8",fg="black",font=("arial",20))
    stock_nuevo.place(x=80,y=350)

    stock_nuevo_entry = Entry(frame_actualizar,font=("arial",14))
    stock_nuevo_entry.place(x=220,y=357)
    id_entry = Entry(frame_actualizar,font=("arial",14),width=2)
    id_entry.place(x=250,y=80)
    
    def actualizar():
        if(nombre_actualiz_entry.get() != ""):
            tabla=conexion.cursor()
            modificardatos=(nombre_nuevo_entry.get(),precio_nuevo_entry.get(),stock_nuevo_entry.get(),id_entry.get())
            tabla.execute("UPDATE productos SET nombre=?,precio=?,stock=? WHERE id=?",(modificardatos))
            conexion.commit()
            tabla.close()
            messagebox.showinfo("Actualizar","Actualizado correctamente")
            nombre_nuevo_entry.delete(0,END)
            precio_nuevo_entry.delete(0,END)
            stock_nuevo_entry.delete(0,END)
            nombre_actualiz_entry.delete(0,END)
            id_entry.delete(0,END)

    boton_actualizar = Button(frame_actualizar,text="Actualizar ✓",command=actualizar,font=("arial",14),bg="#3EEC0A",fg="black",relief=RAISED,width=20,height=2)
    boton_actualizar.place(x=150,y=430)
    def volver():
        frame_actualizar.destroy()

    boton_volver = Button(frame_actualizar,text="Volver ⬅",command=volver,font=("arial",14),bg="#E6D90F",relief=RAISED,width=10,height=1)
    boton_volver.place(x=1,y=1)
#ver lista

def ver_lista():
    frame_lista = Frame(ventana)
    frame_lista.place(x=230,y=0)
    frame_lista.config(bg="#00A2E8",width=570,height=500)

    titulo = Label(frame_lista,text=" Nombre:          Precio:             Stock:",bg="#00A2E8",fg="black",font=("arial",20))
    titulo.place(x=1,y=50)
    lista = Listbox(frame_lista)
    lista.place(x=10, y=90,width=550,height=390)

    def listar():
        tabla = conexion.cursor()
        tabla.execute("SELECT nombre, precio, stock FROM productos ORDER BY nombre")
        conexion.commit()
        datos = tabla.fetchall()
        tabla.close()
        lista.delete(0,END)
        for dato in datos:
            lista.insert(END,str(dato[0])+"                                                      "+str(dato[1])+"                                                      "+str(dato[2]))
    def mostrar_datos():
        listar()
        ventana.after(1000, mostrar_datos)
    ventana.after(1000, mostrar_datos)
    def volver():
        frame_lista.place_forget()
    
    boton_volver = Button(frame_lista,text="Volver ⬅",command=volver,font=("arial",14),bg="#E6D90F",relief=RAISED,width=10,height=1)
    boton_volver.place(x=1,y=1)
#borrar
def borrar():
    frame_borrar = Frame(ventana)
    frame_borrar.place(x=230,y=0)
    frame_borrar.config(bg="#00A2E8",width=570,height=500)

    nombre = Label(frame_borrar,text="Nombre de Producto:",bg="#00A2E8",fg="black",font=("arial",20))
    nombre.place(x=15,y=40)

    nombre_actualiz_entry = Entry(frame_borrar,font=("arial",14))
    nombre_actualiz_entry.place(x=300,y=50)

    def borrar():
        if(nombre_actualiz_entry.get() != ""):
            tablame = conexion.cursor()
            borrardatos=(nombre_nuevo_entry.get(),)
            tablame.execute("DELETE FROM productos WHERE nombre=?",(borrardatos))
            conexion.commit()
            tablame.close()
            nombre_nuevo_entry.delete(0,END)
            precio_nuevo_entry.delete(0,END)
            messagebox.showinfo("Borrar","Producto borrado")
        else:
            messagebox.showwarning("Programa","Debe completar los campos")


    def buscar():
        if(nombre_actualiz_entry.get() != ""):
            buscar_nombrep=(nombre_actualiz_entry.get(),)
            tablame=conexion.cursor()
            tablame.execute("SELECT * FROM productos WHERE nombre=?",(buscar_nombrep))
            datos_buscar=tablame.fetchall()
            tablame.close()
            nombre_nuevo_entry.delete(0,END)
            precio_nuevo_entry.delete(0,END)
        else:
            messagebox.showerror("ERROR", "Debe completar los campos correspondientes")
        for fila in datos_buscar:
            nombre_nuevo_entry.insert(END,fila[1])
            precio_nuevo_entry.insert(END,fila[2])


                        
    boton_buscar = Button(frame_borrar,text="Buscar 🔎",command=buscar,font=("arial",14),bg="#3EEC0A",fg="black",relief=RAISED,width=20,height=2)
    boton_buscar.place(x=150,y=110)
   

    nombre_nuevo = Label(frame_borrar,text="Nombre:",bg="#00A2E8",fg="black",font=("arial",20))
    nombre_nuevo.place(x=80,y=200)

    nombre_nuevo_entry = Entry(frame_borrar,font=("arial",14))
    nombre_nuevo_entry.place(x=220,y=207)

    precio=Label(frame_borrar,text="Precio:",bg="#00A2E8",fg="black",font=("arial",20))
    precio.place(x=80,y=250)

    precio_nuevo_entry = Entry(frame_borrar,font=("arial",14))
    precio_nuevo_entry.place(x=220,y=257)

    boton_borrar = Button(frame_borrar,text=" Borrar 🗑️",command=borrar,font=("arial",14),bg="#FD0C00",fg="black",relief=RAISED,width=25,height=3)
    boton_borrar.place(x=120,y=350)
    def volver():
        frame_borrar.destroy()
        
    boton_volver = Button(frame_borrar,text="Volver ⬅",command=volver,font=("arial",14),bg="#E6D90F",relief=RAISED,width=10,height=1)
    boton_volver.place(x=1,y=1)

#cambiar color botones
##cambiar color y funcion de boton agregar
def cambiarcoloragregar():
    botonactualizarp.config(bg="grey")
    botonverlista.config(bg="grey")
    botonborrarp.config(bg="grey")
    botonagregarp.config(bg="#00A2E8")

def boton1():
    cambiarcoloragregar()
    agregarp()

##cambiar color y funcion de boton actualizar
def cambiarcoloractualizar():
    botonagregarp.config(bg="grey")
    botonverlista.config(bg="grey")
    botonborrarp.config(bg="grey")
    botonactualizarp.config(bg="#00A2E8")

def boton2():
    cambiarcoloractualizar()
    actualizar()



##cambiar color y funcion de boton ver lista
def cambiarcolorverlista():
    botonactualizarp.config(bg="grey")
    botonagregarp.config(bg="grey")
    botonborrarp.config(bg="grey")
    botonverlista.config(bg="#00A2E8")

def boton3():
    cambiarcolorverlista()
    ver_lista()

##cambiar color y funcion de boton borrar
def cambiarcolorborrar():
    botonagregarp.config(bg="grey")
    botonactualizarp.config(bg="grey")
    botonverlista.config(bg="grey")
    botonborrarp.config(bg="#00A2E8")

def boton4():
    cambiarcolorborrar()
    borrar()

#botones

botonagregarp = Button(ventana,text="Agregar Producto Nuevo",command=boton1,font=("arial",14),bg="#00A2E8",fg="black",relief=RAISED,width=20,height=5)
botonagregarp.place(x=0,y=0)


botonactualizarp = Button(ventana,text="Actualizar Producto",command=boton2,font=("arial",14),bg="#00A2E8",fg="black",relief=RAISED,width=20,height=5)
botonactualizarp.place(x=0,y=127)


botonverlista = Button(ventana,text="Ver Lista de Productos",command=boton3,font=("arial",14),bg="#00A2E8",fg="black",relief=RAISED,width=20,height=5)
botonverlista.place(x=0,y=254)

botonborrarp = Button(ventana,text="Borrar Producto",command=boton4,font=("arial",14),bg="#00A2E8",fg="black",relief=RAISED,width=20,height=5)
botonborrarp.place(x=0,y=381)

boton_vender = Button(ventana,text="Vender",command=vender,font=("arial",14),bg="#00A2E8",fg="black",relief=RAISED,width=20,height=2)
boton_vender.place(x=400,y=381)

ventana.mainloop()