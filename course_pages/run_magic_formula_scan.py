import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from course_pages.functions.stock_utils import fetch_stock_list
from course_pages.chapter1_app import _filter_morningstar_universe
from course_pages.chapter1_app import get_row_with_retries

OUT = Path("magic_formula_scan.csv")
SAVE_EVERY = 20
MAX_WORKERS = 5

MIN_MARKET_CAP = 5_000_000_000
EXCLUDED_SECTORS = {"Financial Services", "Real Estate", "Utilities"}

##SYMBOLS = ["NVDA", "AAPL", "MSFT"]  # ✅ keep your test list


def load_existing_done_symbols() -> set[str]:
    if OUT.exists():
        try:
            df = pd.read_csv(OUT, usecols=["symbol"])
            return set(df["symbol"].astype(str))
        except Exception:
            return set()
    return set()


def append_rows(rows: list[dict]):
    if not rows:
        return
    df = pd.DataFrame(rows)
    if OUT.exists():
        df.to_csv(OUT, mode="a", header=False, index=False)
    else:
        df.to_csv(OUT, mode="w", header=True, index=False)


def main():
    # Streamlit secrets aren’t needed here because chapter1_app already reads API_KEY for the app,
    # but we need the key for direct calls in this script:
    from pathlib import Path
    try:
        import tomllib
        toml_loads = tomllib.loads
    except ModuleNotFoundError:
        import tomli
        toml_loads = tomli.loads

    secrets = toml_loads(Path(".streamlit/secrets.toml").read_text(encoding="utf-8"))
    api_key = secrets["api"]["fmp_key"]

    stock_list = fetch_stock_list(api_key)
    stock_list = _filter_morningstar_universe(stock_list)

    symbols = stock_list["symbol"].dropna().unique().tolist()

    done = load_existing_done_symbols()
    symbols = [s for s in symbols if s not in done]


    print(f"Remaining symbols: {len(symbols)}")
    print(f"Using {MAX_WORKERS} threads")
    print(f"Output: {OUT.resolve()}")

    def append_rows(rows: list[dict]):
        if not rows:
            return
        df = pd.DataFrame(rows)
        if OUT.exists():
            df.to_csv(OUT, mode="a", header=False, index=False)
        else:
            df.to_csv(OUT, mode="w", header=True, index=False)


    buffer = []
    processed = 0

    def compute(symbol: str):
        return get_row_with_retries(
            symbol,
            api_key,
            tries=4,
            min_market_cap=MIN_MARKET_CAP,
            excluded_sectors=EXCLUDED_SECTORS,
        )

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(compute, sym): sym for sym in symbols}

        for future in as_completed(futures):
            sym = futures[future]
            processed += 1

            try:
                row = future.result()
                if row:
                    buffer.append(row)
                    print(f"{sym},ok")
                else:
                    print(f"{sym},filtered_or_none")
            except Exception as e:
                print(f"[ERROR] {sym}: {e}")

            if processed % SAVE_EVERY == 0:
                append_rows(buffer)
                buffer = []
                print(f"Checkpoint: {processed}/{len(symbols)}")

        append_rows(buffer)

    print("Done.")


if __name__ == "__main__":
    main()
