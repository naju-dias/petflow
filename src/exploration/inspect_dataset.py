from pathlib import Path

import pandas as pd


# diretório onde estão os dados brutos do projeto
RAW_DATA_DIR = Path("data/raw")


def inspect_file(file_path: Path) -> None:
    # carrega um CSV e apresenta informações básicaspara entendermos sua estrutura e qualidade
    print("\n" + "=" * 70)
    print(f"ARQUIVO: {file_path.name}")
    print("=" * 70)

    # carrega o CSV para um DataFrame
    df = pd.read_csv(file_path)

    # mostra quantidade de linhas e colunas
    print(f"\nLinhas: {df.shape[0]:,}")
    print(f"Colunas: {df.shape[1]}")

    # mostra os nomes das colunas
    print("\nColunas:")
    for column in df.columns:
        print(f"  - {column}")

    # mostra os tipos de dados
    print("\nTipos:")
    print(df.dtypes)

    # mostra quantidade de valores ausentes
    print("\nValores ausentes:")
    missing = df.isna().sum()

    # mostra apenas colunas que possuem valores ausentes
    print(missing[missing > 0].sort_values(ascending=False))

    # mostra as primeiras linhas
    print("\nPrimeiras linhas:")
    print(df.head(3))


def main() -> None:
    # inspeciona todos os arquivos CSV presentes em data/raw

    # busca todos os arquivos CSV da pasta
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("Nenhum arquivo CSV encontrado em data/raw.")
        return

    print(f"Encontrados {len(csv_files)} arquivos CSV.")

    for file_path in csv_files:
        inspect_file(file_path)


if __name__ == "__main__":
    main()