def calculate_cost_of_equity(risk_free_rate, beta, equity_risk_premium, size_premium=0.0, company_specific_premium=0.0):
    return risk_free_rate + beta * equity_risk_premium + size_premium + company_specific_premium


def calculate_after_tax_cost_of_debt(pre_tax_cost_of_debt, tax_rate):
    return pre_tax_cost_of_debt * (1 - tax_rate)


def calculate_wacc(
    market_value_equity,
    market_value_debt,
    cost_of_equity,
    after_tax_cost_of_debt,
):
    total_capital = market_value_equity + market_value_debt

    if total_capital <= 0:
        return 0.0

    equity_weight = market_value_equity / total_capital
    debt_weight = market_value_debt / total_capital

    return equity_weight * cost_of_equity + debt_weight * after_tax_cost_of_debt
