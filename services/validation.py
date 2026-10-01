import re


class ValidationError(Exception):
    pass


BLOCKED_PATTERNS = [
    r"<script",
    r"</script",
    r"DROP\s+TABLE",
    r"DELETE\s+FROM",
    r"INSERT\s+INTO",
    r"UPDATE\s+.*SET",
    r"--",
    r";--",
]


def validate_name(value, field_name="Name", max_length=100):
    if value is None:
        raise ValidationError(f"{field_name} is required.")

    cleaned = str(value).strip()

    if not cleaned:
        raise ValidationError(f"{field_name} cannot be empty.")

    if len(cleaned) > max_length:
        raise ValidationError(f"{field_name} must be {max_length} characters or fewer.")

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, cleaned, flags=re.IGNORECASE):
            raise ValidationError(f"{field_name} contains unsafe content.")

    return cleaned


def validate_number(value, field_name, min_value=None, max_value=None):
    try:
        number = float(value)
    except Exception:
        raise ValidationError(f"{field_name} must be a number.")

    if min_value is not None and number < min_value:
        raise ValidationError(f"{field_name} must be at least {min_value}.")

    if max_value is not None and number > max_value:
        raise ValidationError(f"{field_name} must be no more than {max_value}.")

    return number


def validate_percentage(value, field_name, min_value=-1.0, max_value=1.0):
    return validate_number(
        value,
        field_name=field_name,
        min_value=min_value,
        max_value=max_value,
    )


def validate_integer(value, field_name, min_value=None, max_value=None):
    number = validate_number(value, field_name, min_value, max_value)

    if int(number) != number:
        raise ValidationError(f"{field_name} must be a whole number.")

    return int(number)


def validate_simulation_count(value, max_allowed=10000):
    return validate_integer(
        value,
        field_name="Monte Carlo simulations",
        min_value=100,
        max_value=max_allowed,
    )


def validate_standard_dcf_inputs(
    company_name,
    current_market_cap,
    cash,
    debt,
    shares,
    starting_revenue,
    forecast_years,
):
    return {
        "company_name": validate_name(company_name, "Company name"),
        "current_market_cap": validate_number(current_market_cap, "Current market cap", 0, 10_000_000),
        "cash": validate_number(cash, "Cash", 0, 10_000_000),
        "debt": validate_number(debt, "Debt", 0, 10_000_000),
        "shares": validate_number(shares, "Shares outstanding", 0.0001, 100_000),
        "starting_revenue": validate_number(starting_revenue, "Starting revenue", 0, 10_000_000),
        "forecast_years": validate_integer(forecast_years, "Forecast years", 1, 20),
    }


def validate_biotech_inputs(
    asset_name,
    eligible_patients,
    price_per_treatment,
    launch_year,
    forecast_years,
    years_to_peak,
    peak_penetration,
    probability_of_approval,
    operating_margin,
    tax_rate,
    discount_rate,
    annual_rd_cost,
    launch_cost,
    cash,
    debt,
    shares,
    current_market_cap,
):
    return {
        "asset_name": validate_name(asset_name, "Asset / company name"),
        "eligible_patients": validate_integer(eligible_patients, "Eligible patients", 0, 1_000_000_000),
        "price_per_treatment": validate_number(price_per_treatment, "Price per treatment", 0, 100_000_000),
        "launch_year": validate_integer(launch_year, "Launch year", 1, 50),
        "forecast_years": validate_integer(forecast_years, "Forecast years", 1, 50),
        "years_to_peak": validate_integer(years_to_peak, "Years to peak", 1, 50),
        "peak_penetration": validate_percentage(peak_penetration, "Peak penetration", 0, 1),
        "probability_of_approval": validate_percentage(probability_of_approval, "Probability of approval", 0, 1),
        "operating_margin": validate_percentage(operating_margin, "Operating margin", -1, 1),
        "tax_rate": validate_percentage(tax_rate, "Tax rate", 0, 1),
        "discount_rate": validate_percentage(discount_rate, "Discount rate", 0, 1),
        "annual_rd_cost": validate_number(annual_rd_cost, "Annual R&D cost", 0, 10_000_000),
        "launch_cost": validate_number(launch_cost, "Launch cost", 0, 10_000_000),
        "cash": validate_number(cash, "Cash", 0, 10_000_000),
        "debt": validate_number(debt, "Debt", 0, 10_000_000),
        "shares": validate_number(shares, "Shares outstanding", 0.0001, 100_000),
        "current_market_cap": validate_number(current_market_cap, "Current market cap", 0, 10_000_000),
    }
