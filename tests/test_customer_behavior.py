from pathlib import Path

import pandas as pd


CUSTOMER_BEHAVIOR_PATH = Path(
    "data/processed/customer_behavior.csv"
)


def load_customer_behavior() -> pd.DataFrame:
    # carrega a tabela analítica gerada pelo pipeline

    return pd.read_csv(
        CUSTOMER_BEHAVIOR_PATH
    )


def test_customer_count() -> None:
    # garante que a quantidade de clientes permaneça consistente com a análise

    df = load_customer_behavior()

    assert len(df) == 93_358


def test_order_count() -> None:
    # a soma dos pedidos por cliente deve representar os 96.478 pedidos entregues considerados na análise

    df = load_customer_behavior()

    assert df["total_orders"].sum() == 96_478


def test_customer_types() -> None:
    # verifica se a classificação de clientes está consistente

    df = load_customer_behavior()

    repeat_customers = (
        df["total_orders"] >= 2
    ).sum()

    one_time_customers = (
        df["total_orders"] == 1
    ).sum()

    assert repeat_customers == 2_801
    assert one_time_customers == 90_557


def test_customer_ids_are_unique() -> None:
    # a tabela customer_behavior deve possuir uma única linha por cliente

    df = load_customer_behavior()

    assert df["customer_unique_id"].is_unique


def test_customer_ids_are_not_null() -> None:
    # nenhum cliente pode estar sem identificador

    df = load_customer_behavior()

    assert df["customer_unique_id"].notna().all()


def test_spending_is_positive() -> None:
    # clientes considerados na análise devem possuir valor de pedido positivo

    df = load_customer_behavior()

    assert (df["total_spent"] > 0).all()


def test_purchase_dates_are_valid() -> None:
    # a primeira compra nunca pode acontecer depois da última compra

    df = load_customer_behavior()

    first_purchase = pd.to_datetime(
        df["first_purchase_date"]
    )

    last_purchase = pd.to_datetime(
        df["last_purchase_date"]
    )

    assert (first_purchase <= last_purchase).all()