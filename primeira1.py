from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

root = Tk()

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont("Helvetica", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 26)
        self.c.drawString(50, 700, "Código: ")
        self.c.drawString(50, 660, "Nome: ")
        self.c.drawString(50, 620, "Telefone: ")
        self.c.drawString(50, 580, "Cidade: ")

        self.c.setFont("Helvetica", 26)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 660, self.nomeRel)
        self.c.drawString(170, 620, self.telefoneRel)
        self.c.drawString(150, 580, self.cidadeRel)

        self.c.rect(20, 550, 550, 20, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs:
    def limpar_cliente(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
    def connecta_bd(self):
        self.conn = sqlite3.connect('Clientes.db')
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.connecta_bd(); 
        ### Criar tabela
        self.cursor.execute("""   
             CREATE TABLE IF NOT EXISTS clientes(
                 cod INTEGER PRIMARY KEY,
                 nome_cliente CHAR(40) NOT NULL,
                 telefone INTEGER(20),
                 cidade CHAR(40)
            );
        """)
        self.conn.commit(); print('Banco de dados criado')
        self.desconecta_bd()
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
    def add_cliente(self):
        self.variaveis()
        self.connecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
            VALUES (?, ?, ?) """, (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_cliente()
    def select_lista(self):
        self.listacliente.delete(*self.listacliente.get_children())
        self.connecta_bd()

        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes ORDER BY nome_cliente ASC;  """)
        for i in lista:
            self.listacliente.insert("", END, values=i)
        self.desconecta_bd()
    def OnDoubleClick(self, event):
        self.limpar_cliente()
        self.listacliente.selection()

        for n in self.listacliente.selection():
            col1, col2, col3, col4 = self.listacliente.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    def deletar_clientes(self):
        self.variaveis()
        self.connecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_cliente()
        self.select_lista()
    def alterar_cliente(self):
        self.variaveis()
        self.connecta_bd()
        self.cursor.execute("""UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ? WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_cliente()
    def buscar_cliente(self):
        self.connecta_bd()
        self.listacliente.delete(*self.listacliente.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes WHERE nome_cliente LIKE  '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listacliente.insert("", END, values=i)
        self.limpar_cliente()
        self.desconecta_bd()
class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
        
    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='#3A3EF0')
        self.root.geometry('600x500')
        self.root.resizable(True, True)
        self.root.maxsize(width=2000, height=1500)
        self.root.minsize(width=500, height=300)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#0094F0', highlightbackground='#4C82F0', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.45)
        self.frame_2 = Frame(self.root, bd=4, bg='#0094F0', highlightbackground='#4C82F0', highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        self.canvas_bt = Canvas(self.frame_1, bd=0, bg='#2C97F5', highlightbackground='gray', highlightthickness=5)
        self.canvas_bt.place(relx=0.19,rely=0.08, relwidth=0.22, relheight=0.19)

        self.bt_limpar = Button(self.frame_1,text="Limpar", bg='#2777F0', fg='#E6EEF1', activebackground='#4C68F5', activeforeground='white', font= ('verdana', 8, 'bold'), command=self.limpar_cliente)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_buscar = Button(self.frame_1, text="Buscar", bg='#2777F0', fg='#E6EEF1', font= ('verdana', 8, 'bold'), command=self.buscar_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        
        self.bt_novo = Button(self.frame_1, text='Novo', bg='#2777F0', fg='#E6EEF1', font= ('verdana', 8, 'bold'), command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15,)

        self.bt_alterar = Button(self.frame_1, text='Alterar', bg='#2777F0', fg='#E6EEF1', font= ('verdana', 8, 'bold'), command=self.alterar_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_apagar = Button(self.frame_1, text='Apagar', bg='#2777F0', fg='#E6EEF1', font= ('verdana', 8, 'bold'), command=self.deletar_clientes)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        #criação de label e entrada do codigo
        self.lb_codigo = Label(self.frame_1, text='Código', bg='#0094F0', fg='#E6EEF1', font=('italac', 11))
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

        #criação de label e entrada do nome
        self.lb_nome = Label(self.frame_1, text='Nome', bg='#0094F0', fg='#E6EEF1', font=('italac', 11))
        self.lb_nome.place(relx=0.05, rely=0.35)
        
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.35)

        #criação da label e entrada do telefone
        self.lb_telefone = Label(self.frame_1, text='Telefone', bg='#0094F0', fg='#E6EEF1', font=('italac', 11))
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.3)

        #criação da label e entrada da cidade
        self.lb_cidade = Label(self.frame_1, text='Cidade', bg='#0094F0', fg='#E6EEF1', font=('italac', 11))
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)
    def lista_frame2(self):
        self.listacliente = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4"))
        self.listacliente.heading("#0", text="")
        self.listacliente.heading('#1', text='Código')
        self.listacliente.heading('#2', text='Nome')
        self.listacliente.heading('#3', text='Telefone')
        self.listacliente.heading('#4', text='Cidade')

        self.listacliente.column('#0', width=1)
        self.listacliente.column('#1', width=50)
        self.listacliente.column('#2', width=200)
        self.listacliente.column('#3', width=125)
        self.listacliente.column('#4', width=125)

        self.listacliente.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listacliente.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listacliente.bind("<Double-1>", self.OnDoubleClick )
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        def Quit(): self.root.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatórios", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpar Cliente", command=self.limpar_cliente)

        filemenu2.add_command(label="Ficha do Cliente", command=self.geraRelatCliente)



Application()



