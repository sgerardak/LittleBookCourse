import pandas as pd
import fmpsdk

def fetch_financial_data(stock_symbol, api_key):
    """Fetch income statement, balance sheet, and cash flow data for a given stock symbol."""
    income_statement = pd.DataFrame(fmpsdk.income_statement(apikey=api_key, symbol=stock_symbol))
    balance_sheet = pd.DataFrame(fmpsdk.balance_sheet_statement(apikey=api_key, symbol=stock_symbol))
    cash_flow = pd.DataFrame(fmpsdk.cash_flow_statement(apikey=api_key, symbol=stock_symbol))
    return income_statement, balance_sheet, cash_flow

def process_data(income_statement, balance_sheet, cash_flow):
    """Process and merge financial data to prepare it for analysis."""
    # Process income statement
    income_statement_focus = income_statement[[
        "calendarYear", "symbol", "grossProfit", "revenue", "operatingIncome", "netIncome", "epsdiluted","weightedAverageShsOutDil"
    ]].rename(columns={
        "revenue": "TotalRevenue",
        "operatingIncome": "OperatingIncome",
        "netIncome": "IncomeCommonStockholders",
        "epsdiluted": "DilutedEps",
    })

    # Process balance sheet
    balance_sheet["Liabilities_A-E"] = balance_sheet["totalAssets"] - balance_sheet["totalStockholdersEquity"]
    balance_sheet_focus = balance_sheet[[
        "calendarYear", "symbol", "totalAssets", "totalStockholdersEquity", "Liabilities_A-E",
        "totalLiabilities", "totalCurrentLiabilities"
    ]].rename(columns={
        "totalAssets": "TotalAssets",
        "totalStockholdersEquity": "Stockholdersequity",
        "totalLiabilities": "TotalNonCurrentLiabilitiesNetMinorityInterest",
        "totalCurrentLiabilities": "CurrentLiabilities"
    })

    # Process cash flow
    cash_flow_focus = cash_flow[[
        "calendarYear", "symbol", "debtRepayment", "netCashUsedProvidedByFinancingActivities", 
        "dividendsPaid", "commonStockRepurchased", "commonStockIssued"
    ]].rename(columns={
        "debtRepayment": "RepaymentOfDebt",
        "commonStockRepurchased": "RepurchaseOfCapitalStock",
        "commonStockIssued": "IssuanceOfCapitalStock",
        "dividendsPaid": "CashDividendsPaid"
    })

    # Merge data
    ticker_data = pd.merge(income_statement_focus, balance_sheet_focus, how='left', on=["calendarYear", "symbol"])
    ticker_data = pd.merge(ticker_data, cash_flow_focus, how='left', on=["calendarYear", "symbol"])

    # Additional calculations
    ticker_data["Liabilities_CL-NL"] = ticker_data["CurrentLiabilities"] + ticker_data["TotalNonCurrentLiabilitiesNetMinorityInterest"]
    ticker_data["Issuance_Repayment"] = (
        ticker_data["IssuanceOfCapitalStock"] + ticker_data["RepurchaseOfCapitalStock"]
    )
    ticker_data["Issuance_Repurchase_Stocks"] = ticker_data["IssuanceOfCapitalStock"] + ticker_data["RepurchaseOfCapitalStock"]
    ticker_data["debt_assets"] = ticker_data["Liabilities_CL-NL"] / ticker_data["TotalAssets"]
    ticker_data["net_margin"] = ticker_data["IncomeCommonStockholders"] / ticker_data["TotalRevenue"]
    ticker_data["oper_margin"] = ticker_data["OperatingIncome"] / ticker_data["TotalRevenue"]
    ticker_data["gross_margin"] = ticker_data["grossProfit"] / ticker_data["TotalRevenue"]

    return ticker_data

def calculate_results(ticker_data, interest_rate, time_range):
    """Perform calculations to determine financial metrics and intrinsic value."""
    avg_stock = ticker_data["weightedAverageShsOutDil"].mean()
    tasa = interest_rate / 100
    multiplicador = 1 / tasa

    # Determine the period based on time range
    period = {"3y": 3, "5y": 5, "10y": 10}.get(time_range, 5)

    ticker_results = {
        "ticker": [ticker_data["symbol"].iloc[0]],
        "avg_eps": [ticker_data["DilutedEps"].mean()],
        "iv_eps": [multiplicador * ticker_data["DilutedEps"].mean()],
        "avg_stock": avg_stock,
        "debt": [
            multiplicador * (
                (ticker_data["IncomeCommonStockholders"].sum() - ticker_data["Issuance_Repayment"].sum()) / period
            ) / ticker_data["Stockholdersequity"].mean()
        ],
        "intrinsic_value": multiplicador * (
            (((ticker_data["TotalAssets"].iloc[0] - ticker_data["TotalAssets"].iloc[-1]) / period / avg_stock) +
             ((-1 * ticker_data["Issuance_Repurchase_Stocks"].sum() - ticker_data["CashDividendsPaid"].sum()) / period / avg_stock))
        )
    }

    return ticker_results
