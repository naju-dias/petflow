from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


# ============================================================
# CONFIGURAÇÕES
# ============================================================

RAW_DATA_DIR = Path("data/raw")

DATABASE_URL = (
    "postgresql+psycopg2://"
    "petflow:petflow@localhost:5432/petflow"
)


# ============================================================
# CONEXÃO
# ============================================================

engine = create_engine(DATABASE_URL)


# ============================================================
# CONFIGURAÇÃO DOS DATASETS
# ============================================================

DATASETS = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
}


# ============================================================
# LOAD
# ============================================================

def load_dataset(
    table_name: str,
    filename: str,
) -> None:
    """
    Carrega um CSV da camada RAW para a camada STAGING.
    """

    file_path = RAW_DATA_DIR / filename

    print(
        f"\nCarregando: {filename}"
    )

    # lê o arquivo CSV.
    df = pd.read_csv(file_path)

    print(
        f"Registros encontrados: {len(df):,}"
    )

    # envia os dados para PostgreSQL.
    #
    # if_exists='replace' significa que, durante nosso
    # desenvolvimento local, a tabela será recriada.
    df.to_sql(
        name=table_name,
        con=engine,
        schema="staging",
        if_exists="replace",
        index=False,
        chunksize=5_000,
        method="multi",
    )

    print(
        f"OK: staging.{table_name}"
    )


def main() -> None:
    # executa a carga de todos os datasets

    print("=" * 70)
    print("PETFLOW - LOAD STAGING")
    print("=" * 70)

    for table_name, filename in DATASETS.items():

        load_dataset(
            table_name,
            filename,
        )

    print("\nCarga concluída.")


if __name__ == "__main__":
    main()