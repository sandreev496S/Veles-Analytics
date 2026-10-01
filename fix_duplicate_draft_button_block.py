from pathlib import Path

path = Path("app.py")
text = path.read_text()

block = '''        if st.button(
            "Draft Thesis From Company Profile",
            key=f"draft_thesis_{selected_company}",
        ):
            st.session_state[thesis_key] = (
                f"{selected_company} is positioned within the {selected_profile['focus']} segment of neurotechnology. "
                f"The company may be attractive if it can convert technical differentiation into clinical adoption, regulatory progress, and durable market leadership."
            )
            st.session_state[catalysts_key] = (
                "Clinical progress; regulatory milestones; new funding rounds; strategic partnerships; published performance data."
            )
            st.session_state[risks_key] = selected_profile["risk"]
            st.session_state[questions_key] = (
                "What is the clearest regulatory pathway? What evidence supports commercial adoption? "
                "How differentiated is the technology versus direct competitors? What valuation is justified by current traction?"
            )
            st.success(f"Draft thesis created for {selected_company}. Refresh or switch tabs to view populated fields.")

'''

count = text.count(block)

if count < 2:
    raise SystemExit(f"Expected duplicate block at least twice, found {count}.")

first = text.find(block)
second = text.find(block, first + len(block))

text = text[:second] + text[second + len(block):]

path.write_text(text)

print("Removed duplicate Draft Thesis button block.")
