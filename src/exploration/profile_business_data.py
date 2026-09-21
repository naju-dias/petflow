from pathlib import Path

import pandas as pd


# diretório onde estão os dados brutos do projeto
RAW_DATA_DIR = Path("data/raw")


def load_data() -> dict[str, pd.DataFrame]:
    # carrega apenas as tabelas necessárias para a análise inicial
    # retornar um dicionário facilita acessar cada DataFrame pelo nome da tabela

    return {
        "customers": pd.read_csv(
            RAW_DATA_DIR / "olist_customers_dataset.csv"
        ),
        "orders": pd.read_csv(
            RAW_DATA_DIR / "olist_orders_dataset.csv"
        ),
        "order_items": pd.read_csv(
            RAW_DATA_DIR / "olist_order_items_dataset.csv"
        ),
        "products": pd.read_csv(
            RAW_DATA_DIR / "olist_products_dataset.csv"
        ),
        "payments": pd.read_csv(
            RAW_DATA_DIR / "olist_order_payments_dataset.csv"
        ),
    }


def analyze_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> None:
    # analisa a quantidade de clientes e o comportamento de recompra
    
    print("\n" + "=" * 70)
    print("ANÁLISE DE CLIENTES")
    print("=" * 70)

    # quantidade total de registros na tabela de clientes
    print(f"\nRegistros em customers: {len(customers):,}")

    # customer_unique_id representa o consumidor de forma única
    unique_customers = customers["customer_unique_id"].nunique()

    print(f"Clientes únicos: {unique_customers:,}")

    # relaciona pedidos aos clientes para descobrir quantas compra cada consumidor realizou
    customer_orders = (
        orders
        .merge(
            customers[["customer_id", "customer_unique_id"]],
            on="customer_id",
            how="left",
        )
        .groupby("customer_unique_id")
        .size()
    )

    print("\nDistribuição de pedidos por cliente:")

    print(
        customer_orders
        .value_counts()
        .sort_index()
        .head(10)
    )

    # clientes que realizaram mais de um pedido
    repeat_customers = (customer_orders > 1).sum()

    print(f"\nClientes com mais de um pedido: {repeat_customers:,}")

    repeat_rate = repeat_customers / unique_customers * 100

    print(f"Taxa de recompra observada: {repeat_rate:.2f}%")


def analyze_orders(orders: pd.DataFrame) -> None:
    # analisa status e período dos pedidos

    print("\n" + "=" * 70)
    print("ANÁLISE DE PEDIDOS")
    print("=" * 70)

    # convertemos a coluna para datetime para permitir análises temporais
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    print("\nStatus dos pedidos:")

    print(
        orders["order_status"]
        .value_counts()
    )

    print("\nPrimeiro pedido:")
    print(orders["order_purchase_timestamp"].min())

    print("\nÚltimo pedido:")
    print(orders["order_purchase_timestamp"].max())

    # contagem mensal de pedidos
    monthly_orders = (
        orders
        .set_index("order_purchase_timestamp")
        .resample("ME")
        .size()
    )

    print("\nPedidos por mês:")
    print(monthly_orders)


def analyze_sales(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    payments: pd.DataFrame,
) -> None:
    # analisa valores financeiros básicos do dataset

    print("\n" + "=" * 70)
    print("ANÁLISE FINANCEIRA")
    print("=" * 70)

    # receita dos itens vendidos
    items_revenue = order_items["price"].sum()

    print(f"\nValor dos produtos: R$ {items_revenue:,.2f}")

    # frete total
    freight = order_items["freight_value"].sum()

    print(f"Frete total: R$ {freight:,.2f}")

    # valor total registrado na tabela de pagamentos
    payment_total = payments["payment_value"].sum()

    print(f"Valor total dos pagamentos: R$ {payment_total:,.2f}")

    # ticket médio aproximado considerando os pedidos
    average_order_value = payment_total / len(orders)

    print(
        f"Ticket médio aproximado: R$ {average_order_value:,.2f}"
    )


def analyze_relationships(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    payments: pd.DataFrame,
) -> None:
    # verifica se as principais relações entre tabelas estão consistentes

    print("\n" + "=" * 70)
    print("VALIDAÇÃO DE RELACIONAMENTOS")
    print("=" * 70)

    # verifica pedidos sem cliente correspondente
    orders_without_customer = (
        ~orders["customer_id"].isin(customers["customer_id"])
    ).sum()

    print(
        f"\nPedidos sem cliente correspondente: "
        f"{orders_without_customer:,}"
    )

    # verifica itens associados a pedidos inexistentes
    items_without_order = (
        ~order_items["order_id"].isin(orders["order_id"])
    ).sum()

    print(
        f"Itens sem pedido correspondente: "
        f"{items_without_order:,}"
    )

    # verifica itens associados a produtos inexistentes
    items_without_product = (
        ~order_items["product_id"].isin(products["product_id"])
    ).sum()

    print(
        f"Itens sem produto correspondente: "
        f"{items_without_product:,}"
    )

    # verifica pagamentos associados a pedidos inexistentes
    payments_without_order = (
        ~payments["order_id"].isin(orders["order_id"])
    ).sum()

    print(
        f"Pagamentos sem pedido correspondente: "
        f"{payments_without_order:,}"
    )


def main() -> None:
    # executa a análise exploratória inicial

    data = load_data()

    analyze_customers(
        data["customers"],
        data["orders"],
    )

    analyze_orders(data["orders"])

    analyze_sales(
        data["orders"],
        data["order_items"],
        data["payments"],
    )

    analyze_relationships(
        data["customers"],
        data["orders"],
        data["order_items"],
        data["products"],
        data["payments"],
    )


if __name__ == "__main__":
    main()