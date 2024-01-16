import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import logging

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_entry = self.format(record) + '\n'
        self.text_widget.insert(tk.END, log_entry)
        self.text_widget.see(tk.END)

class IPFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Finder Infos")

        # Configuração do ícone para Windows
        try:
            self.root.iconbitmap("icon.ico")
        except tk.TclError:
            pass  # Ignora o erro se o ícone não puder ser carregado

        # Configuração das abas
        self.notebook = ttk.Notebook(root)
        self.tab_inicio = ttk.Frame(self.notebook)
        self.tab_sobre = ttk.Frame(self.notebook)
        self.tab_informacoes = ttk.Frame(self.notebook)
        self.tab_logs = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_inicio, text="Inicio")
        self.notebook.add(self.tab_sobre, text="Sobre")
        self.notebook.add(self.tab_informacoes, text="Informações")
        self.notebook.add(self.tab_logs, text="Logs")
        self.notebook.pack(expand=1, fill="both")

        # Configuração da aba Início
        self.label_titulo = tk.Label(self.tab_inicio, text="IP Finder Infos", font=("Helvetica", 16))
        self.label_titulo.pack(pady=10)

        self.entry_ip = tk.Entry(self.tab_inicio)
        self.entry_ip.pack(pady=10)

        self.btn_capturar = tk.Button(self.tab_inicio, text="Capturar informações", command=self.capturar_informacoes)
        self.btn_capturar.pack(pady=10)

        # Configuração da aba Sobre
        sobre_texto = (
            "Este programa captura informações sobre um endereço IP, incluindo Cidade, Região, Código postal, "
            "País, Continente, Coordenadas, Fuso horário, Hostname, Provedor e ASN.\n"
            "As informações dos IPs são extraídas a partir do site https://tools.keycdn.com/ Todos os créditos ao site."
        )
        self.label_sobre = tk.Label(self.tab_sobre, text=sobre_texto, wraplength=400, justify="left")
        self.label_sobre.pack(pady=10)

        # Configuração da aba Informações
        informacoes_texto = "Criado por Kensdy\nConfira o repositório em: https://github.com/kensdy/IP-Finder-Infos"
        self.label_informacoes = tk.Label(self.tab_informacoes, text=informacoes_texto, wraplength=400, justify="left", fg="blue", cursor="hand2")
        self.label_informacoes.pack(pady=10)
        self.label_informacoes.bind("<Button-1>", lambda e: self.abrir_link("https://github.com/kensdy/IP-Finder-Infos"))

        # Configuração da aba Logs
        self.log_text = scrolledtext.ScrolledText(self.tab_logs, wrap=tk.WORD, width=80, height=20)
        self.log_text.pack(padx=10, pady=10)

        # Configuração do logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        text_handler = TextHandler(self.log_text)
        self.logger.addHandler(text_handler)

    def capturar_informacoes(self):
        ip_address = self.entry_ip.get()

        url = f"https://tools.keycdn.com/geo?host={ip_address}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")

            location_info = soup.find_all("dl")[0]
            location_data = {}
            for dt, dd in zip(location_info.find_all("dt"), location_info.find_all("dd")):
                location_data[dt.text.strip()] = dd.text.strip()

            network_info = soup.find_all("dl")[1]
            network_data = {}
            for dt, dd in zip(network_info.find_all("dt"), network_info.find_all("dd")):
                network_data[dt.text.strip()] = dd.text.strip()

            info_text = "Localização:\n"
            for key, value in location_data.items():
                info_text += f"{key.replace(':', '')}: {value}\n"

            info_text += "\nRede:\n"
            for key, value in network_data.items():
                info_text += f"{key.replace(':', '')}: {value}\n"

            messagebox.showinfo("Informações", info_text)
            self.logger.info(f'Successful request to {url}')
        else:
            messagebox.showerror("Erro", f"Erro ao acessar o site. Código de status: {response.status_code}")
            self.logger.error(f'Error accessing {url}. Status code: {response.status_code}')

    def abrir_link(self, link):
        import webbrowser
        webbrowser.open_new(link)

if __name__ == "__main__":
    root = tk.Tk()
    app = IPFinderApp(root)
    root.mainloop()
