from pathlib import Path

import pandas as pd


RAW_DATA_DIR = Path("data/raw")

ANALYSIS_CUTOFF = pd.Timestamp("2018-08-31 23:59:59")


def load_data() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    # carrega as tabelas necessárias para construir o comportamento dos clientes

    customers = pd.read_csv(
        RAW_DATA_DIR / "olist_customers_dataset.csv"
    )

    orders = pd.read_csv(
        RAW_DATA_DIR / "olist_orders_dataset.csv"
    )

    order_items = pd.read_csv(
        RAW_DATA_DIR / "olist_order_items_dataset.csv"
    )

    return customers, orders, order_items


def prepare_orders(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    # filtra pedidos válidos para a análise e associa cada pedido ao cliente único

    # converte a data de compra para datetime
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    # mantém apenas pedidos dentro do período analisado
    orders = orders[
        orders["order_purchase_timestamp"] <= ANALYSIS_CUTOFF
    ].copy()

    # para a análise de comportamento e receita realizada, considera somente pedidos entregues
    orders = orders[
        orders["order_status"] == "delivered"
    ].copy()

    # adicionamos o identificador único do consumidor
    orders = orders.merge(
        customers[
            [
                "customer_id",
                "customer_unique_id",
            ]
        ],
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    return orders


def calculate_order_values(
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    # consolida os itens de cada pedido.

    # o agrupamento é feito antes de qualquer relacionamento com outras tabelas para evitar duplicação de valores

    order_values = (
        order_items
        .groupby("order_id")
        .agg(
            product_value=("price", "sum"),
            freight_value=("freight_value", "sum"),
        )
        .reset_index()
    )

    # valor total do pedido segundo os itens + frete
    order_values["order_value"] = (
        order_values["product_value"]
        + order_values["freight_value"]
    )

    return order_values


def calculate_purchase_intervals(
    orders: pd.DataFrame,
) -> pd.DataFrame:
    # calcula o intervalo médio entre compras consecutivas de cada cliente

    orders = orders.sort_values(
        [
            "customer_unique_id",
            "order_purchase_timestamp",
        ]
    ).copy()

    # diferença entre a compra atual e a anterior
    orders["purchase_interval_days"] = (
        orders
        .groupby("customer_unique_id")[
            "order_purchase_timestamp"
        ]
        .diff()
        .dt.total_seconds()
        / 86400
    )

    # calcula a média apenas para clientes que possuem pelo menos duas compras
    intervals = (
        orders
        .dropna(subset=["purchase_interval_days"])
        .groupby("customer_unique_id")
        .agg(
            avg_purchase_interval_days=(
                "purchase_interval_days",
                "mean",
            )
        )
        .reset_index()
    )

    return intervals


def build_customer_behavior(
    orders: pd.DataFrame,
    order_values: pd.DataFrame,
    intervals: pd.DataFrame,
) -> pd.DataFrame:
    # cria uma linha consolidada por cliente

    # valor financeiro de cada pedido
    orders = orders.merge(
        order_values[
            [
                "order_id",
                "order_value",
            ]
        ],
        on="order_id",
        how="left",
        validate="one_to_one",
    )

    # comportamento do cliente
    customer_behavior = (
        orders
        .groupby("customer_unique_id")
        .agg(
            first_purchase_date=(
                "order_purchase_timestamp",
                "min",
            ),
            last_purchase_date=(
                "order_purchase_timestamp",
                "max",
            ),
            total_orders=(
                "order_id",
                "nunique",
            ),
            total_spent=(
                "order_value",
                "sum",
            ),
            average_order_value=(
                "order_value",
                "mean",
            ),
        )
        .reset_index()
    )

    # intervalo médio entre compras
    customer_behavior = customer_behavior.merge(
        intervals,
        on="customer_unique_id",
        how="left",
        validate="one_to_one",
    )

    # recência: quantos dias se passaram entre a última compra do cliente e a data de corte
    customer_behavior["days_since_last_purchase"] = (
        ANALYSIS_CUTOFF
        - customer_behavior["last_purchase_date"]
    ).dt.total_seconds() / 86400

    # classificação simples baseada na frequência observada
    customer_behavior["customer_type"] = "one_time"

    customer_behavior.loc[
        customer_behavior["total_orders"] >= 2,
        "customer_type",
    ] = "repeat"

    return customer_behavior


def validate_customer_behavior(
    customer_behavior: pd.DataFrame,
) -> None:
    # executa verificações básicas na tabela analítica

    print("\n" + "=" * 70)
    print("VALIDAÇÃO CUSTOMER BEHAVIOR")
    print("=" * 70)

    print(
        f"\nClientes: "
        f"{len(customer_behavior):,}"
    )

    print(
        f"Pedidos consolidados: "
        f"{customer_behavior['total_orders'].sum():,}"
    )

    print(
        f"Clientes recorrentes: "
        f"{(customer_behavior['total_orders'] >= 2).sum():,}"
    )

    print(
        f"Clientes de uma compra: "
        f"{(customer_behavior['total_orders'] == 1).sum():,}"
    )

    print("\nTipos de cliente:")

    print(
        customer_behavior["customer_type"]
        .value_counts()
    )

    print("\nTotal gasto:")

    print(
        f"R$ {customer_behavior['total_spent'].sum():,.2f}"
    )

    print("\nRecência:")

    print(
        customer_behavior[
            "days_since_last_purchase"
        ].describe()
    )

    # verifica se existem clientes sem identificador
    null_customer_ids = (
        customer_behavior["customer_unique_id"]
        .isna()
        .sum()
    )

    print(
        f"\nClientes sem customer_unique_id: "
        f"{null_customer_ids:,}"
    )


def main() -> None:
    # executa a construção da tabela customer_behavior

    customers, orders, order_items = load_data()

    orders = prepare_orders(customers, orders)

    order_values = calculate_order_values(order_items)

    intervals = calculate_purchase_intervals(orders)

    customer_behavior = build_customer_behavior(orders, order_values, intervals)

    validate_customer_behavior(customer_behavior)

    # cria a pasta de saída caso ela ainda não exista
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    # salva a primeira tabela analítica
    output_path = (output_dir / "customer_behavior.csv")

    customer_behavior.to_csv(output_path, index=False)

    print(f"\nArquivo salvo em: {output_path}")


if __name__ == "__main__":
    main()