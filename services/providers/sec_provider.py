from typing import Any, Dict
import requests

from services.providers.base_provider import BaseProvider
from services.providers.sec_fact_retention import (
    retain_periodic_facts,
)


SEC_HEADERS = {
    "User-Agent": "VelesAnalytics/0.1 contact: steven.andreev@example.com",
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov",
}


class SECProvider(BaseProvider):
    name = "sec"
    capabilities = {"filings", "company_facts"}

    def health_check(self) -> Dict[str, Any]:
        try:
            r = requests.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers={"User-Agent": SEC_HEADERS["User-Agent"]},
                timeout=10,
            )
            return {
                "provider": self.name,
                "status": "online" if r.status_code == 200 else "degraded",
                "http_status": r.status_code,
                "note": "SEC EDGAR reachable.",
            }
        except Exception as e:
            return {
                "provider": self.name,
                "status": "error",
                "error": str(e),
            }

    def _ticker_to_cik(self, ticker: str) -> str:
        ticker = ticker.upper().strip()

        r = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers={"User-Agent": SEC_HEADERS["User-Agent"]},
            timeout=15,
        )
        r.raise_for_status()

        data = r.json()

        for _, row in data.items():
            if row.get("ticker", "").upper() == ticker:
                return str(row["cik_str"]).zfill(10)

        raise ValueError(f"No SEC CIK found for ticker: {ticker}")

    def get_filings(self, ticker: str) -> Dict[str, Any]:
        ticker = ticker.upper().strip()
        cik = self._ticker_to_cik(ticker)

        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        r = requests.get(url, headers=SEC_HEADERS, timeout=20)
        r.raise_for_status()

        data = r.json()
        recent = data.get("filings", {}).get("recent", {})

        forms = recent.get("form", [])
        accession_numbers = recent.get("accessionNumber", [])
        filing_dates = recent.get("filingDate", [])
        report_dates = recent.get("reportDate", [])
        primary_docs = recent.get("primaryDocument", [])

        filings = []
        for i in range(min(10, len(forms))):
            filings.append({
                "form": forms[i],
                "accession_number": accession_numbers[i] if i < len(accession_numbers) else "",
                "filing_date": filing_dates[i] if i < len(filing_dates) else "",
                "report_date": report_dates[i] if i < len(report_dates) else "",
                "primary_document": primary_docs[i] if i < len(primary_docs) else "",
            })

        return {
            "ticker": ticker,
            "cik": cik,
            "source": "SEC EDGAR submissions API",
            "status": "live",
            "company_name": data.get("name"),
            "sic": data.get("sic"),
            "sic_description": data.get("sicDescription"),
            "filings": filings,
        }

    def get_company_facts(self, ticker: str) -> Dict[str, Any]:
        ticker = ticker.upper().strip()
        cik = self._ticker_to_cik(ticker)

        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        r = requests.get(url, headers=SEC_HEADERS, timeout=25)
        r.raise_for_status()

        data = r.json()
        facts = data.get("facts", {}).get("us-gaap", {})

        useful_fields = [
            # Revenue
            "Revenues",
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "SalesRevenueNet",

            # Income statement
            "ResearchAndDevelopmentExpense",
            "OperatingIncomeLoss",
            "NetIncomeLoss",

            # Cash and liquidity
            "CashAndCashEquivalentsAtCarryingValue",
            "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",

            # Debt and financing obligations
            "ShortTermBorrowings",
            "ShortTermDebtCurrent",
            "DebtCurrent",
            "LongTermDebtCurrent",
            "LongTermDebtNoncurrent",
            "LongTermDebt",
            "LongTermDebtAndFinanceLeaseObligations",
            "LongTermDebtAndFinanceLeaseObligationsCurrent",
            "LongTermDebtAndFinanceLeaseObligationsNoncurrent",
            "NotesPayableCurrent",
            "NotesPayableNoncurrent",
            "NotesPayable",
            "FinanceLeaseLiabilityCurrent",
            "FinanceLeaseLiabilityNoncurrent",
            "OperatingLeaseLiabilityCurrent",
            "OperatingLeaseLiabilityNoncurrent",
            "OperatingLeaseLiability",

            # Cash flow
            "NetCashProvidedByUsedInOperatingActivities",
            "PaymentsToAcquirePropertyPlantAndEquipment",
            "PaymentsToAcquireProductiveAssets",
            "PaymentsToAcquireIntangibleAssets",

            # Balance sheet
            "Assets",
            "Liabilities",
            "StockholdersEquity",
        ]

        extracted = {}

        for field in useful_fields:
            if field not in facts:
                continue

            units = facts[field].get("units", {})
            usd_values = units.get("USD") or units.get("shares") or []

            if not usd_values:
                continue

            latest = retain_periodic_facts(
                usd_values,
                limit=80,
            )

            extracted[field] = [
                {
                    "fy": item.get("fy"),
                    "fp": item.get("fp"),
                    "form": item.get("form"),
                    "filed": item.get("filed"),
                    "start": item.get("start"),
                    "end": item.get("end"),
                    "frame": item.get("frame"),
                    "accession_number": item.get("accn"),
                    "value": item.get("val"),
                }
                for item in latest
            ]

        return {
            "ticker": ticker,
            "cik": cik,
            "source": "SEC EDGAR companyfacts API",
            "status": "live",
            "entity_name": data.get("entityName"),
            "facts": extracted,
        }
