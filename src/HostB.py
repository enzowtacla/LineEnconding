import Mensagem
import tkinter as tk
from tkinter import ttk, scrolledtext
import socket
import threading
import json
import queue
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def obter_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class HostB(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Host B")
        self.geometry("800x800")

        self.sinal_ami_b = tk.StringVar()
        self.msg_binaria_b = tk.StringVar()
        self.msg_criptografada_b = tk.StringVar()
        self.msg_final_b = tk.StringVar()
        self.log_queue = queue.Queue()

        self.create_widgets()
        self.verificar_fila()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Servidor", padding="10")
        info_frame.pack(fill="x", pady=5)

        ip_local = obter_ip_local()
        ttk.Label(info_frame, text=f"IP deste Servidor:", font="-weight bold").pack(side="left")
        ttk.Label(info_frame, text=f"{ip_local}", foreground="blue", font="-size 12 -weight bold").pack(side="left", padx=5)
        self.start_button = ttk.Button(info_frame, text="Iniciar Servidor", command=self.iniciar_servidor_thread)
        self.start_button.pack(side="right")
        
        results_frame = ttk.LabelFrame(main_frame, text="Dados Recebidos", padding="10")
        results_frame.pack(fill="x", pady=10)
        ttk.Label(results_frame, text="1. Sinal AMI Recebido:", font="-weight bold").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Label(results_frame, textvariable=self.sinal_ami_b, wraplength=600, foreground="green").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Label(results_frame, text="2. Binário Decodificado:", font="-weight bold").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Label(results_frame, textvariable=self.msg_binaria_b, wraplength=600, foreground="green").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Label(results_frame, text="3. Texto Recuperado:", font="-weight bold").grid(row=4, column=0, sticky="w", pady=2)
        ttk.Label(results_frame, textvariable=self.msg_criptografada_b, wraplength=600, foreground="green").grid(row=5, column=0, sticky="w", pady=5)
        ttk.Label(results_frame, text="4. Mensagem Final:", font="-weight bold").grid(row=6, column=0, sticky="w", pady=2)
        ttk.Label(results_frame, textvariable=self.msg_final_b, wraplength=600, font="-size 14 -weight bold", foreground="red").grid(row=7, column=0, sticky="w", pady=5)
       
        plot_frame_b = ttk.Frame(results_frame)
        plot_frame_b.grid(row=8, column=0, pady=10)
        self.fig_b = Figure(figsize=(8, 3), dpi=100)
        self.ax_ami = self.fig_b.add_subplot(111)
        self.fig_b.tight_layout(pad=3.0)
        self.canvas_b = FigureCanvasTkAgg(self.fig_b, master=plot_frame_b)
        self.canvas_b.get_tk_widget().pack()
        self.canvas_b.draw()
        log_frame = ttk.LabelFrame(main_frame, text="Log de Atividade", padding="10")
        log_frame.pack(fill="both", expand=True, pady=5)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=3, state="disabled")
        self.log_text.pack(fill="both", expand=True)
    
    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)
    
    def plotar_sinais_servidor(self, ami_data_list):
        self.ax_ami_b.clear()
        ami_data_list = ami_data_list[:64]
        time_steps = range(len(ami_data_list))
        self.ax_ami_b.step(time_steps, ami_data_list, where='post', color='red')
        self.ax_ami_b.set_title('Onda Recebida')
        self.ax_ami_b.set_ylim(-1.5, 1.5)
        self.ax_ami_b.grid(True)
        self.canvas_b.draw()
        
    def verificar_fila(self):
        try:
            while True:
                data = self.log_queue.get_nowait()
                if "log" in data:
                    self.log(data["log"])

                if "final" in data:
                    self.sinal_ami_b.set(data["sinal_str"])
                    self.msg_binaria_b.set(data["binario"])
                    self.msg_criptografada_b.set(data["cifrado"])
                    self.msg_final_b.set(data["final"])
                    self.plotar_sinais_servidor(data["plot_ami"])

        except queue.Empty:
            pass
        self.after(100, self.verificar_fila)

    def iniciar_servidor_thread(self):
        self.start_button.config(state="disabled", text="Servidor Rodando...")
        server_thread = threading.Thread(target=self.rodar_servidor, daemon=True)
        server_thread.start()

    def rodar_servidor(self):
        HOST = '0.0.0.0'
        PORT = 65432
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            self.log_queue.put({"log": f"Servidor escutando em {obter_ip_local()}:{PORT}"})
            while True:
                conn, addr = s.accept()
                with conn:
                    self.log_queue.put({"log": f"Conectado por {addr}"})
                    data_recebida_bytes = conn.recv(4096)
                    if not data_recebida_bytes: continue

                    data_recebida_str = data_recebida_bytes.decode('utf-8')
                    pacote = json.loads(data_recebida_str)
                    chave = pacote['chave']
                    sinal_ami = pacote['sinal_ami']
                    
                    sinal_ami_str = " ".join(["+" if p > 0 else "-" if p < 0 else "0" for p in sinal_ami])
                    binario_decodificado = Mensagem.decodifica_amipseudo(sinal_ami)
                    texto_cifrado = Mensagem.binario_para_string(binario_decodificado)
                    texto_final = Mensagem.descriptografar(texto_cifrado, chave)
                    
                    self.log_queue.put({
                        "sinal_str": sinal_ami_str,
                        "binario": binario_decodificado,
                        "cifrado": texto_cifrado,
                        "final": texto_final,
                        "plot_ami": sinal_ami,
                        "plot_bin": binario_decodificado,
                        "log": "Mensagem processada com sucesso!"
                    })

if __name__ == "__main__":
    app = HostB()
    app.mainloop()