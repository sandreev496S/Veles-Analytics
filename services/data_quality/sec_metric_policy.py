from __future__ import annotations


SEC_CONCEPT_POLICY: dict[str, tuple[str, ...]] = {
    "total_revenue": (
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet",
    ),
    "operating_revenue": (
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
    ),
    "research_and_development_expense": (
        "ResearchAndDevelopmentExpense",
    ),
    "operating_income": (
        "OperatingIncomeLoss",
    ),
    "net_income": (
        "NetIncomeLoss",
    ),
    "cash_and_cash_equivalents": (
        "CashAndCashEquivalentsAtCarryingValue",
    ),
    "cash_including_restricted_cash": (
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
    ),
    "stockholders_equity": (
        "StockholdersEquity",
    ),
    "operating_cash_flow": (
        "NetCashProvidedByUsedInOperatingActivities",
    ),
    "property_and_equipment_purchases": (
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ),
    "intangible_asset_purchases": (
        "PaymentsToAcquireIntangibleAssets",
    ),
    "short_term_borrowings": (
        "ShortTermBorrowings",
        "ShortTermDebtCurrent",
    ),
    "current_financial_debt": (
        "LongTermDebtAndFinanceLeaseObligationsCurrent",
        "DebtCurrent",
        "LongTermDebtCurrent",
        "NotesPayableCurrent",
    ),
    "noncurrent_financial_debt": (
        "LongTermDebtAndFinanceLeaseObligationsNoncurrent",
        "LongTermDebtNoncurrent",
        "NotesPayableNoncurrent",
    ),
    "total_financial_debt": (
        "LongTermDebtAndFinanceLeaseObligations",
        "LongTermDebt",
        "NotesPayable",
    ),
    "finance_lease_current": (
        "FinanceLeaseLiabilityCurrent",
    ),
    "finance_lease_noncurrent": (
        "FinanceLeaseLiabilityNoncurrent",
    ),
    "operating_lease_current": (
        "OperatingLeaseLiabilityCurrent",
    ),
    "operating_lease_noncurrent": (
        "OperatingLeaseLiabilityNoncurrent",
        "OperatingLeaseLiability",
    ),
}
