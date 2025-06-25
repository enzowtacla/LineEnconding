import Mensagem
import tkinter as tk
from tkinter import ttk, messagebox
import socket
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HostA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Host A")
        self.geometry("1280x720")

        self.msg_criptografada = tk.StringVar()
        self.msg_binaria = tk.StringVar()
        self.msg_sinal_ami = tk.StringVar()

        self.criar_widgets()

    def criar_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        input_frame = ttk.LabelFrame(main_frame, text="Dados de Envio", padding="10")
        input_frame.pack(fill="x", pady=5)

        ttk.Label(input_frame, text="IP do Servidor:").grid(row=0, column=0, sticky="w", pady=5)
        self.ip_entry = ttk.Entry(input_frame, width=20)
        self.ip_entry.grid(row=0, column=1, sticky="w", pady=5)
        self.ip_entry.insert(0, "192.168.0.78")

        ttk.Label(input_frame, text="Mensagem:").grid(row=1, column=0, sticky="w", pady=5)
        self.msg_entry = ttk.Entry(input_frame, width=50)
        self.msg_entry.grid(row=1, column=1, pady=5)

        ttk.Label(input_frame, text="Chave de César:").grid(row=2, column=0, sticky="w", pady=5)
        self.chave_entry = ttk.Entry(input_frame, width=10)
        self.chave_entry.grid(row=2, column=1, sticky="w", pady=5)
        self.chave_entry.insert(0, "3")

        self.send_button = ttk.Button(input_frame, text="Enviar Mensagem", command=self.processar_e_enviar)
        self.send_button.grid(row=3, column=1, sticky="e", pady=10)
        
        results_frame = ttk.LabelFrame(main_frame, text="Etapas de Codificação (Antes do Envio)", padding="10")
        results_frame.pack(fill="x", pady=10)
  
        ttk.Label(results_frame, text="1. Texto Criptografado:", font="-weight bold").grid(row=0, column=0, sticky="w")
        ttk.Label(results_frame, textvariable=self.msg_criptografada, wraplength=600, foreground="blue").grid(row=1, column=0, sticky="w")
        ttk.Label(results_frame, text="2. Conversão para Binário:", font="-weight bold").grid(row=2, column=0, sticky="w", pady=(10,0))
        ttk.Label(results_frame, textvariable=self.msg_binaria, wraplength=600, foreground="blue").grid(row=3, column=0, sticky="w")
        ttk.Label(results_frame, text="3. Codificação de Linha:", font="-weight bold").grid(row=4, column=0, sticky="w", pady=(10,0))
        ttk.Label(results_frame, textvariable=self.msg_sinal_ami, wraplength=600, foreground="blue").grid(row=5, column=0, sticky="w")
        
        plot_frame_a = ttk.Frame(results_frame)
        plot_frame_a.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.fig_a = Figure(figsize=(8, 3), dpi=100)
        self.ax_ami = self.fig_a.add_subplot(111)
        self.fig_a.tight_layout(pad=3.0)

        self.canvas_a = FigureCanvasTkAgg(self.fig_a, master=plot_frame_a)
        self.canvas_a.get_tk_widget().pack()
        self.canvas_a.draw()

    def plotar_sinais_cliente(self, ami_data_list):
        self.ax_ami.clear()
        
        ami_data_list = ami_data_list[:64]
        time_steps = range(len(ami_data_list))
        
        self.ax_ami.step(time_steps, ami_data_list, where='post', color='r')
        self.ax_ami.set_title('Sinal Gerado')
        self.ax_ami.set_ylim(-1.5, 1.5)
        self.ax_ami.grid(True)
        
        self.canvas_a.draw()
    def processar_e_enviar(self):
        server_ip = self.ip_entry.get()
        mensagem = self.msg_entry.get()
        try:
            chave = int(self.chave_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "A chave deve ser um número inteiro.")
            return

        if not all([server_ip, mensagem]):
            messagebox.showerror("Erro", "Preencha o IP do servidor e a mensagem.")
            return

        texto_cifrado = Mensagem.criptografar(mensagem, chave)
        binario = Mensagem.string_para_binario(texto_cifrado)
        sinal_ami = Mensagem.codifica_amipseudo(binario)
        
        self.msg_criptografada.set(texto_cifrado)
        self.msg_binaria.set(binario)
        sinal_ami_str = " ".join(["+" if p > 0 else "-" if p < 0 else "0" for p in sinal_ami])
        self.msg_sinal_ami.set(sinal_ami_str)


        self.plotar_sinais_cliente(sinal_ami)

        PORT = 65432
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_ip, PORT))
                pacote = {"chave": chave, "sinal_ami": sinal_ami}
                dados_para_enviar = json.dumps(pacote).encode('utf-8')
                s.sendall(dados_para_enviar)
                messagebox.showinfo("Sucesso", "Mensagem enviada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao servidor.\nVerifique o IP e o Firewall.\n\nErro: {e}")

if __name__ == "__main__":
    app = HostA()
    app.mainloop()