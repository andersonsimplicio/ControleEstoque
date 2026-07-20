# view/View.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime

# Importação Segura
try:
    from view.ctk_datepicker import CTkDatePicker
except ImportError:
    print("Aviso: DatePicker não encontrado, usando Entry.")
    CTkDatePicker = None

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Variáveis de Interface
        self.var_id_entrada = ctk.StringVar(master=self)
        self.var_desc_entrada = ctk.StringVar(master=self, value="Nenhuma peça selecionada")
        self.var_id_saida = ctk.StringVar(master=self)
        self.var_desc_saida = ctk.StringVar(master=self, value="Nenhuma peça selecionada")
        
        self.janelas = {} 
        
        self.title('Sistema de Estoque')
        self.geometry("1240x600")
        self.protocol("WM_DELETE_WINDOW", self.controller.fechar_aplicacao)
        
        # Delay seguro para desenhar
        self.after(100, self._criar_menu)

    def _criar_menu(self):
        # Limpa widgets anteriores
        for widget in self.pack_slaves(): widget.destroy()
        for widget in self.grid_slaves(): widget.destroy()
        # --- LOGOTIPO (EMOJI GIGANTE) ---
        # Usamos um emoji de "Prédio de Escritório" ou "Fábrica" para representar a empresa
        lbl_logo = ctk.CTkLabel(self, text="🏢", font=("Arial", 80)) 
        lbl_logo.pack(pady=(30, 0)) # Padding top 30, bottom 0 (colado no título)
        # Título Principal
        lbl_titulo = ctk.CTkLabel(self, text="Painel de Controle", font=ctk.CTkFont(size=28, weight="bold"))
        lbl_titulo.pack(pady=(5, 25))

        # Container Grid
        frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        frame_conteudo.pack(fill="both", expand=True, padx=40, pady=5)
        
        frame_conteudo.grid_columnconfigure(0, weight=1)
        frame_conteudo.grid_columnconfigure(1, weight=1)
        frame_conteudo.grid_columnconfigure(2, weight=1)

        # --- GRUPO 1: MOVIMENTAÇÃO ---
        # Ícone: Caixa/Pacote
        self._criar_grupo_botoes(
            master=frame_conteudo, 
            titulo="Movimentação", 
            coluna=0,
            icone="📦", 
            botoes=[
                ("📥 Registrar Entrada", self.controller.tela_entrada, "#00897B", "#004D40"),
                ("📤 Registrar Saída", self.controller.tela_saida, "#D32F2F", "#B71C1C")
            ]
        )

        # --- GRUPO 2: GESTÃO ---
        # Ícone: Ferramentas/Lista
        self._criar_grupo_botoes(
            master=frame_conteudo, 
            titulo="Gestão de Itens", 
            coluna=1,
            icone="🛠️",
            botoes=[
                ("📋 Ver Estoque", self.controller.tela_estoque, "#1F6AA5", "#144870"),
                ("➕ Nova Peça", self.controller.tela_cadastro, "#2E7D32", "#1B5E20")
            ]
        )

        # --- GRUPO 3: RELATÓRIOS ---
        # Ícone: Gráfico
        self._criar_grupo_botoes(
            master=frame_conteudo, 
            titulo="Inteligência", 
            coluna=2,
            icone="📊",
            botoes=[
                ("⏳ Histórico Completo", self.controller.tela_historico, "#5E35B1", "#4527A0"),
                ("💰 Lucro Real", self.controller.tela_lucro, "#C27803", "#8F5802")
            ]
        )

        # Rodapé
        btn_sair = ctk.CTkButton(self, text="Sair do Sistema", command=self.controller.fechar_aplicacao, 
                                 fg_color="transparent", border_width=2, border_color="#444", text_color="#AAA", 
                                 hover_color="#333", height=35)
        btn_sair.pack(pady=20)

    def _criar_grupo_botoes(self, master, titulo, coluna, botoes, icone=None):
        """
        Cria um 'Card' visual contendo Ícone, Título e Botões.
        """
        # Frame do Grupo (Card)
        frame_card = ctk.CTkFrame(master, corner_radius=15, border_width=2, border_color="#2B2B2B")
        frame_card.grid(row=0, column=coluna, sticky="nsew", padx=15, pady=10)
        
        # --- ÍCONE (EMOJI GIGANTE) ---
        if icone:
            lbl_icone = ctk.CTkLabel(frame_card, text=icone, font=("Segoe UI Emoji", 48)) # Fonte Emoji para Windows/Linux
            lbl_icone.pack(pady=(25, 0))

        # Título do Grupo
        lbl_grupo = ctk.CTkLabel(frame_card, text=titulo, font=ctk.CTkFont(size=18, weight="bold"), text_color="#DCE4EE")
        lbl_grupo.pack(pady=(5, 10))
        
        # Linha divisória decorativa
        linha = ctk.CTkFrame(frame_card, height=2, fg_color="#333")
        linha.pack(fill="x", padx=40, pady=(0, 20))

        # Botões
        for txt, cmd, color, hover in botoes:
            btn = ctk.CTkButton(frame_card, 
                                text=txt, 
                                command=cmd, 
                                width=240, 
                                height=40,
                                font=ctk.CTkFont(size=15),
                                fg_color=color, 
                                hover_color=hover,
                                corner_radius=8)
            btn.pack(pady=10, padx=20)

    # --- Utilitários ---
    def _janela_modal(self, title, tamanho="700x600"):
        tl = ctk.CTkToplevel(self)
        tl.title(title)
        if tamanho: tl.geometry(tamanho)
        tl.transient(self)
        tl.grab_set()
        tl.focus_set()
        
        # Centraliza
        self.update_idletasks()
        try:
            x = self.winfo_x() + (self.winfo_width() // 2) - (tl.winfo_reqwidth() // 2)
            y = self.winfo_y() + (self.winfo_height() // 2) - (tl.winfo_reqheight() // 2)
            tl.geometry(f"+{x}+{y}")
        except: pass
        
        fr = ctk.CTkFrame(tl)
        fr.pack(expand=True, fill='both', padx=10, pady=10)
        return tl, fr

    def fmt_moeda(self, v):
        return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if v else "R$ 0,00"

    def msg(self, tipo, txt):
        if tipo == 'erro': messagebox.showerror("Erro", txt)
        elif tipo == 'info': messagebox.showinfo("Sucesso", txt)
        elif tipo == 'ask': return messagebox.askyesno("Confirmar", txt)

    def _treeview(self, master, cols):
        tv = ttk.Treeview(master, columns=cols, show='headings')
        for c in cols: 
            tv.heading(c, text=c)
            tv.column(c, anchor='center')
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#333", foreground="white", fieldbackground="#333")
        style.map('Treeview', background=[('selected', '#1f538d')])
        return tv

    def _picker_ou_entry(self, master):
        if CTkDatePicker:
            try:
                w = CTkDatePicker(master)
                w.get_data = w.get_date_str
                return w
            except: pass
        w = ctk.CTkEntry(master)
        w.insert(0, datetime.now().strftime("%d/%m/%Y"))
        w.get_data = w.get
        return w

    # --- Telas ---
    def tela_cadastro(self):
        tl, fr = self._janela_modal("Nova Peça", "500x500")
        campos = {}
        for lb in ['Descrição:', 'Série:', 'Marca:', 'Custo:']:
            ctk.CTkLabel(fr, text=lb).pack(anchor='w')
            e = ctk.CTkEntry(fr); e.pack(fill='x', pady=(0,5))
            campos[lb] = e
        
        ctk.CTkLabel(fr, text="Condição:").pack(anchor='w')
        cb = ctk.CTkComboBox(fr, values=["Nova", "Usada", "Sucata"]); cb.pack(fill='x', pady=(0,5))
        cb.set("Nova")

        def salvar():
            d = {'desc': campos['Descrição:'].get(), 'serie': campos['Série:'].get(), 
                 'marca': campos['Marca:'].get(), 'custo': campos['Custo:'].get(), 'cond': cb.get()}
            self.controller.acao_salvar_peca(tl, d)
            
        # Botão Salvar (Verde)
        ctk.CTkButton(fr, text="💾 Salvar Cadastro", 
                      fg_color="#2E7D32", hover_color="#1B5E20",
                      command=salvar).pack(pady=20)

    def tela_estoque(self):
        tl, fr = self._janela_modal("Estoque", "1100x600") # Ajuste largura se precisar
        
        lbl_tot = ctk.CTkLabel(fr, text="Total: ...", font=("Arial", 16, "bold"))
        lbl_tot.pack(pady=10)
        
        tv = self._treeview(fr, ('ID', 'Descrição', 'Marca', 'Custo', 'Qtd', 'Condição'))
        tv.column('ID', width=40)
        tv.column('Descrição', width=250)
        tv.pack(fill='both', expand=True)
        
        fr_b = ctk.CTkFrame(fr)
        fr_b.pack(pady=10)
        
        # Botão Editar (Laranja)
        ctk.CTkButton(fr_b, 
                      text="✏️ Editar Peça", 
                      fg_color="#F59E0B", hover_color="#B45309", # Laranja
                      command=lambda: self.controller.tela_edicao(tl, tv, lbl_tot)
        ).pack(side='left', padx=10)

        # Botão Excluir (Vermelho)
        ctk.CTkButton(fr_b, 
                      text="🗑️ Excluir Peça", 
                      fg_color="#D32F2F", hover_color="#B71C1C", # Vermelho
                      command=lambda: self.controller.acao_excluir_peca(tl, tv, lbl_tot)
        ).pack(side='left', padx=10)
        
        self.controller.carregar_estoque(tv, lbl_tot)

    def tela_edicao(self, pid, dados, tv, lbl): # Adicionado tv e lbl nos argumentos
        tl, fr = self._janela_modal(f"Editar ID {pid}", "500x450")
        
        vals = [dados[1], dados[2], dados[3], dados[4]]
        campos = {}
        labels = ['Descrição', 'Série', 'Marca', 'Custo']
        
        for i, lb in enumerate(labels):
            ctk.CTkLabel(fr, text=lb).pack(anchor='w')
            e = ctk.CTkEntry(fr); e.insert(0, str(vals[i]) if vals[i] else "")
            e.pack(fill='x', pady=(0, 5))
            campos[lb] = e
        
        ctk.CTkLabel(fr, text="Condição").pack(anchor='w')
        cb = ctk.CTkComboBox(fr, values=["Nova", "Usada", "Sucata"])
        cb.set(dados[5] or "Nova")
        cb.pack(fill='x', pady=(0, 5))
        
        def salvar():
            d = {'desc': campos['Descrição'].get(), 'serie': campos['Série'].get(), 
                 'marca': campos['Marca'].get(), 'custo': campos['Custo'].get(), 'cond': cb.get()}
            
            # CORREÇÃO: Agora passamos tv e lbl de volta para o Controller
            self.controller.acao_atualizar_peca(tl, pid, d, tv, lbl)
            
        ctk.CTkButton(fr, text="Salvar Alterações", command=salvar, fg_color="#2E7D32", hover_color="#1B5E20").pack(pady=20)

    def tela_entrada(self):
        tl, fr = self._janela_modal("Entrada", "500x450")
        
        ctk.CTkLabel(fr, text="Peça:").pack(anchor='w')
        ctk.CTkEntry(fr, textvariable=self.var_desc_entrada, state="readonly").pack(fill='x', pady=(0,5))
        
        # Botão Buscar (Azul)
        ctk.CTkButton(fr, text="🔍 Buscar Peça", 
                      command=lambda: self.tela_busca(self.var_id_entrada, self.var_desc_entrada),
                      fg_color="#1F6AA5", hover_color="#144870", height=30
        ).pack(pady=5)
        
        ctk.CTkLabel(fr, text="Data:").pack(anchor='w')
        dt = self._picker_ou_entry(fr); dt.pack(fill='x', pady=(0,5))
        
        ctk.CTkLabel(fr, text="Qtd:").pack(anchor='w')
        qtd = ctk.CTkEntry(fr); qtd.pack(fill='x', pady=(0,5))
        
        def salvar(): self.controller.acao_entrada(tl, self.var_id_entrada.get(), dt.get_data(), qtd.get())
        
        # Botão Salvar (Verde)
        ctk.CTkButton(fr, text="✅ Confirmar Entrada", 
                      fg_color="#2E7D32", hover_color="#1B5E20",
                      command=salvar).pack(pady=20)

    def tela_saida(self):
        tl, fr = self._janela_modal("Saída", "500x600")
        
        ctk.CTkLabel(fr, text="Peça:").pack(anchor='w')
        ctk.CTkEntry(fr, textvariable=self.var_desc_saida, state="readonly").pack(fill='x', pady=(0,5))
        
        # Botão Buscar (Azul)
        ctk.CTkButton(fr, text="🔍 Buscar Peça", 
                      command=lambda: self.tela_busca(self.var_id_saida, self.var_desc_saida),
                      fg_color="#1F6AA5", hover_color="#144870", height=30
        ).pack(pady=5)
        
        ctk.CTkLabel(fr, text="Data:").pack(anchor='w')
        dt = self._picker_ou_entry(fr); dt.pack(fill='x', pady=(0,5))
        
        ctk.CTkLabel(fr, text="Qtd:").pack(anchor='w')
        qtd = ctk.CTkEntry(fr); qtd.pack(fill='x', pady=(0,5))
        
        ctk.CTkLabel(fr, text="Preço Venda (R$):").pack(anchor='w')
        venda = ctk.CTkEntry(fr); venda.pack(fill='x', pady=(0,5))
        
        ctk.CTkLabel(fr, text="Canal:").pack(anchor='w')
        canal = ctk.CTkComboBox(fr, values=["Loja", "Online"]); canal.pack(fill='x', pady=(0,5))
        
        def salvar(): 
            d = {'data': dt.get_data(), 'qtd': qtd.get(), 'venda': venda.get(), 'canal': canal.get()}
            self.controller.acao_saida(tl, self.var_id_saida.get(), d)
            
        # Botão Confirmar (Verde)
        ctk.CTkButton(fr, text="✅ Confirmar Saída", 
                      fg_color="#2E7D32", hover_color="#1B5E20",
                      command=salvar).pack(pady=20)

    def tela_busca(self, var_id, var_desc):
        tl, fr = self._janela_modal("Buscar", "600x400")
        ent = ctk.CTkEntry(fr, placeholder_text="Digite..."); ent.pack(fill='x', pady=5)
        tv = self._treeview(fr, ('ID', 'Descrição', 'Série'))
        tv.pack(fill='both', expand=True)
        
        def buscar(): self.controller.carregar_busca(tv, ent.get())
        ent.bind('<Return>', lambda e: buscar())
        ctk.CTkButton(fr, text="Buscar", command=buscar).pack(pady=5)
        
        def selecionar():
            sel = tv.focus()
            if sel:
                vals = tv.item(sel, 'values')
                var_id.set(vals[0])
                var_desc.set(f"{vals[0]} - {vals[1]}")
                tl.destroy()
        ctk.CTkButton(fr, text="Selecionar", fg_color="green", command=selecionar).pack(pady=10)
        buscar()

    def tela_historico(self):
        tl, fr = self._janela_modal("Histórico", "1100x650")
        
        # --- Filtros ---
        filtros = ctk.CTkFrame(fr)
        filtros.pack(fill='x', pady=5)
        
        d1 = self._picker_ou_entry(filtros); d1.pack(side='left', padx=5)
        d2 = self._picker_ou_entry(filtros); d2.pack(side='left', padx=5)
        
        tipo = ctk.StringVar(value="saidas")
        
        # Ícones nos Radio Buttons para facilitar a leitura rápida
        ctk.CTkRadioButton(filtros, text="📥 Entradas", variable=tipo, value="entradas").pack(side='left', padx=10)
        ctk.CTkRadioButton(filtros, text="📤 Saídas", variable=tipo, value="saidas").pack(side='left', padx=10)
        
        tv = self._treeview(fr, ('ID', 'Data', 'Qtd', 'Peça', 'Unit', 'Total'))
        tv.column('ID', width=40)
        tv.column('Peça', width=250)
        tv.pack(fill='both', expand=True, pady=5)
        
        lbl = ctk.CTkLabel(fr, text="Resumo...", font=("Arial", 12, "bold")); lbl.pack()
        
        def carregar(): self.controller.carregar_historico(tv, tipo.get(), d1.get_data(), d2.get_data(), lbl)
        
        # Botão Filtrar com Lupa
        ctk.CTkButton(filtros, 
                      text="🔎 Filtrar", 
                      command=carregar,
                      width=100,
                      fg_color="#1F6AA5", hover_color="#144870" # Azul padrão
        ).pack(side='left', padx=10)
        
        if hasattr(d1, 'set_callback'): d1.set_callback(carregar)
        if hasattr(d2, 'set_callback'): d2.set_callback(carregar)

        # Botão Excluir com Lixeira
        ctk.CTkButton(fr, 
                      text="🗑️ Excluir Movimento Selecionado", 
                      fg_color="#D32F2F", hover_color="#B71C1C", # Vermelho Alerta
                      command=lambda: self.controller.acao_excluir_movimento(tipo.get(), tv, carregar)
        ).pack(pady=10)
        
        carregar()

    def tela_lucro(self):
        tl, fr = self._janela_modal("Lucro", "1200x650")
        
        # --- Área de Destaque (Card de Resultado) ---
        # Criamos um frame transparente para centralizar o card
        frame_destaque = ctk.CTkFrame(fr, fg_color="transparent")
        frame_destaque.pack(fill='x', pady=(20, 10))

        # O Label agora parece um "Botão/Card" informativo
        lbl_tot = ctk.CTkLabel(frame_destaque, 
                               text="💰 Lucro Total: ...",   # <--- ÍCONE ADICIONADO AQUI
                               font=("Arial", 24, "bold"),   # Aumentei para 24 para o ícone ficar visível
                               text_color="#FFFFFF", 
                               fg_color="#2E7D32", 
                               corner_radius=15, 
                               width=350, 
                               height=60)
        lbl_tot.pack()

        # --- Filtros ---
        filtros = ctk.CTkFrame(fr)
        filtros.pack(fill='x', pady=10, padx=10)
        
        d1 = self._picker_ou_entry(filtros); d1.pack(side='left', padx=5)
        d2 = self._picker_ou_entry(filtros); d2.pack(side='left', padx=5)
        
        # Botão Calcular (Dourado)
        def carregar(): self.controller.carregar_lucro(tv, d1.get_data(), d2.get_data(), lbl_tot)
        
        ctk.CTkButton(filtros, text="💰 Calcular Resultado", 
                      fg_color="#C27803", hover_color="#8F5802",
                      font=("Arial", 14, "bold"),
                      command=carregar).pack(side='left', padx=15)

        # --- Tabela ---
        tv = self._treeview(fr, ('Data', 'Qtd', 'Peça', 'Custo', 'Venda', 'Lucro'))
        tv.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        carregar()