from pathlib import Path

import pandas as pd


# diretório onde estão os dados brutos do projeto
RAW_DATA_DIR = Path("data/raw")

# data de corte escolhida para evitar usar o período incompleto de setembro/outubro de 2018
ANALYSIS_CUTOFF = pd.Timestamp("2018-08-31 23:59:59")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    # carrega clientes e pedidos

    customers = pd.read_csv(
        RAW_DATA_DIR / "olist_customers_dataset.csv"
    )

    orders = pd.read_csv(
        RAW_DATA_DIR / "olist_orders_dataset.csv"
    )

    return customers, orders


def prepare_orders(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    # relaciona pedidos aos clientes únicos e prepara os dados para análise temporal

    # converte a data de compra de texto para datetime
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    # mantém apenas pedidos realizados até a data de corte
    orders = orders[
        orders["order_purchase_timestamp"] <= ANALYSIS_CUTOFF
    ].copy()

    # usa apenas pedidos efetivamente entregues para análise
    orders = orders[
        orders["order_status"] == "delivered"
    ].copy()

    # adiciona o identificador único do consumidor
    orders = orders.merge(
        customers[
            ["customer_id", "customer_unique_id"]
        ],
        on="customer_id",
        how="left",
    )

    return orders


def calculate_purchase_intervals(
    orders: pd.DataFrame,
) -> pd.DataFrame:
    # calcula o intervalo entre compras consecutivas de cada cliente

    # ordena cronologicamente as compras de cada cliente
    orders = orders.sort_values(
        ["customer_unique_id", "order_purchase_timestamp"]
    ).copy()

    # calcula a diferença entre uma compra e a anterior
    orders["days_since_previous_order"] = (
        orders
        .groupby("customer_unique_id")[
            "order_purchase_timestamp"
        ]
        .diff()
        .dt.total_seconds()
        / 86400
    )

    # remove a primeira compra de cada cliente que não possui uma compra anterior
    intervals = orders.dropna(
        subset=["days_since_previous_order"]
    ).copy()

    return intervals


def analyze_intervals(intervals: pd.DataFrame) -> None:
    # apresenta estatísticas sobre os intervalos entre compras

    print("\n" + "=" * 70)
    print("INTERVALO ENTRE COMPRAS")
    print("=" * 70)

    if intervals.empty:
        print("\nNão existem clientes com compras recorrentes.")
        return

    interval_series = intervals[
        "days_since_previous_order"
    ]

    print(
        f"\nIntervalos analisados: "
        f"{len(interval_series):,}"
    )

    print(
        f"Menor intervalo: "
        f"{interval_series.min():.1f} dias"
    )

    print(
        f"Mediana: "
        f"{interval_series.median():.1f} dias"
    )

    print(
        f"Média: "
        f"{interval_series.mean():.1f} dias"
    )

    print(
        f"Percentil 75: "
        f"{interval_series.quantile(0.75):.1f} dias"
    )

    print(
        f"Percentil 90: "
        f"{interval_series.quantile(0.90):.1f} dias"
    )

    print(
        f"Percentil 95: "
        f"{interval_series.quantile(0.95):.1f} dias"
    )

    print(
        f"Maior intervalo: "
        f"{interval_series.max():.1f} dias"
    )


def analyze_customer_frequency(
    orders: pd.DataFrame,
) -> None:
    # analisa a frequência de compra dos clientes

    print("\n" + "=" * 70)
    print("FREQUÊNCIA DE COMPRA")
    print("=" * 70)

    customer_frequency = (
        orders
        .groupby("customer_unique_id")
        .agg(
            total_orders=("order_id", "nunique"),
            first_purchase=("order_purchase_timestamp", "min"),
            last_purchase=("order_purchase_timestamp", "max"),
        )
    )

    customer_frequency["customer_lifetime_days"] = (
        customer_frequency["last_purchase"]
        - customer_frequency["first_purchase"]
    ).dt.days

    print("\nEstatísticas de pedidos por cliente:")

    print(
        customer_frequency["total_orders"].describe()
    )

    print("\nClientes recorrentes:")

    repeat_customers = customer_frequency[
        customer_frequency["total_orders"] > 1
    ]

    print(
        f"{len(repeat_customers):,}"
    )


def main() -> None:
    # executa a análise de comportamento de compra

    customers, orders = load_data()

    orders = prepare_orders(
        customers,
        orders,
    )

    print("\n" + "=" * 70)
    print("BASE ANALÍTICA")
    print("=" * 70)

    print(
        f"\nPedidos considerados: "
        f"{len(orders):,}"
    )

    print(
        f"Clientes considerados: "
        f"{orders['customer_unique_id'].nunique():,}"
    )

    intervals = calculate_purchase_intervals(
        orders
    )

    analyze_intervals(intervals)

    analyze_customer_frequency(
        orders
    )


if __name__ == "__main__":
    main()