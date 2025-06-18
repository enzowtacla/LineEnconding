# Interface.py - VERSÃO CORRIGIDA

import Mensagem 
import tkinter as tk
from tkinter import ttk

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comunicação em Camadas")
        self.geometry("1280x720")

        # Nomes das variáveis estão corretos aqui
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

        host_a_frame = ttk.LabelFrame(main_frame, text="Host A", padding="10")
        host_a_frame.pack(fill="x", expand=True, pady=5)

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

    def processar_e_enviar(self):
        # Limpa os campos de resultado
        self.sinal_amipseudo_b.set("")
        self.msg_binaria_b.set("")
        self.msg_criptografada_b.set("")
        self.msg_final_b.set("")

        # Pega os dados da interface
        mensagem_original = self.msg_entry.get()
        try:
            chave = int(self.chave_entry.get())
        except ValueError:
            self.msg_criptografada_a.set("Chave inválida")
            return

        if not mensagem_original:
            self.msg_criptografada_a.set("Mensagem vazia")
            return
    
        # ---- ETAPAS DO HOST A ----
        texto_criptografado = Mensagem.criptografar(mensagem_original, chave)
        self.msg_criptografada_a.set(texto_criptografado)

        seq_binaria = Mensagem.string_to_binario(texto_criptografado)
        self.msg_binaria_a.set(seq_binaria)

        sinal_amipseudo = Mensagem.codifica_amipseudo(seq_binaria)
        # CORREÇÃO 2: Formatar a lista para uma string antes de exibir
        sinal_ami_str = " ".join(["+" if p > 0 else "-" if p < 0 else "0" for p in sinal_amipseudo])
        # CORREÇÃO 1: Usar o nome correto da variável
        self.sinal_amipseudo_a.set(sinal_ami_str)

        # ---- SIMULAÇÃO DE "ENVIO" ----
        sinal_recebido = sinal_amipseudo
        self.sinal_amipseudo_b.set(sinal_ami_str)

        # ---- ETAPAS DO HOST B ----
        seq_decodificada = Mensagem.decodifica_amipseudo(sinal_recebido)
        self.msg_binaria_b.set(seq_decodificada)

        # CORREÇÃO 3: Adicionar a etapa que faltava de converter binário para texto
        def binario_para_string(b): # Função auxiliar
            return "".join([chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8)])
        
        texto_cifrado_recuperado = binario_para_string(seq_decodificada)
        self.msg_criptografada_b.set(texto_cifrado_recuperado)

        # Agora sim, descriptografa o TEXTO recuperado, e não o binário
        texto_final = Mensagem.descriptografar(texto_cifrado_recuperado, chave)
        self.msg_final_b.set(texto_final)


if __name__ == "__main__":
    app = Interface()
    app.mainloop()