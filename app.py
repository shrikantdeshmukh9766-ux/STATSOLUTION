# ── Top summary metrics ──
            total_master    = len(master)
            total_filled    = len(filled)
            total_remaining = len(remaining)
            pct_done        = round(total_filled / total_master * 100, 1) if total_master else 0

            st.markdown(f"""
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:18px;">
                <div style="background:#dff5ec; border-radius:14px; padding:16px 20px; border:1px solid #c2ead8;">
                    <div style="font-size:11px; font-weight:700; color:#1a8a5a; text-transform:uppercase; letter-spacing:.6px;">एकूण मास्टर</div>
                    <div style="font-size:28px; font-weight:800; color:#1a8a5a;">{total_master}</div>
                </div>
                <div style="background:#dbeeff; border-radius:14px; padding:16px 20px; border:1px solid #c2dcf7;">
                    <div style="font-size:11px; font-weight:700; color:#1a6fa6; text-transform:uppercase; letter-spacing:.6px;">भरलेले</div>
                    <div style="font-size:28px; font-weight:800; color:#1a6fa6;">{total_filled}</div>
                </div>
                <div style="background:#fef3dc; border-radius:14px; padding:16px 20px; border:1px solid #fde5b4;">
                    <div style="font-size:11px; font-weight:700; color:#b5770a; text-transform:uppercase; letter-spacing:.6px;">उर्वरित</div>
                    <div style="font-size:28px; font-weight:800; color:#b5770a;">{total_remaining}</div>
                </div>
            </div>
            <div style="margin-bottom:18px;">
                <div style="font-size:12px; color:#4a6070; font-weight:600; margin-bottom:4px;">एकूण प्रगती &nbsp;·&nbsp; {pct_done}% पूर्ण</div>
                <div class="progress-wrap">
                    <div class="progress-bar" style="width:{pct_done}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Summary table per ASHA ──
            styled4 = (
                summary.style
                .background_gradient(cmap=light_teal_cmap(),     subset=['भरलेले'])
                .background_gradient(cmap=light_red_cmap(),      subset=['उर्वरित'])
                .background_gradient(cmap=light_lavender_cmap(), subset=['% पूर्ण'])
                .format({'एकूण_सहभागी': '{:.0f}', 'भरलेले': '{:.0f}', 'उर्वरित': '{:.0f}', '% पूर्ण': '{:.1f}%'})
                .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '13px', 'color': '#1b4f72'})
                .set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'), ('font-weight', '700'), ('font-size', '13px'), ('border', '1px solid #b8d9f0')]},
                    {'selector': 'td', 'props': [('border', '1px solid #eaf4fb')]},
                ])
            )
            st.dataframe(styled4, use_container_width=True, height=min(420, (len(summary) + 1) * 38 + 10))

            # ── Detailed remaining list with ASHA filter ──
            st.markdown("---")
            st.markdown("**📋 उर्वरित सहभागींची तपशीलवार यादी**")

            col1, col2 = st.columns([2, 4])
            with col1:
                asha_filter = st.selectbox(
                    "👩‍⚕️ आशा निवडा",
                    ["सर्व"] + sorted(remaining['asha'].unique().tolist()),
                    help="विशिष्ट आशाची उर्वरित यादी पाहा"
                )

            filtered_remaining = remaining if asha_filter == "सर्व" else remaining[remaining['asha'] == asha_filter]
            filtered_remaining = filtered_remaining.rename(columns={'asha': '👩‍⚕️ आशा', 'Paticipant': '👤 उर्वरित सहभागी'})

            st.dataframe(filtered_remaining, use_container_width=True, height=min(420, (len(filtered_remaining) + 1) * 38 + 10))

            # ── Download buttons ──
            st.markdown("---")
            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                st.download_button(
                    label="⬇️ उर्वरित यादी CSV डाउनलोड करा",
                    data=to_csv_bytes(filtered_remaining),
                    file_name="remaining_participants.csv",
                    mime="text/csv"
                )
            with dl_col2:
                excel_data = to_excel_bytes({
                    "उर्वरित सहभागी": filtered_remaining,
                    "आशा सारांश": summary
                })
                st.download_button(
                    label="⬇️ Excel डाउनलोड करा",
                    data=excel_data,
                    file_name="remaining_participants.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"⚠️ फाइल वाचताना त्रुटी आली: {e}")

st.markdown("</div>", unsafe_allow_html=True)
