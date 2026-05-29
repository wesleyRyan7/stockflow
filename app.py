from supabase_client import supabase

# ==========================================
# INSUMOS
# ==========================================

def listar_insumos():

    response = supabase.table("insumos").select("*").execute()

    insumos = response.data

    print("\n=== INSUMOS ===")

    for insumo in insumos:

        alerta = ""

        if insumo["quantidade"] <= 5:
            alerta = " ⚠️ ESTOQUE BAIXO"

        print(
            f"ID: {insumo['id']} | "
            f"{insumo['nome']} | "
            f"{insumo['quantidade']} {insumo['unidade']}"
            f"{alerta}"
        )


def adicionar_insumo():

    nome = input("Nome do insumo: ")
    quantidade = float(input("Quantidade: ").replace(",", "."))
    unidade = input("Unidade: ")

    supabase.table("insumos").insert({
        "nome": nome,
        "quantidade": quantidade,
        "unidade": unidade
    }).execute()

    print("\n✅ Insumo adicionado!")


def editar_insumo():

    listar_insumos()

    insumo_id = int(input("\nID do insumo: "))

    novo_nome = input("Novo nome: ")
    nova_quantidade = float(input("Nova quantidade: ").replace(",", "."))
    nova_unidade = input("Nova unidade: ")

    supabase.table("insumos") \
        .update({
            "nome": novo_nome,
            "quantidade": nova_quantidade,
            "unidade": nova_unidade
        }) \
        .eq("id", insumo_id) \
        .execute()

    print("\n✅ Insumo atualizado!")


def excluir_insumo():

    listar_insumos()

    insumo_id = int(input("\nID do insumo para excluir: "))

    supabase.table("insumos") \
        .delete() \
        .eq("id", insumo_id) \
        .execute()

    print("\n🗑️ Insumo removido!")


# ==========================================
# PRODUTOS
# ==========================================

def criar_produto():

    nome = input("Nome do produto: ")
    preco = float(input("Preço: ").replace(",", "."))

    supabase.table("produtos").insert({
        "nome": nome,
        "preco": preco
    }).execute()

    print("\n✅ Produto criado!")


def listar_produtos():

    response = supabase.table("produtos").select("*").execute()

    produtos = response.data

    print("\n=== PRODUTOS ===")

    for produto in produtos:

        print(
            f"ID: {produto['id']} | "
            f"{produto['nome']} | "
            f"R$ {produto['preco']}"
        )


def editar_produto():

    listar_produtos()

    produto_id = int(input("\nID do produto: "))

    novo_nome = input("Novo nome: ")
    novo_preco = float(input("Novo preço: ").replace(",", "."))

    supabase.table("produtos") \
        .update({
            "nome": novo_nome,
            "preco": novo_preco
        }) \
        .eq("id", produto_id) \
        .execute()

    print("\n✅ Produto atualizado!")


def excluir_produto():

    listar_produtos()

    produto_id = int(input("\nID do produto: "))

    supabase.table("produtos") \
        .delete() \
        .eq("id", produto_id) \
        .execute()

    print("\n🗑️ Produto removido!")


# ==========================================
# RECEITA
# ==========================================

def criar_receita():

    listar_produtos()

    produto_id = int(input("\nID do produto: "))

    while True:

        listar_insumos()

        insumo_id = int(input("\nID do insumo: "))
        quantidade = float(input("Quantidade usada: ").replace(",", "."))

        supabase.table("receita_produtos").insert({
            "produto_id": produto_id,
            "insumo_id": insumo_id,
            "quantidade_usada": quantidade
        }).execute()

        continuar = input("\nAdicionar mais insumos? (s/n): ")

        if continuar.lower() != "s":
            break

    print("\n✅ Receita criada!")


# ==========================================
# BEBIDAS
# ==========================================

def listar_bebidas():

    response = supabase.table("bebidas").select("*").execute()

    bebidas = response.data

    print("\n=== BEBIDAS ===")

    for bebida in bebidas:

        print(
            f"ID: {bebida['id']} | "
            f"{bebida['nome']} | "
            f"Qtd: {bebida['quantidade']} | "
            f"R$ {bebida['preco']}"
        )


def adicionar_bebida():

    nome = input("Nome da bebida: ")
    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço: ").replace(",", "."))

    supabase.table("bebidas").insert({
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco
    }).execute()

    print("\n✅ Bebida adicionada!")


# ==========================================
# VENDA
# ==========================================

def vender_produto():

    listar_produtos()

    produto_id = int(input("\nID produto: "))
    quantidade_venda = int(input("Quantidade: "))

    produto_response = supabase.table("produtos") \
        .select("*") \
        .eq("id", produto_id) \
        .single() \
        .execute()

    produto = produto_response.data

    receita_response = supabase.table("receita_produtos") \
        .select("*") \
        .eq("produto_id", produto_id) \
        .execute()

    receita = receita_response.data

    # BAIXA INSUMOS
    for item in receita:

        insumo_id = item["insumo_id"]

        quantidade_usada = (
            item["quantidade_usada"] * quantidade_venda
        )

        estoque_response = supabase.table("insumos") \
            .select("*") \
            .eq("id", insumo_id) \
            .single() \
            .execute()

        insumo = estoque_response.data

        nova_quantidade = (
            insumo["quantidade"] - quantidade_usada
        )

        supabase.table("insumos") \
            .update({
                "quantidade": nova_quantidade
            }) \
            .eq("id", insumo_id) \
            .execute()

    valor_total = produto["preco"] * quantidade_venda

    # VENDA COM BEBIDA
    adicionar_bebida_venda = input(
        "\nAdicionar bebida? (s/n): "
    )

    bebida_id = None

    if adicionar_bebida_venda.lower() == "s":

        listar_bebidas()

        bebida_id = int(input("\nID bebida: "))

        bebida_response = supabase.table("bebidas") \
            .select("*") \
            .eq("id", bebida_id) \
            .single() \
            .execute()

        bebida = bebida_response.data

        nova_qtd_bebida = bebida["quantidade"] - 1

        supabase.table("bebidas") \
            .update({
                "quantidade": nova_qtd_bebida
            }) \
            .eq("id", bebida_id) \
            .execute()

        valor_total += bebida["preco"]

    # REGISTRA VENDA
    supabase.table("vendas").insert({
        "produto_id": produto_id,
        "bebida_id": bebida_id,
        "quantidade": quantidade_venda,
        "valor_total": valor_total
    }).execute()

    print("\n✅ Venda realizada!")
    print(f"\n💰 Total: R$ {valor_total}")


# ==========================================
# RELATÓRIO
# ==========================================

def relatorio_vendas():

    response = supabase.table("vendas").select("*").execute()

    vendas = response.data

    total = 0

    print("\n=== RELATÓRIO ===")

    for venda in vendas:

        print(venda)

        total += venda["valor_total"]

    print(f"\n💰 FATURAMENTO TOTAL: R$ {total}")


# ==========================================
# MENU
# ==========================================

while True:

    print("\n=========================")
    print("       STOCKFLOW")
    print("=========================")

    print("1 - Listar insumos")
    print("2 - Adicionar insumo")
    print("3 - Editar insumo")
    print("4 - Excluir insumo")

    print("5 - Criar produto")
    print("6 - Listar produtos")
    print("7 - Editar produto")
    print("8 - Excluir produto")

    print("9 - Criar receita")

    print("10 - Adicionar bebida")
    print("11 - Listar bebidas")

    print("12 - Vender produto")

    print("13 - Relatório vendas")

    print("14 - Sair")

    opcao = input("\nEscolha: ")

    if opcao == "1":
        listar_insumos()

    elif opcao == "2":
        adicionar_insumo()

    elif opcao == "3":
        editar_insumo()

    elif opcao == "4":
        excluir_insumo()

    elif opcao == "5":
        criar_produto()

    elif opcao == "6":
        listar_produtos()

    elif opcao == "7":
        editar_produto()

    elif opcao == "8":
        excluir_produto()

    elif opcao == "9":
        criar_receita()

    elif opcao == "10":
        adicionar_bebida()

    elif opcao == "11":
        listar_bebidas()

    elif opcao == "12":
        vender_produto()

    elif opcao == "13":
        relatorio_vendas()

    elif opcao == "14":
        print("\n👋 Encerrando...")
        break

    else:
        print("\n❌ Opção inválida!")