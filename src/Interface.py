import Mensagem 
import tkinter as tk
from tkinter import ttk

class Interface(tk.TK)
    def __init__(self):
        super().__init__()
        self.title("Comunicação em Camadas")
        self.geometry("800x750")

        self.msg_criptografada_a = tk.StringVar()
        self.msg_binaria_a = tk.StringVar()
        self.sinal_amipseudo_a = tk.StringVar()

        self.sinal_amipseudo_b = tk.StringVar()
        self.msg_binaria_b = tk.StringVar()
        self.msg_criptografada_b = tk.StringVar()
        self.msg_final_b = tk.StringVar()
