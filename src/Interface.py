# Interface.py - VERSÃO CORRIGIDA

import Mensagem 
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comunicação em Camadas")
        self.geometry("1000x900")

        self.msg_criptografada_a = tk.StringVar()
        self.msg_binaria_a = tk.StringVar()
        self.sinal_amipseudo_a = tk.StringVar()

        self.sinal_amipseudo_b = tk.StringVar()
        self.msg_binaria_b = tk.StringVar()
        self.msg_criptografada_b = tk.StringVar()
        self.msg_final_b = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Frame do Host A
        host_a_frame = ttk.LabelFrame(main_frame, text="Host A", padding="10")
        host_a_frame.pack(fill="x", expand=True, pady=5)

        #Entrada de texto A
        ttk.Label(host_a_frame, text="Digite a mensagem:").grid(row=0, column=0, sticky="w", pady=2)
        self.msg_entry = ttk.Entry(host_a_frame, width=80)
        self.msg_entry.grid(row=0, column=1, pady=2, columnspan=2)
        ttk.Label(host_a_frame, text="Deslocamento:").grid(row=1, column=0, sticky="w", pady=2)
        self.chave_entry = ttk.Entry(host_a_frame, width=10)
        self.chave_entry.grid(row=1, column=1, sticky="w", pady=2)
        self.chave_entry.insert(0, "3")
        send_button = ttk.Button(host_a_frame, text="Criptografar e Enviar", command=self.processar_e_enviar)
        send_button.grid(row=1, column=2, sticky="e", pady=10)
        ttk.Label(host_a_frame, text="Mensagem Criptografada:", font="-weight bold").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Label(host_a_frame, textvariable=self.msg_criptografada_a, wraplength=600, foreground="blue").grid(row=3, column=0, columnspan=3, sticky="w")
        ttk.Label(host_a_frame, text="Conversão para Binário:", font="-weight bold").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Label(host_a_frame, textvariable=self.msg_binaria_a, wraplength=700, foreground="blue").grid(row=5, column=0, columnspan=3, sticky="w")
        ttk.Label(host_a_frame, text="Codificação de Linha (Ami Pseudoternário):", font="-weight bold").grid(row=6, column=0, sticky="w", pady=5)
        ttk.Label(host_a_frame, textvariable=self.sinal_amipseudo_a, wraplength=700, foreground="blue").grid(row=7, column=0, columnspan=3, sticky="w")

        # Gráfico do Host A
        plot_frame_a = ttk.Frame(host_a_frame)
        plot_frame_a.grid(row=8, column=0, columnspan=3, pady=10)

        self.fig_a = Figure(figsize=(9, 3), dpi=100)
        self.ax_bin_a, self.ax_ami_a = self.fig_a.subplots(1, 2)
        self.fig_a.tight_layout(pad=3.0)
        self.canvas_a = FigureCanvasTkAgg(self.fig_a, master=plot_frame_a)
        self.canvas_a.get_tk_widget().pack()
        self.canvas_a.draw()

        #Entrada de texto B
        host_b_frame = ttk.LabelFrame(main_frame, text=" Host B", padding="10")
        host_b_frame.pack(fill="x", expand=True, pady=15)
        ttk.Label(host_b_frame, text="4. Sinal Recebido (Simulado):", font="-weight bold").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Label(host_b_frame, textvariable=self.sinal_amipseudo_b, wraplength=700, foreground="green").grid(row=1, column=0, columnspan=3, sticky="w")
        ttk.Label(host_b_frame, text="5. Binário Decodificado:", font="-weight bold").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Label(host_b_frame, textvariable=self.msg_binaria_b, wraplength=700, foreground="green").grid(row=3, column=0, columnspan=3, sticky="w")
        ttk.Label(host_b_frame, text="6. Texto Cifrado Recuperado:", font="-weight bold").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Label(host_b_frame, textvariable=self.msg_criptografada_b, wraplength=600, foreground="green").grid(row=5, column=0, columnspan=3, sticky="w")
        ttk.Label(host_b_frame, text="7. Mensagem Final Descriptografada:", font="-weight bold").grid(row=6, column=0, sticky="w", pady=5)
        ttk.Label(host_b_frame, textvariable=self.msg_final_b, wraplength=600, font="-size 12 -weight bold", foreground="red").grid(row=7, column=0, columnspan=3, sticky="w")

        # Gráfico do Host B
        plot_frame_b = ttk.Frame(host_b_frame)
        plot_frame_b.grid(row=8, column=0, columnspan=3, pady=10)

        self.fig_b = Figure(figsize=(9, 3), dpi=100)
        self.ax_ami_b, self.ax_bin_b = self.fig_b.subplots(1, 2)
        self.fig_b.tight_layout(pad=3.0)
        self.canvas_b = FigureCanvasTkAgg(self.fig_b, master=plot_frame_b)
        self.canvas_b.get_tk_widget().pack()
        self.canvas_b.draw()
    
    def plotar_sinais(self, seq_binaria, sinal_amipseudo, bin_decod, ami_recebido):
        
        self.ax_ami_a.clear()
        self.ax_bin_a.clear()
        self.ax_ami_b.clear()
        self.ax_bin_b.clear()

        # Converte as strings de bits para listas de inteiros para plotagem
        bin_data_int = [int(bit) for bit in seq_binaria]
        bin_decod_int = [int(bit) for bit in bin_decod]

        # Limita os dados para melhor visualização
        bin_data_int = bin_data_int[:128]
        sinal_amipseudo = sinal_amipseudo[:128]
        bin_decod_int = bin_decod_int[:128]
        ami_recebido = ami_recebido[:128]
        
        time_steps = range(len(bin_data_int))

        # Desenha o gráfico do Binário Original (Host A)
        self.ax_bin_a.step(time_steps, bin_data_int, where='post', color='b')
        self.ax_bin_a.set_title('Sinal Binário (Host A)')
        self.ax_bin_a.set_ylim(-0.2, 1.2)
        self.ax_bin_a.grid(True)

        # Desenha o gráfico do Sinal AMI (Host A)
        self.ax_ami_a.step(time_steps, sinal_amipseudo, where='post', color='r')
        self.ax_ami_a.set_title('Onda AMI (Host A)')
        self.ax_ami_a.set_ylim(-1.5, 1.5)
        self.ax_ami_a.axhline(0, color='grey', linestyle='--')
        self.ax_ami_a.grid(True)

        # Desenha o gráfico do Sinal AMI Recebido (Host B)
        self.ax_ami_b.step(range(len(ami_recebido)), ami_recebido, where='post', color='g')
        self.ax_ami_b.set_title('Onda AMI Recebida (Host B)')
        self.ax_ami_b.set_ylim(-1.5, 1.5)
        self.ax_ami_b.axhline(0, color='grey', linestyle='--')
        self.ax_ami_b.grid(True)

        # Desenha o gráfico do Binário Decodificado (Host B)
        self.ax_bin_b.step(range(len(bin_decod_int)), bin_decod_int, where='post', color='purple')
        self.ax_bin_b.set_title('Sinal Binário Decodificado (Host B)')
        self.ax_bin_b.set_ylim(-0.2, 1.2)
        self.ax_bin_b.grid(True)

        # Atualiza a tela para mostrar os gráficos
        self.canvas_a.draw()
        self.canvas_b.draw()

    def processar_e_enviar(self):

        self.sinal_amipseudo_b.set("")
        self.msg_binaria_b.set("")
        self.msg_criptografada_b.set("")
        self.msg_final_b.set("")

        mensagem_original = self.msg_entry.get()
        try:
            chave = int(self.chave_entry.get())
        except ValueError:
            self.msg_criptografada_a.set("Chave inválida")
            return

        if not mensagem_original:
            self.msg_criptografada_a.set("Mensagem vazia")
            return
    
        texto_criptografado = Mensagem.criptografar(mensagem_original, chave)
        self.msg_criptografada_a.set(texto_criptografado)

        seq_binaria = Mensagem.string_para_binario(texto_criptografado)
        self.msg_binaria_a.set(seq_binaria)

        sinal_amipseudo = Mensagem.codifica_amipseudo(seq_binaria)
        sinal_ami_str = " ".join(["+" if p > 0 else "-" if p < 0 else "0" for p in sinal_amipseudo])
        self.sinal_amipseudo_a.set(sinal_ami_str)

        sinal_recebido = sinal_amipseudo
        self.sinal_amipseudo_b.set(sinal_ami_str)

        seq_decodificada = Mensagem.decodifica_amipseudo(sinal_recebido)
        self.msg_binaria_b.set(seq_decodificada)

        texto_recuperado = Mensagem.binario_para_string(seq_decodificada)
        self.msg_criptografada_b.set(texto_recuperado)
    
        texto_descriptografado = Mensagem.descriptografar(texto_recuperado, chave)
        self.msg_final_b.set(texto_descriptografado)

        self.plotar_sinais(seq_binaria, sinal_amipseudo, seq_decodificada, sinal_recebido)

if __name__ == "__main__":
    app = Interface()
    app.mainloop()