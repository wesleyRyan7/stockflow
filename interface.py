import customtkinter as ctk
from tkinter import messagebox
from supabase_client import supabase

# ==========================================
# CONFIG
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# JANELA
# ==========================================

app = ctk.CTk()

app.title("StockFlow")
app.geometry("1400x800")

# ==========================================
# CORES
# ==========================================

COR_FUNDO = "#0f172a"
COR_CARD = "#1e293b"
COR_BOTAO = "#2563eb"

app.configure(fg_color=COR_FUNDO)

# ==========================================
# ÁREA PRINCIPAL
# ==========================================

main_frame = ctk.CTkFrame(
    app,
    fg_color=COR_FUNDO
)

main_frame.pack(
    side="right",
    fill="both",
    expand=True
)

# ==========================================
# LIMPAR TELA
# ==========================================

def limpar_tela():

    for widget in main_frame.winfo_children():
        widget.destroy()

# ==========================================
# DASHBOARD
# ==========================================

def abrir_dashboard():

    limpar_tela()

    titulo = ctk.CTkLabel(
        main_frame,
        text="Dashboard",
        font=("Arial", 32, "bold")
    )

    titulo.pack(pady=30)

    card = ctk.CTkFrame(
        main_frame,
        fg_color=COR_CARD,
        corner_radius=15
    )

    card.pack(
        padx=20,
        pady=20,
        fill="x"
    )

    texto = ctk.CTkLabel(
        card,
        text="Bem-vindo ao StockFlow",
        font=("Arial", 20)
    )

    texto.pack(pady=40)

# ==========================================
# ESTOQUE
# ==========================================

def abrir_estoque():

    limpar_tela()

    titulo = ctk.CTkLabel(
        main_frame,
        text="Controle de Estoque",
        font=("Arial", 30, "bold")
    )

    titulo.pack(pady=20)

    # CARD
    card = ctk.CTkFrame(
        main_frame,
        fg_color=COR_CARD,
        corner_radius=15
    )

    card.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    # ENTRADAS
    entry_nome = ctk.CTkEntry(
        card,
        placeholder_text="Nome do insumo"
    )

    entry_nome.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    entry_quantidade = ctk.CTkEntry(
        card,
        placeholder_text="Quantidade"
    )

    entry_quantidade.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    entry_unidade = ctk.CTkEntry(
        card,
        placeholder_text="Unidade"
    )

    entry_unidade.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    # LISTA
    tabela = ctk.CTkTextbox(
        main_frame,
        font=("Consolas", 15),
        fg_color=COR_CARD
    )

    tabela.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    def atualizar_estoque():

        tabela.delete("1.0", "end")

        response = supabase.table("insumos").select("*").execute()

        insumos = response.data

        tabela.insert(
            "end",
            "ID | NOME | QUANTIDADE | UNIDADE\n\n"
        )

        for insumo in insumos:

            alerta = ""

            if insumo["quantidade"] <= 5:
                alerta = " ⚠️"

            tabela.insert(
                "end",
                f"{insumo['id']} | "
                f"{insumo['nome']} | "
                f"{insumo['quantidade']} | "
                f"{insumo['unidade']}"
                f"{alerta}\n"
            )

    def adicionar_insumo():

        nome = entry_nome.get()

        quantidade = float(
            entry_quantidade.get().replace(",", ".")
        )

        unidade = entry_unidade.get()

        supabase.table("insumos").insert({
            "nome": nome,
            "quantidade": quantidade,
            "unidade": unidade
        }).execute()

        messagebox.showinfo(
            "Sucesso",
            "Insumo adicionado!"
        )

        atualizar_estoque()

    btn_add = ctk.CTkButton(
        card,
        text="Adicionar Insumo",
        fg_color=COR_BOTAO,
        height=40,
        command=adicionar_insumo
    )

    btn_add.pack(
        padx=20,
        pady=20,
        fill="x"
    )

    atualizar_estoque()

# ==========================================
# PRODUTOS
# ==========================================

def abrir_produtos():

    limpar_tela()

    titulo = ctk.CTkLabel(
        main_frame,
        text="Produtos",
        font=("Arial", 30, "bold")
    )

    titulo.pack(pady=20)

    tabela = ctk.CTkTextbox(
        main_frame,
        fg_color=COR_CARD
    )

    tabela.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    response = supabase.table("produtos").select("*").execute()

    produtos = response.data

    tabela.insert(
        "end",
        "ID | PRODUTO | PREÇO\n\n"
    )

    for produto in produtos:

        tabela.insert(
            "end",
            f"{produto['id']} | "
            f"{produto['nome']} | "
            f"R$ {produto['preco']}\n"
        )

# ==========================================
# VENDAS
# ==========================================

def abrir_vendas():

    limpar_tela()

    titulo = ctk.CTkLabel(
        main_frame,
        text="Vendas",
        font=("Arial", 30, "bold")
    )

    titulo.pack(pady=20)

    card = ctk.CTkFrame(
        main_frame,
        fg_color=COR_CARD,
        corner_radius=15
    )

    card.pack(
        padx=20,
        pady=20,
        fill="x"
    )

    # ==========================================
    # PRODUTOS
    # ==========================================

    response = supabase.table("produtos").select("*").execute()

    produtos = response.data

    produtos_dict = {}

    nomes_produtos = []

    for produto in produtos:

        nomes_produtos.append(produto["nome"])

        produtos_dict[produto["nome"]] = produto

    combo_produto = ctk.CTkComboBox(
        card,
        values=nomes_produtos
    )

    combo_produto.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    # ==========================================
    # QUANTIDADE
    # ==========================================

    entry_quantidade = ctk.CTkEntry(
        card,
        placeholder_text="Quantidade"
    )

    entry_quantidade.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    # ==========================================
    # BEBIDAS
    # ==========================================

    bebidas_response = supabase.table("bebidas").select("*").execute()

    bebidas = bebidas_response.data

    bebidas_dict = {}

    nomes_bebidas = ["Nenhuma"]

    for bebida in bebidas:

        nomes_bebidas.append(bebida["nome"])

        bebidas_dict[bebida["nome"]] = bebida

    combo_bebida = ctk.CTkComboBox(
        card,
        values=nomes_bebidas
    )

    combo_bebida.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    combo_bebida.set("Nenhuma")

    # ==========================================
    # TOTAL
    # ==========================================

    label_total = ctk.CTkLabel(
        card,
        text="Total: R$ 0.00",
        font=("Arial", 22, "bold")
    )

    label_total.pack(pady=20)

    # ==========================================
    # CALCULAR TOTAL
    # ==========================================

    def calcular_total():

        try:

            produto_nome = combo_produto.get()

            quantidade = int(
                entry_quantidade.get()
            )

            produto = produtos_dict[produto_nome]

            total = produto["preco"] * quantidade

            bebida_nome = combo_bebida.get()

            if bebida_nome != "Nenhuma":

                bebida = bebidas_dict[bebida_nome]

                total += bebida["preco"]

            label_total.configure(
                text=f"Total: R$ {total:.2f}"
            )

            return total

        except:

            return 0

    # ==========================================
    # FINALIZAR VENDA
    # ==========================================

    def finalizar_venda():

        total = calcular_total()

        produto_nome = combo_produto.get()

        quantidade = int(
            entry_quantidade.get()
        )

        produto = produtos_dict[produto_nome]

        produto_id = produto["id"]

        # ==========================
        # RECEITA
        # ==========================

        receita_response = supabase.table(
            "receita_produtos"
        ).select("*").eq(
            "produto_id",
            produto_id
        ).execute()

        receita = receita_response.data

        # ==========================
        # BAIXAR INSUMOS
        # ==========================

        for item in receita:

            insumo_id = item["insumo_id"]

            quantidade_usada = (
                item["quantidade_usada"] * quantidade
            )

            estoque_response = supabase.table(
                "insumos"
            ).select("*").eq(
                "id",
                insumo_id
            ).single().execute()

            insumo = estoque_response.data

            nova_quantidade = (
                insumo["quantidade"] - quantidade_usada
            )

            supabase.table("insumos").update({
                "quantidade": nova_quantidade
            }).eq(
                "id",
                insumo_id
            ).execute()

        # ==========================
        # BEBIDA
        # ==========================

        bebida_nome = combo_bebida.get()

        bebida_id = None

        if bebida_nome != "Nenhumcoca":

            bebida = bebidas_dict[bebida_nome]

            bebida_id = bebida["id"]

            nova_qtd = bebida["quantidade"] - 1

            supabase.table("bebidas").update({
                "quantidade": nova_qtd
            }).eq(
                "id",
                bebida_id
            ).execute()

        # ==========================
        # REGISTRAR VENDA
        # ==========================

        supabase.table("vendas").insert({
            "produto_id": produto_id,
            "bebida_id": bebida_id,
            "quantidade": quantidade,
            "valor_total": total
        }).execute()

        messagebox.showinfo(
            "Sucesso",
            "Venda realizada!"
        )

        label_total.configure(
            text="Total: R$ 0.00"
        )

    # ==========================================
    # BOTÕES
    # ==========================================

    btn_total = ctk.CTkButton(
        card,
        text="Calcular Total",
        fg_color=COR_BOTAO,
        command=calcular_total
    )

    btn_total.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    btn_finalizar = ctk.CTkButton(
        card,
        text="Finalizar Venda",
        fg_color="#16a34a",
        hover_color="#15803d",
        height=45,
        command=finalizar_venda
    )

    btn_finalizar.pack(
        padx=20,
        pady=20,
        fill="x"
    )

# ==========================================
# RELATÓRIOS
# ==========================================

def abrir_relatorios():

    limpar_tela()

    titulo = ctk.CTkLabel(
        main_frame,
        text="Relatórios",
        font=("Arial", 30, "bold")
    )

    titulo.pack(pady=20)

    tabela = ctk.CTkTextbox(
        main_frame,
        fg_color=COR_CARD
    )

    tabela.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    response = supabase.table("vendas").select("*").execute()

    vendas = response.data

    total = 0

    tabela.insert(
        "end",
        "RELATÓRIO DE VENDAS\n\n"
    )

    for venda in vendas:

        tabela.insert(
            "end",
            f"Venda ID: {venda['id']} | "
            f"Valor: R$ {venda['valor_total']}\n"
        )

        total += venda["valor_total"]

    tabela.insert(
        "end",
        f"\nFATURAMENTO TOTAL: R$ {total}"
    )

# ==========================================
# SIDEBAR
# ==========================================

sidebar = ctk.CTkFrame(
    app,
    width=250,
    fg_color=COR_CARD
)

sidebar.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)

logo = ctk.CTkLabel(
    sidebar,
    text="STOCKFLOW",
    font=("Arial", 28, "bold")
)

logo.pack(pady=40)

def criar_botao(texto, comando):

    botao = ctk.CTkButton(
        sidebar,
        text=texto,
        fg_color=COR_BOTAO,
        hover_color="#1d4ed8",
        height=45,
        command=comando
    )

    botao.pack(
        padx=20,
        pady=10,
        fill="x"
    )

criar_botao("Dashboard", abrir_dashboard)
criar_botao("Estoque", abrir_estoque)
criar_botao("Produtos", abrir_produtos)
criar_botao("Vendas", abrir_vendas)
criar_botao("Relatórios", abrir_relatorios)

# ==========================================
# INICIAR
# ==========================================

abrir_dashboard()

app.mainloop()