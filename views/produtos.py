import customtkinter as ctk
from tkinter import messagebox
from supabase_client import supabase


def abrir_produtos(main_frame, limpar_tela, COR_CARD, COR_BOTAO):

    limpar_tela()

    produto_selecionado = {
        "id": None
    }

    # ==========================================
    # TÍTULO
    # ==========================================

    titulo = ctk.CTkLabel(
        main_frame,
        text="Produtos",
        font=("Arial", 30, "bold")
    )

    titulo.pack(pady=20)

    # ==========================================
    # CARD
    # ==========================================

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

    # ==========================================
    # ENTRADAS
    # ==========================================

    entry_nome = ctk.CTkEntry(
        card,
        placeholder_text="Nome do produto"
    )

    entry_nome.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    entry_preco = ctk.CTkEntry(
        card,
        placeholder_text="Preço"
    )

    entry_preco.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    # ==========================================
    # TABELA
    # ==========================================

    tabela = ctk.CTkTextbox(
        main_frame,
        fg_color=COR_CARD,
        font=("Consolas", 15)
    )

    tabela.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    # ==========================================
    # ATUALIZAR PRODUTOS
    # ==========================================

    def atualizar_produtos():

        tabela.delete("1.0", "end")

        response = supabase.table(
            "produtos"
        ).select("*").execute()

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
    # ADICIONAR PRODUTO
    # ==========================================

    def adicionar_produto():

        nome = entry_nome.get()

        preco = float(
            entry_preco.get().replace(",", ".")
        )

        supabase.table("produtos").insert({
            "nome": nome,
            "preco": preco
        }).execute()

        messagebox.showinfo(
            "Sucesso",
            "Produto adicionado!"
        )

        atualizar_produtos()

        entry_nome.delete(0, "end")
        entry_preco.delete(0, "end")

    # ==========================================
    # BUSCAR PRODUTO
    # ==========================================

    def buscar_produto():

        try:

            produto_id = int(
                entry_nome.get()
            )

            response = supabase.table(
                "produtos"
            ).select("*").eq(
                "id",
                produto_id
            ).single().execute()

            produto = response.data

            produto_selecionado["id"] = produto["id"]

            entry_nome.delete(0, "end")
            entry_nome.insert(0, produto["nome"])

            entry_preco.delete(0, "end")
            entry_preco.insert(0, produto["preco"])

            messagebox.showinfo(
                "Sucesso",
                "Produto carregado!"
            )

        except:

            messagebox.showerror(
                "Erro",
                "Produto não encontrado"
            )

    # ==========================================
    # EDITAR PRODUTO
    # ==========================================

    def editar_produto():

        if not produto_selecionado["id"]:

            messagebox.showerror(
                "Erro",
                "Busque um produto pelo ID primeiro"
            )

            return

        nome = entry_nome.get()

        preco = float(
            entry_preco.get().replace(",", ".")
        )

        supabase.table("produtos").update({
            "nome": nome,
            "preco": preco
        }).eq(
            "id",
            produto_selecionado["id"]
        ).execute()

        messagebox.showinfo(
            "Sucesso",
            "Produto atualizado!"
        )

        atualizar_produtos()

    # ==========================================
    # EXCLUIR PRODUTO
    # ==========================================

    def excluir_produto():

        if not produto_selecionado["id"]:

            messagebox.showerror(
                "Erro",
                "Busque um produto primeiro"
            )

            return

        supabase.table("produtos").delete().eq(
            "id",
            produto_selecionado["id"]
        ).execute()

        messagebox.showinfo(
            "Sucesso",
            "Produto excluído!"
        )

        atualizar_produtos()

        entry_nome.delete(0, "end")
        entry_preco.delete(0, "end")

    # ==========================================
    # BOTÕES
    # ==========================================

    btn_add = ctk.CTkButton(
        card,
        text="Adicionar Produto",
        fg_color=COR_BOTAO,
        command=adicionar_produto
    )

    btn_add.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    btn_buscar = ctk.CTkButton(
        card,
        text="Buscar Produto por ID",
        fg_color="#7c3aed",
        command=buscar_produto
    )

    btn_buscar.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    btn_editar = ctk.CTkButton(
        card,
        text="Editar Produto",
        fg_color="#ca8a04",
        command=editar_produto
    )

    btn_editar.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    btn_excluir = ctk.CTkButton(
        card,
        text="Excluir Produto",
        fg_color="#dc2626",
        hover_color="#b91c1c",
        command=excluir_produto
    )

    btn_excluir.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    atualizar_produtos()