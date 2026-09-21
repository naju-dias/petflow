from pathlib import Path

import pandas as pd


RAW_DATA_DIR = Path("data/raw")

ANALYSIS_CUTOFF = pd.Timestamp("2018-08-31 23:59:59")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # carrega pedidos, itens e pagamentos

    orders = pd.read_csv(
        RAW_DATA_DIR / "olist_orders_dataset.csv"
    )

    order_items = pd.read_csv(
        RAW_DATA_DIR / "olist_order_items_dataset.csv"
    )

    payments = pd.read_csv(
        RAW_DATA_DIR / "olist_order_payments_dataset.csv"
    )

    return orders, order_items, payments


def prepare_orders(orders: pd.DataFrame) -> pd.DataFrame:
    # prepara os pedidos utilizados na análise

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    # somente pedidos até a data de corte
    orders = orders[
        orders["order_purchase_timestamp"] <= ANALYSIS_CUTOFF
    ].copy()

    # usa pedidos entregues para analisar receita
    orders = orders[
        orders["order_status"] == "delivered"
    ].copy()

    return orders


def calculate_item_values(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    # calcula o valor dos produtos e frete por pedido
    
    order_values = (
        order_items
        .groupby("order_id")
        .agg(
            product_value=("price", "sum"),
            freight_value=("freight_value", "sum"),
        )
        .reset_index()
    )

    # relaciona os valores agregados aos pedidos
    result = orders[
        ["order_id", "customer_id"]
    ].merge(
        order_values,
        on="order_id",
        how="left",
    )

    return result


def calculate_payment_values(
    orders: pd.DataFrame,
    payments: pd.DataFrame,
) -> pd.DataFrame:
    # soma os pagamentos por pedido antes de fazer join com outras tabelas

    payment_values = (
        payments
        .groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
        )
        .reset_index()
    )

    result = orders[
        ["order_id", "customer_id"]
    ].merge(
        payment_values,
        on="order_id",
        how="left",
    )

    return result


def compare_values(
    item_values: pd.DataFrame,
    payment_values: pd.DataFrame,
) -> None:
    # compara os valores derivados dos itens com os valores registrados nos pagamentos

    comparison = item_values.merge(
        payment_values[
            ["order_id", "payment_value"]
        ],
        on="order_id",
        how="left",
    )

    comparison["calculated_order_value"] = (
        comparison["product_value"]
        + comparison["freight_value"]
    )

    comparison["difference"] = (
        comparison["payment_value"]
        - comparison["calculated_order_value"]
    )

    print("\n" + "=" * 70)
    print("VALIDAÇÃO DE VALORES POR PEDIDO")
    print("=" * 70)

    print(
        f"\nPedidos analisados: "
        f"{len(comparison):,}"
    )

    print(
        f"Valor dos produtos: "
        f"R$ {comparison['product_value'].sum():,.2f}"
    )

    print(
        f"Frete: "
        f"R$ {comparison['freight_value'].sum():,.2f}"
    )

    print(
        f"Produtos + frete: "
        f"R$ {comparison['calculated_order_value'].sum():,.2f}"
    )

    print(
        f"Pagamentos: "
        f"R$ {comparison['payment_value'].sum():,.2f}"
    )

    print("\nDiferença média por pedido:")

    print(
        f"R$ {comparison['difference'].mean():,.2f}"
    )

    print("\nMaiores diferenças:")

    print(
        comparison
        .sort_values(
            "difference",
            key=lambda x: x.abs(),
            ascending=False,
        )
        [
            [
                "order_id",
                "product_value",
                "freight_value",
                "payment_value",
                "difference",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


def main() -> None:

    orders, order_items, payments = load_data()

    orders = prepare_orders(orders)

    item_values = calculate_item_values(
        orders,
        order_items,
    )

    payment_values = calculate_payment_values(
        orders,
        payments,
    )

    compare_values(
        item_values,
        payment_values,
    )


if __name__ == "__main__":
    main()