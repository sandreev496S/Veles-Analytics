from pathlib import Path

path = Path("app.py")
text = path.read_text()

text = text.replace(
'''        section_title("Risk Analysis", "Monte Carlo simulation, valuation distribution, percentile outcomes, and scenario risk.")

        simulations = st.slider(''',
'''        with st.expander("Risk Analysis Suite", expanded=False):
            section_title("Risk Analysis", "Monte Carlo simulation, valuation distribution, percentile outcomes, and scenario risk.")

            simulations = st.slider(''',
1
)

risk_start = text.index('''        with st.expander("Risk Analysis Suite", expanded=False):''')
risk_end = text.index('''        rnpv_valuation_df = pd.DataFrame(''', risk_start)

risk_block = text[risk_start:risk_end]
lines = risk_block.splitlines()

fixed = []
for idx, line in enumerate(lines):
    if idx == 0:
        fixed.append(line)
    elif line.startswith("        "):
        fixed.append("    " + line)
    else:
        fixed.append(line)

text = text[:risk_start] + "\n".join(fixed) + "\n" + text[risk_end:]

path.write_text(text)
print("Collapsed rNPV risk analysis suite.")
