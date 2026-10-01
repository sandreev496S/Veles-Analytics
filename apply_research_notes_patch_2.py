from pathlib import Path

path = Path("app.py")
text = path.read_text()

start_marker = '''    with notes_tab:
        note_key = f"research_note_{selected_company}"'''

end_marker = '''    with reports_tab:'''

if start_marker not in text:
    raise SystemExit("Could not find Notes tab start block.")

if end_marker not in text:
    raise SystemExit("Could not find Reports tab marker.")

start = text.index(start_marker)
end = text.index(end_marker, start)

new_block = '''    with notes_tab:
        user_id = get_current_user()["id"]

        section_title(
            "Research Notes",
            f"Persistent analyst workspace for {selected_company}."
        )

        general_note_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="general",
        )

        thesis_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="thesis",
        )

        catalysts_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="catalysts",
        )

        risks_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="risks",
        )

        questions_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="questions",
        )

        note_text = st.text_area(
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
        )

        if st.button(
            "Draft Thesis From Company Profile",
            key=f"draft_thesis_{selected_company}",
        ):
            draft_thesis = (
                f"{selected_company} is positioned within the {selected_profile['focus']} segment of neurotechnology. "
                f"The company may be attractive if it can convert technical differentiation into clinical adoption, regulatory progress, and durable market leadership."
            )

            save_research_note(user_id, selected_company, "thesis", draft_thesis)
            save_research_note(
                user_id,
                selected_company,
                "catalysts",
                "Clinical progress; regulatory milestones; new funding rounds; strategic partnerships; published performance data.",
            )
            save_research_note(user_id, selected_company, "risks", selected_profile["risk"])
            save_research_note(
                user_id,
                selected_company,
                "questions",
                "What is the clearest regulatory pathway? What evidence supports commercial adoption? How differentiated is the technology versus direct competitors? What valuation is justified by current traction?",
            )

            st.success(f"Draft thesis created for {selected_company}.")
            st.rerun()

        if st.button(
            "Save Thesis Workspace",
            key=f"save_thesis_workspace_{selected_company}",
        ):
            save_research_note(user_id, selected_company, "thesis", thesis)
            save_research_note(user_id, selected_company, "catalysts", catalysts)
            save_research_note(user_id, selected_company, "risks", risks)
            save_research_note(user_id, selected_company, "questions", questions)

            st.success(f"Investment thesis workspace saved for {selected_company}.")
            st.rerun()

        company_notes = list_research_notes(
            user_id=user_id,
            company_name=selected_company,
        )

        if company_notes:
            notes_df = pd.DataFrame(company_notes)
            st.dataframe(notes_df, use_container_width=True)
        else:
            activity_item(
                "No Saved Notes Yet",
                "Use the fields above to start building a persistent company-specific research log.",
                "Notes"
            )

'''

text = text[:start] + new_block + text[end:]

path.write_text(text)

print("Research Workspace Notes tab now uses Supabase research_notes.")
