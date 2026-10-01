from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        if st.button(
            "Save Thesis Workspace",
            key=f"save_thesis_workspace_{selected_company}",
        ):
            st.session_state[thesis_key] = thesis
            st.session_state[catalysts_key] = catalysts
            st.session_state[risks_key] = risks
            st.session_state[questions_key] = questions
            st.success(f"Investment thesis workspace saved for {selected_company}.")'''

new = '''        if st.button(
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

        if st.button(
            "Save Thesis Workspace",
            key=f"save_thesis_workspace_{selected_company}",
        ):
            st.session_state[thesis_key] = thesis
            st.session_state[catalysts_key] = catalysts
            st.session_state[risks_key] = risks
            st.session_state[questions_key] = questions
            st.success(f"Investment thesis workspace saved for {selected_company}.")'''

if old not in text:
    raise SystemExit("Could not find Save Thesis Workspace button block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 33 applied: AI-style draft thesis button added.")
