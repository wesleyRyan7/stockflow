import customtkinter as ctk
from tkinter import messagebox
from supabase_client import supabase
from views.estoque import abrir_estoque
from views.produtos import abrir_produtos

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

    # ==========================================
    # TÍTULO
    # ==========================================

    titulo = ctk.CTkLabel(
        main_frame,
        text="Dashboard",
        font=("Arial", 35, "bold")
    )

    titulo.pack(pady=20)

    # ==========================================
    # BUSCAR DADOS
    # ==========================================

    vendas_response = supabase.table(
        "vendas"
    ).select("*").execute()

    vendas = vendas_response.data

    produtos_response = supabase.table(
        "produtos"
    ).select("*").execute()

    produtos = produtos_response.data

    insumos_response = supabase.table(
        "insumos"
    ).select("*").execute()

    insumos = insumos_response.data

    # ==========================================
    # CÁLCULOS
    # ==========================================

    faturamento_total = 0

    for venda in vendas:
        faturamento_total += venda["valor_total"]

    total_vendas = len(vendas)

    total_produtos = len(produtos)

    estoque_baixo = 0

    for insumo in insumos:

        if insumo["quantidade"] <= 5:
            estoque_baixo += 1

    # ==========================================
    # FRAME DOS CARDS
    # ==========================================

    cards_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )

    cards_frame.pack(
        fill="x",
        padx=20,
        pady=20
    )

    # ==========================================
    # FUNÇÃO CARD
    # ==========================================

    def criar_card(titulo, valor, cor):

        card = ctk.CTkFrame(
            cards_frame,
            fg_color=cor,
            corner_radius=20,
            width=250,
            height=150
        )

        card.pack(
            side="left",
            padx=15,
            pady=10,
            expand=True,
            fill="both"
        )

        texto_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 20)
        )

        texto_titulo.pack(pady=(25, 10))

        texto_valor = ctk.CTkLabel(
            card,
            text=valor,
            font=("Arial", 32, "bold")
        )

        texto_valor.pack()

    # ==========================================
    # CARDS
    # ==========================================

    criar_card(
        "Faturamento",
        f"R$ {faturamento_total:.2f}",
        "#2563eb"
    )

    criar_card(
        "Vendas",
        str(total_vendas),
        "#16a34a"
    )

    criar_card(
        "Produtos",
        str(total_produtos),
        "#9333ea"
    )

    criar_card(
        "Estoque Baixo",
        str(estoque_baixo),
        "#dc2626"
    )

    # ==========================================
    # TABELA DE ALERTAS
    # ==========================================

    frame_alertas = ctk.CTkFrame(
        main_frame,
        fg_color=COR_CARD,
        corner_radius=20
    )

    frame_alertas.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    titulo_alerta = ctk.CTkLabel(
        frame_alertas,
        text="⚠️ Alertas de Estoque",
        font=("Arial", 24, "bold")
    )

    titulo_alerta.pack(pady=20)

    tabela = ctk.CTkTextbox(
        frame_alertas,
        fg_color="#0f172a",
        font=("Consolas", 15)
    )

    tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    for insumo in insumos:

        if insumo["quantidade"] <= 5:

            tabela.insert(
                "end",
                f"{insumo['nome']} → "
                f"{insumo['quantidade']} "
                f"{insumo['unidade']}\n"
            )
# ==========================================
# PRODUTOS
# ==========================================


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
criar_botao(
    "Estoque",
    lambda: abrir_estoque(
        main_frame,
        limpar_tela,
        COR_CARD,
        COR_BOTAO
    )
)
criar_botao(
    "Produtos",
    lambda: abrir_produtos(
        main_frame,
        limpar_tela,
        COR_CARD,
        COR_BOTAO
    )
)
criar_botao("Vendas", abrir_vendas)
criar_botao("Relatórios", abrir_relatorios)

# ==========================================
# INICIAR
# ==========================================

abrir_dashboard()

app.mainloop()