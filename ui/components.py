import streamlit as st


def page_title():

    st.markdown(
        """
        <h1 style='text-align:center;color:#4F8BF9;'>
        📄 HireSense AI
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center;'>AI Resume Analyzer & ATS Optimizer</h4>",
        unsafe_allow_html=True
    )

    st.divider()


def metric_cards(ats, similarity, skill, overall):

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric("📄 ATS", f"{ats}%")

        st.progress(int(ats))

    with c2:

        st.metric("🎯 Match", f"{similarity}%")

        st.progress(int(similarity))

    with c3:

        st.metric("💡 Skills", f"{skill}%")

        st.progress(int(skill))

    with c4:

        st.metric("⭐ Overall", f"{overall}%")

        st.progress(int(overall))


def section(title):

    st.divider()

    st.subheader(title)