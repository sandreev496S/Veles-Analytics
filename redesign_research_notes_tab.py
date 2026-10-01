from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        section_title(
            "Research Notes",
            f"Persistent analyst workspace for {selected_company}."
        )'''

new = '''        section_title(
            "Analyst Notebook",
            f"Persistent research notes, thesis development, catalysts, risks, and diligence questions for {selected_company}."
        )'''

if old not in text:
    raise SystemExit("Could not find Research Notes section title.")

text = text.replace(old, new, 1)

old = '''        note_text = st.text_area(
            "Company research note",
            value=(general_note_record or {}).get("content", ""),
            height=260,
            placeholder="Write thesis updates, risks, catalysts, diligence questions, funding notes, or technical observations here.",
            key=f"research_note_input_{selected_company}",
        )

        if st.button(
            "Save Research Note",
            key=f"save_research_note_{selected_company}",
        ):
            save_research_note(
                user_id=user_id,
                company_name=selected_company,
                note_type="general",
                content=note_text,
            )
            st.success(f"Research note saved for {selected_company}.")
            st.rerun()

        section_title(
            "Investment Thesis",
            "Structured diligence fields for institutional research."
        )

        thesis = st.text_area(
            "Thesis",
            value=(thesis_record or {}).get("content", ""),
            height=140,
            key=f"thesis_input_{selected_company}",
        )

        catalysts = st.text_area(
            "Catalysts",
            value=(catalysts_record or {}).get("content", ""),
            height=120,
            key=f"catalysts_input_{selected_company}",
        )

        risks = st.text_area(
            "Risks",
            value=(risks_record or {}).get("content", ""),
            height=120,
            key=f"risks_input_{selected_company}",
        )

        questions = st.text_area(
            "Open Questions",
            value=(questions_record or {}).get("content", ""),
            height=120,
            key=f"questions_input_{selected_company}",
        )'''

new = '''        notes_left, notes_right = st.columns([1.25, 1])

        with notes_left:
            st.markdown(
                '<div class="veles-mini-panel-title">Company Research Note</div>',
                unsafe_allow_html=True,
            )

            note_text = st.text_area(
                "Company research note",
                value=(general_note_record or {}).get("content", ""),
                height=320,
                placeholder="Write thesis updates, risks, catalysts, diligence questions, funding notes, or technical observations here.",
                key=f"research_note_input_{selected_company}",
            )

            if st.button(
                "Save Research Note",
                key=f"save_research_note_{selected_company}",
            ):
                save_research_note(
                    user_id=user_id,
                    company_name=selected_company,
                    note_type="general",
                    content=note_text,
                )
                st.success(f"Research note saved for {selected_company}.")
                st.rerun()

        with notes_right:
            st.markdown(
                '<div class="veles-mini-panel-title">Research Structure</div>',
                unsafe_allow_html=True,
            )

            activity_item(
                "Notebook Scope",
                "Capture thesis updates, catalysts, risks, technical observations, funding notes, diligence questions, and report ideas.",
                "Analyst Notes"
            )

            activity_item(
                "Research Workflow",
                "Use structured fields below to separate investment thesis, catalysts, risks, and open questions.",
                "Workflow"
            )

        section_title(
            "Structured Thesis Workspace",
            "Institutional diligence fields for thesis, catalysts, risks, and open questions."
        )

        thesis_col, catalysts_col = st.columns(2)

        with thesis_col:
            thesis = st.text_area(
                "Thesis",
                value=(thesis_record or {}).get("content", ""),
                height=160,
                key=f"thesis_input_{selected_company}",
            )

        with catalysts_col:
            catalysts = st.text_area(
                "Catalysts",
                value=(catalysts_record or {}).get("content", ""),
                height=160,
                key=f"catalysts_input_{selected_company}",
            )

        risks_col, questions_col = st.columns(2)

        with risks_col:
            risks = st.text_area(
                "Risks",
                value=(risks_record or {}).get("content", ""),
                height=160,
                key=f"risks_input_{selected_company}",
            )

        with questions_col:
            questions = st.text_area(
                "Open Questions",
                value=(questions_record or {}).get("content", ""),
                height=160,
                key=f"questions_input_{selected_company}",
            )'''

if old not in text:
    raise SystemExit("Could not find notes text area block.")

text = text.replace(old, new, 1)

text = text.replace(
'''        if company_notes:
            notes_df = pd.DataFrame(company_notes)
            st.dataframe(notes_df, use_container_width=True)
        else:
            activity_item(
                "No Saved Notes Yet",
                "Use the fields above to start building a persistent company-specific research log.",
                "Notes"
            )''',
'''        section_title(
            "Saved Research Log",
            "Stored note records linked to this company."
        )

        if company_notes:
            notes_df = pd.DataFrame(company_notes)
            st.dataframe(notes_df, use_container_width=True)
        else:
            activity_item(
                "No Saved Notes Yet",
                "Use the fields above to start building a persistent company-specific research log.",
                "Notes"
            )''',
1
)

path.write_text(text)

print("Research Workspace notes tab redesigned.")
