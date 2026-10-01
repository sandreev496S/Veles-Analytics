from datetime import date
from services.data.company_data_service import get_company_data
from services.reports.equity_report_assembler import assemble_equity_report
from services.reports.profiles import resolve_report_profile


def build_equity_report_v2(company_name, ticker, industry, description=""):
    today = date.today().strftime("%B %d, %Y")

    return {
        "company_name": company_name,
        "ticker": ticker.upper(),
        "industry": industry,
        "date": today,
        "prepared_by": "Veles Analytics",
        "description": description,
        "snapshot": {
            "Company": company_name,
            "Ticker": ticker.upper(),
            "Industry": industry,
            "Exchange": "NASDAQ",
            "Report Type": "Equity Research",
            "Prepared By": "Veles Analytics",
            "Date": today,
        },
        "thesis_points": [
            "AI-enabled drug discovery platform may improve speed and scale of biological experimentation.",
            "Large proprietary datasets and automated wet-lab infrastructure may create a data advantage.",
            "The company remains high-risk due to clinical, financing, and commercialization uncertainty.",
        ],
        "risks": [
            "Clinical trial failure or delays",
            "High cash burn and future dilution risk",
            "Competitive pressure from other AI drug discovery companies",
            "Regulatory uncertainty",
            "Difficulty translating platform promise into approved therapies",
        ],
        "competitors": [
            ["Company", "Focus", "Positioning"],
            ["Schrödinger", "Computational chemistry", "Software/platform peer"],
            ["Exscientia", "AI drug discovery", "Clinical-stage AI biotech"],
            ["Isomorphic Labs", "AI biology", "DeepMind-backed private competitor"],
            ["Relay Therapeutics", "Structure-based drug discovery", "Precision medicine competitor"],
        ],
        "financial_table": [
            ["Metric", "Commentary"],
            ["Revenue", "Review latest 10-K / 10-Q for collaboration and platform revenue."],
            ["Cash Runway", "Assess cash, equivalents, burn rate, and financing needs."],
            ["R&D Spend", "High R&D intensity expected for platform biotech companies."],
            ["Margins", "Early-stage biotech margins are less meaningful than runway and pipeline progress."],
        ],
        "sections": [
            ("Executive Summary", f"{company_name} ({ticker.upper()}) operates in the {industry} market. This report evaluates the company’s technology platform, competitive positioning, financial profile, valuation considerations, and key risks."),
            ("Company Overview", description or f"{company_name} is a biotechnology company operating within {industry}."),
            ("Technology & Platform Analysis", "The company should be assessed across data scale, automation, machine learning capabilities, biological validation, intellectual property, and ability to convert discovery insights into clinical assets."),
            ("Industry & Market Opportunity", f"The {industry} market is shaped by scientific validation, clinical trial execution, regulatory approval pathways, strategic partnerships, and investor appetite for platform biotechnology."),
            ("Competitive Landscape", "The competitive landscape includes AI drug discovery companies, computational biology firms, platform biotechnology companies, and large pharmaceutical partners building internal AI capabilities."),
            ("Financial Overview", "Financial diligence should focus on revenue quality, R&D spend, operating cash burn, cash runway, capital market dependence, and dilution risk."),
            ("Valuation Discussion", "Valuation should combine DCF, scenario analysis, comparable companies, pipeline-adjusted value, and strategic acquisition logic."),
            ("Bull / Base / Bear Case", "Bull case: successful pipeline validation and strategic partnerships. Base case: gradual progress with continued financing needs. Bear case: clinical setbacks, dilution, or weak platform translation."),
            ("Investment Thesis", f"{company_name} represents a high-uncertainty innovation-driven investment profile. The core question is whether the company can convert its technology platform into validated therapies, durable revenue, and defensible market leadership."),
            ("Disclaimer", "This report is for informational and portfolio demonstration purposes only. It is not investment advice or a recommendation to buy or sell securities."),
        ],
    }


def build_equity_report(company_name, ticker, industry, description=""):
    return build_equity_report_v2(company_name, ticker, industry, description)


def build_equity_report_from_ticker_v2(
    ticker: str,
    package: str | None = None,
):
    profile = resolve_report_profile(
        package
    )

    return assemble_equity_report(
        ticker,
        profile=profile,
    )
