from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

text = text.replace(
    "Analyst Command Center",
    "Valuation & Research Console",
    1,
)

path.write_text(text)
print("Dashboard command center label refined.")
