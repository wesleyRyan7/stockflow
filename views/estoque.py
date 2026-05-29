import customtkinter as ctk
from tkinter import messagebox
from supabase_client import supabase

def abrir_estoque(main_frame, limpar_tela, COR_CARD, COR_BOTAO):

    limpar_tela()

    # ==========================================
    # TÍTULO
    # ==========================================

    titulo = ctk.CTkLabel(
        main_frame,
        text="Controle de Estoque",
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

    # NOVO CAMPO ID

    entry_id = ctk.CTkEntry(
        card,
        placeholder_text="ID do insumo"
    )

    entry_id.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    # ==========================================
    # TABELA
    # ==========================================

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

    # ==========================================
    # ATUALIZAR ESTOQUE
    # ==========================================

    def atualizar_estoque():

        tabela.delete("1.0", "end")

        response = supabase.table(
            "insumos"
        ).select("*").execute()

        insumos = response.data

        tabela.insert(
            "end",
            "ID | NOME | QUANTIDADE | UNIDADE\n\n"
        )

        for insumo in insumos:

            alerta = ""

            if insumo["quantidade"] <= 5:
                alerta = " ⚠️ ESTOQUE BAIXO"

            tabela.insert(
                "end",
                f"{insumo['id']} | "
                f"{insumo['nome']} | "
                f"{insumo['quantidade']} | "
                f"{insumo['unidade']}"
                f"{alerta}\n"
            )

    # ==========================================
    # ADICIONAR INSUMO
    # ==========================================

    def adicionar_insumo():

        try:

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

        except:

            messagebox.showerror(
                "Erro",
                "Preencha os campos corretamente"
            )

    # ==========================================
    # EDITAR INSUMO
    # ==========================================

    def editar_insumo():

        try:

            insumo_id = entry_id.get()

            if insumo_id == "":

                messagebox.showerror(
                    "Erro",
                    "Digite o ID do insumo"
                )

                return

            nome = entry_nome.get()

            quantidade = float(
                entry_quantidade.get().replace(",", ".")
            )

            unidade = entry_unidade.get()

            supabase.table("insumos").update({
                "nome": nome,
                "quantidade": quantidade,
                "unidade": unidade
            }).eq(
                "id",
                insumo_id
            ).execute()

            messagebox.showinfo(
                "Sucesso",
                "Insumo atualizado!"
            )

            atualizar_estoque()

        except:

            messagebox.showerror(
                "Erro",
                "Erro ao editar"
            )

    # ==========================================
    # EXCLUIR INSUMO
    # ==========================================

    def excluir_insumo():

        try:

            insumo_id = entry_id.get()

            if insumo_id == "":

                messagebox.showerror(
                    "Erro",
                    "Digite o ID do insumo"
                )

                return

            supabase.table("insumos").delete().eq(
                "id",
                insumo_id
            ).execute()

            messagebox.showinfo(
                "Sucesso",
                "Insumo excluído!"
            )

            atualizar_estoque()

        except:

            messagebox.showerror(
                "Erro",
                "Erro ao excluir"
            )

    # ==========================================
    # BOTÕES
    # ==========================================

    btn_add = ctk.CTkButton(
        card,
        text="Adicionar Insumo",
        fg_color=COR_BOTAO,
        height=40,
        command=adicionar_insumo
    )

    btn_add.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    btn_editar = ctk.CTkButton(
        card,
        text="Editar Insumo",
        fg_color="#d97706",
        hover_color="#b45309",
        height=40,
        command=editar_insumo
    )

    btn_editar.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    btn_excluir = ctk.CTkButton(
        card,
        text="Excluir Insumo",
        fg_color="#dc2626",
        hover_color="#b91c1c",
        height=40,
        command=excluir_insumo
    )

    btn_excluir.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    # ==========================================
    # INICIAR
    # ==========================================

    atualizar_estoque()