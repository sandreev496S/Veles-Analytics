from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        st.dataframe(sens_df, use_container_width=True)

        st.subheader("Reverse DCF — Implied Growth")'''

new = '''        st.dataframe(sens_df, use_container_width=True)

        sens_heatmap = px.imshow(
            sens_df.astype(float),
            text_auto=".2f",
            aspect="auto",
            title="Sensitivity Heatmap — Implied Share Price",
        )

        sens_heatmap.update_layout(
            xaxis_title="Terminal Growth",
            yaxis_title="Discount Rate",
        )

        st.plotly_chart(sens_heatmap, use_container_width=True)

        section_title(
            "Reverse DCF — Implied Growth",
            "Estimate the revenue growth implied by the current market capitalization."
        )'''

if old not in text:
    raise SystemExit("Could not find sensitivity matrix block.")

text = text.replace(old, new, 1)

path.write_text(text)
print("UI patch 11 applied successfully: sensitivity heatmap added.")
