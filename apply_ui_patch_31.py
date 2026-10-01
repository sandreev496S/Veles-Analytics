from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with notes_tab:
        activity_item(
            "Research Notes",
            "Analyst notes, thesis updates, risks, catalysts, and diligence questions will live here.",
            "Notes"
        )'''

new = '''    with notes_tab:
        note_key = f"research_note_{selected_company}"

        existing_note = st.session_state.get(note_key, "")

        section_title(
            "Research Notes",
            f"Analyst workspace for {selected_company}."
        )

        note_text = st.text_area(
            "Company research note",
            value=existing_note,
            height=260,
            placeholder="Write thesis updates, risks, catalysts, diligence questions, funding notes, or technical observations here.",
            key=f"research_note_input_{selected_company}",
        )

        if st.button(
            "Save Research Note",
            key=f"save_research_note_{selected_company}",
        ):
            st.session_state[note_key] = note_text
            st.success(f"Research note saved for {selected_company}.")

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
    raise SystemExit("Could not find Notes tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 31 applied: Research Notes workspace added.")
