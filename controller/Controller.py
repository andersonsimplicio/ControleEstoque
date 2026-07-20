# controller/Controller.py
from model.database import DatabaseManager
from view.View import AppView

class AppController:
    def __init__(self):
        self.db = DatabaseManager()
        self.view = AppView(self)
        self.encerrar = self.fechar_aplicacao # Alias

    def run(self):
        self.view.mainloop()

    def fechar_aplicacao(self):
        try: self.db.fechar()
        except: pass
        self.view.destroy()
        exit()

    # --- Navegação ---
    def tela_cadastro(self): self.view.tela_cadastro()
    def tela_estoque(self): self.view.tela_estoque()
    def tela_entrada(self): self.view.tela_entrada()
    def tela_saida(self): self.view.tela_saida()
    def tela_historico(self): self.view.tela_historico()
    def tela_lucro(self): self.view.tela_lucro()

    # --- Ações ---
    def acao_salvar_peca(self, janela, d):
        try:
            if not d['desc']: return self.view.msg('erro', 'Descrição obrigatória.')
            custo = float(d['custo'].replace(',', '.') or 0)
            self.db.cadastrar_peca((d['desc'], d['serie'], d['marca'], custo, d['cond']))
            self.view.msg('info', 'Sucesso!')
            janela.destroy()
        except Exception as e: self.view.msg('erro', str(e))

    def carregar_estoque(self, tv, lbl):
        tv.delete(*tv.get_children())
        dados = self.db.buscar_estoque_completo()
        for p in dados:
            custo = self.view.fmt_moeda(p[4])
            tv.insert('', 'end', values=(p[0], p[1], p[3], custo, p[6], p[5]))
        tot = self.db.calcular_total_estoque()
        lbl.configure(text=f"Total Estoque: {self.view.fmt_moeda(tot)}")

    def acao_excluir_peca(self, janela, tv, lbl):
        sel = tv.focus()
        if not sel: return
        pid = tv.item(sel, 'values')[0]
        if self.view.msg('ask', 'Excluir peça e todo histórico?'):
            self.db.excluir_peca(pid)
            self.carregar_estoque(tv, lbl)

    def tela_edicao(self, janela_pai, tv, lbl):
        sel = tv.focus()
        if not sel: return
        pid = tv.item(sel, 'values')[0]
        
        dados = self.db.buscar_peca_por_id(pid)
        if dados: 
            # CORREÇÃO: Agora passamos 'tv' e 'lbl' para a View de edição também
            self.view.tela_edicao(pid, dados, tv, lbl)

    def acao_atualizar_peca(self, janela, pid, d, tv, lbl): # Adicionado tv e lbl aqui
        try:
            custo = float(d['custo'].replace(',', '.') or 0)
            self.db.atualizar_peca((d['desc'], d['serie'], d['marca'], custo, d['cond'], pid))
            self.view.msg('info', 'Peça atualizada com sucesso!')
            janela.destroy()
            
            # CORREÇÃO: Agora chamamos o recarregamento da tabela original
            self.carregar_estoque(tv, lbl)
            
        except Exception as e: 
            self.view.msg('erro', str(e))

    def carregar_busca(self, tv, termo):
        tv.delete(*tv.get_children())
        for p in self.db.buscar_pecas_por_descricao(termo):
            tv.insert('', 'end', values=p)

    def acao_entrada(self, janela, pid, data, qtd):
        try:
            if not pid: return self.view.msg('erro', 'Selecione peça.')
            self.db.registrar_movimento('entradas', (data, int(qtd), pid))
            self.view.msg('info', 'Entrada OK!')
            janela.destroy()
        except Exception as e: self.view.msg('erro', str(e))

    def acao_saida(self, janela, pid, d):
        try:
            if not pid: return self.view.msg('erro', 'Selecione peça.')
            sid = self.db.registrar_movimento('saidas', (d['data'], int(d['qtd']), pid))
            pv = float(d['venda'].replace(',', '.') or 0)
            self.db.registrar_venda((d['data'], pv, d['canal'], sid))
            self.view.msg('info', 'Saída OK!')
            janela.destroy()
        except Exception as e: self.view.msg('erro', str(e))

    def carregar_historico(self, tv, tipo, d1, d2, lbl):
        tv.delete(*tv.get_children())
        # DB retorna: (id, data, qtd, desc, custo)
        dados = self.db.buscar_historico(tipo, d1, d2)
        t_qtd, t_val = 0, 0
        for r in dados:
            # Treeview: (ID, Data, Qtd, Peça, Unit, Total)
            val_unit = r[4] or 0
            total = r[2] * val_unit
            t_qtd += r[2]
            t_val += total
            tv.insert('', 'end', values=(r[0], r[1], r[2], r[3], self.view.fmt_moeda(val_unit), self.view.fmt_moeda(total)))
        lbl.configure(text=f"Qtd: {t_qtd} | Total Custo: {self.view.fmt_moeda(t_val)}")

    def acao_excluir_movimento(self, tipo, tv, callback):
        sel = tv.focus()
        if not sel: return self.view.msg('erro', 'Selecione um item.')
        mid = tv.item(sel, 'values')[0] # Pega o ID da coluna 0
        if self.view.msg('ask', 'Excluir este movimento?'):
            self.db.excluir_movimento(tipo, mid)
            callback()

    def carregar_lucro(self, tv, d1, d2, lbl):
        tv.delete(*tv.get_children())
        dados = self.db.buscar_lucro(d1, d2)
        lucro_tot = 0
        for r in dados:
            custo = (r[3] or 0) * r[1]
            rec = (r[4] or 0) * r[1]
            lucro = rec - custo
            lucro_tot += lucro
            tv.insert('', 'end', values=(r[0], r[1], r[2], self.view.fmt_moeda(r[3]), self.view.fmt_moeda(r[4]), self.view.fmt_moeda(lucro)))
        lbl.configure(text=f"Lucro Total: {self.view.fmt_moeda(lucro_tot)}")