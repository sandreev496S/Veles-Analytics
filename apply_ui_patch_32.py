from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        if st.session_state.get(note_key):
            activity_item(
                "Saved Note",
                st.session_state[note_key][:300] + ("..." if len(st.session_state[note_key]) > 300 else ""),
                "Notes"
            )
        else:
            activity_item(
                "No Saved Note Yet",
                "Use the note field above to start building a company-specific research log.",
                "Notes"
            )'''

new = '''        section_title(
            "Investment Thesis",
            "Structured diligence fields for institutional research."
        )

        thesis_key = f"thesis_{selected_company}"
        catalysts_key = f"catalysts_{selected_company}"
        risks_key = f"risks_{selected_company}"
        questions_key = f"questions_{selected_company}"

        thesis = st.text_area(
            "Thesis",
            value=st.session_state.get(thesis_key, ""),
            height=140,
            key=f"thesis_input_{selected_company}",
        )

        catalysts = st.text_area(
            "Catalysts",
            value=st.session_state.get(catalysts_key, ""),
            height=120,
            key=f"catalysts_input_{selected_company}",
        )

        risks = st.text_area(
            "Risks",
            value=st.session_state.get(risks_key, ""),
            height=120,
            key=f"risks_input_{selected_company}",
        )

        questions = st.text_area(
            "Open Questions",
            value=st.session_state.get(questions_key, ""),
            height=120,
            key=f"questions_input_{selected_company}",
        )

        if st.button(
            "Save Thesis Workspace",
            key=f"save_thesis_workspace_{selected_company}",
        ):
            st.session_state[thesis_key] = thesis
            st.session_state[catalysts_key] = catalysts
            st.session_state[risks_key] = risks
            st.session_state[questions_key] = questions
            st.success(f"Investment thesis workspace saved for {selected_company}.")

        if st.session_state.get(note_key):
            activity_item(
                "Saved Note",
                st.session_state[note_key][:300] + ("..." if len(st.session_state[note_key]) > 300 else ""),
                "Notes"
            )
        else:
            activity_item(
                "No Saved Note Yet",
                "Use the note field above to start building a company-specific research log.",
                "Notes"
            )'''

if old not in text:
    raise SystemExit("Could not find saved note display block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 32 applied: Investment Thesis workspace added.")
