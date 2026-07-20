import customtkinter as ctk
from datetime import datetime, date, timedelta
from calendar import monthrange

# Mapeamento robusto para Português (para evitar problemas de locale em diferentes SOs)
# Note: monthrange retorna o dia da semana do primeiro dia do mês (0=Seg, 6=Dom)
MESES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

class CTkDatePicker(ctk.CTkFrame):
    """
    Um widget de seleção de data (calendário) para CustomTkinter.
    Substitui a entrada de data por um botão que abre um calendário pop-up.
    """
    def __init__(self, master, width=220, height=30, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        
        # 1. Variáveis de Estado
        self.current_date = date.today() # Mês atualmente exibido no calendário
        self.selected_date = date.today() # Data selecionada (valor da entrada)
        self.callback = None
        self.width = width
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Entrada e Botão Principal
        self.entry_var = ctk.StringVar(value=self.selected_date.strftime("%d/%m/%Y"))
        
        # A entrada agora é um 'label' com aparência de entry, garantindo que seja 'readonly'
        self.date_label = ctk.CTkLabel(self, textvariable=self.entry_var, width=width - 35, 
                                       fg_color=ctk.ThemeManager.theme['CTkEntry']['fg_color'], 
                                       text_color=ctk.ThemeManager.theme['CTkEntry']['text_color'],
                                       corner_radius=ctk.ThemeManager.theme['CTkEntry']['corner_radius'],
                                       anchor='w', padx=5)
        self.date_label.grid(row=0, column=0, sticky="ew", padx=(0, 0))
        
        self.button = ctk.CTkButton(self, text="🗓", width=35, command=self._open_calendar)
        self.button.grid(row=0, column=1, padx=(0, 0), sticky="e")

        # 3. Janela Toplevel do Calendário
        self.calendar_toplevel = None

    def _open_calendar(self):
        """Abre o widget de calendário Toplevel."""
        if self.calendar_toplevel is None or not self.calendar_toplevel.winfo_exists():
            self.calendar_toplevel = ctk.CTkToplevel(self) 
            self.calendar_toplevel.title("Selecionar Data")
            self.calendar_toplevel.attributes("-topmost", True)
            self.calendar_toplevel.resizable(False, False)
            
            # Centralizar o calendário perto do widget pai
            self.update_idletasks()
            # Posição X: Alinhar com a esquerda do widget pai
            x = self.winfo_rootx() 
            # Posição Y: Abaixo do widget pai
            y = self.winfo_rooty() + self.winfo_height() + 5
            self.calendar_toplevel.geometry(f"+{x}+{y}") 
            
            # Garante que o toplevel feche corretamente
            self.calendar_toplevel.protocol("WM_DELETE_WINDOW", self._close_calendar)
            
            self._draw_calendar_widgets()
            self._update_calendar()
            self.calendar_toplevel.focus_set()
        else:
            self.calendar_toplevel.lift()

    def _close_calendar(self):
        """Fecha o widget de calendário Toplevel."""
        if self.calendar_toplevel and self.calendar_toplevel.winfo_exists():
            self.calendar_toplevel.destroy()
            self.calendar_toplevel = None

    def _draw_calendar_widgets(self):
        """Desenha os elementos de navegação e a grelha de dias."""
        calendar_frame = ctk.CTkFrame(self.calendar_toplevel)
        calendar_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Frame de Navegação (Mês/Ano)
        nav_frame = ctk.CTkFrame(calendar_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkButton(nav_frame, text="<", width=30, command=lambda: self._change_month(-1)).pack(side="left", padx=(0, 5))
        
        self.month_year_label = ctk.CTkLabel(nav_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.month_year_label.pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(nav_frame, text=">", width=30, command=lambda: self._change_month(1)).pack(side="left", padx=(5, 0))

        # Frame da Grelha do Calendário
        self.day_grid_frame = ctk.CTkFrame(calendar_frame, fg_color="transparent")
        self.day_grid_frame.pack(fill="both", expand=True)

        # Cabeçalhos dos Dias da Semana (Seg a Dom)
        dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        for i, dia in enumerate(dias_semana):
            label = ctk.CTkLabel(self.day_grid_frame, text=dia, font=ctk.CTkFont(size=10, weight="bold"))
            self.day_grid_frame.grid_columnconfigure(i, weight=1)
            label.grid(row=0, column=i, padx=2, pady=2)
            
    def _change_month(self, delta):
        """Muda o mês atual para exibição."""
        # Cria um novo objeto date 32 dias no futuro/passado e retorna ao 1º dia
        new_date = self.current_date.replace(day=1) + timedelta(days=32 * delta)
        self.current_date = new_date.replace(day=1)
        self._update_calendar()

    def _select_day(self, day):
        """Define o dia selecionado e atualiza a entrada."""
        self.selected_date = self.current_date.replace(day=day)
        self._update_entry()
        self._close_calendar()
        if self.callback:
            self.callback()

    def _update_calendar(self):
        """Atualiza a grelha com os dias do mês atual."""
        
        # Limpar apenas os botões de dia (mantendo os cabeçalhos)
        for widget in self.day_grid_frame.winfo_children():
            # A linha 0 é o cabeçalho, então destruímos tudo a partir da linha 1
            if int(widget.grid_info()['row']) > 0:
                widget.destroy()

        # Atualizar Mês/Ano (Usando o array em Português)
        mes_pt = MESES_PT[self.current_date.month - 1]
        self.month_year_label.configure(text=f"{mes_pt} de {self.current_date.year}")

        # Informações do Mês
        year, month = self.current_date.year, self.current_date.month
        num_days = monthrange(year, month)[1]
        
        # O dia da semana do 1º dia do mês (0=Seg, 6=Dom)
        start_day_of_week = date(year, month, 1).weekday() 

        row = 1 # Começa na segunda linha (abaixo dos cabeçalhos)
        col = start_day_of_week
        
        for day in range(1, num_days + 1):
            day_date = date(year, month, day)
            is_selected = day_date == self.selected_date
            is_today = day_date == date.today()
            
            # --- Lógica de Cores ---
            fg_color = "transparent"
            text_color = ctk.ThemeManager.theme['CTkLabel']['text_color'] # Padrão
            
            if is_selected:
                fg_color = ctk.ThemeManager.theme['CTkButton']['fg_color'] # Cor principal do tema (Azul)
                text_color = ctk.ThemeManager.theme['CTkButton']['text_color']
            elif is_today:
                # Usando cores baseadas no tema, mas levemente mais escuras/claras
                fg_color = ("#444444", "#555555") 
                
            btn = ctk.CTkButton(self.day_grid_frame, 
                                text=str(day), 
                                width=35, height=30, 
                                command=lambda d=day: self._select_day(d),
                                fg_color=fg_color,
                                text_color=text_color,
                                hover_color=ctk.ThemeManager.theme['CTkButton']['hover_color'],
                                font=ctk.CTkFont(weight="bold" if is_selected else "normal"))
            
            btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            
            col += 1
            if col > 6:
                col = 0
                row += 1

    def _update_entry(self):
        """Atualiza a entrada de texto do widget principal com a data selecionada."""
        self.entry_var.set(self.selected_date.strftime("%d/%m/%Y"))

    # --- Métodos Públicos ---

    def set_date(self, new_date: date):
        """Define a data inicial do widget."""
        self.selected_date = new_date
        self.current_date = new_date.replace(day=1) # O mês exibido começa no mês da data selecionada, mas no 1º dia
        self._update_entry()

    def get_date(self) -> date:
        """Retorna a data selecionada como um objeto date."""
        return self.selected_date
        
    def get_date_str(self) -> str:
        """Retorna a data selecionada no formato DD/MM/AAAA."""
        return self.selected_date.strftime("%d/%m/%Y")
        
    def set_callback(self, func):
        """Define uma função de callback para ser chamada ao selecionar uma data."""
        self.callback = func

# Exemplo de uso (opcional para testar o widget isoladamente)
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Teste do CTkDatePicker")
    app.geometry("400x200")
    
    def on_date_select():
        print(f"Nova data selecionada: {date_picker.get_date_str()}")
        
    date_picker = CTkDatePicker(app, width=250)
    date_picker.pack(padx=50, pady=50)
    date_picker.set_callback(on_date_select)

    app.mainloop()