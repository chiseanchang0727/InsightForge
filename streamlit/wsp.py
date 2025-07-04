
import fitz
import streamlit as st
from submit_api import submit




st.set_page_config(page_title="PDF Annotator", layout="wide")

# ---- SESSION STATE ----
if "page" not in st.session_state:
    st.session_state.page = "upload"
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

# ---- LOGO ----
c1, c2, c3 = st.columns([1,4,1])
with c2:
    st.image("/Users/blakechang/Desktop/wsplogo.png", width=200)
st.markdown("---")

# # ---- DB INSERT ----
# def insert_into_db(pdf_name: str, page_num: int, description: str):
#

# ---- PAGE 1: UPLOAD ----
if st.session_state.page == "upload":
    st.header("Upload Files")
    uploaded = st.file_uploader("PDF File upload button", type=["pdf"])

    #TODO: upload the real file to destination which is the VM currently

    if uploaded:
        data = uploaded.read()
        st.session_state.pdf_bytes = data
        st.session_state.pdf_name = uploaded.name
        if st.button("Next →"):
            st.session_state.page = "view"
            st.rerun()

# ---- PAGE 2: VIEW & ANNOTATE ----

#TODO: condition check: edited or not, if edited show previous record
#TODO: scroll 
#TODO: when clicking show previous record, if the file_name and page is occupied show latest record
#TODO: when submit, insert a new row

else:
    st.header(f"Viewing: {st.session_state.pdf_name}")

    if st.button("Back to Main"):
            st.session_state.page = "upload"
            st.rerun()

    # open with fitz
    pdf_doc = fitz.open(stream=st.session_state.pdf_bytes, filetype="pdf")
    total = pdf_doc.page_count
    cp = st.session_state.current_page

    # navigation
    n1, n2, n3 = st.columns([1,2,1])
    with n1:
        if st.button("◀️ Previous") and cp > 1:
            st.session_state.current_page -= 1
            st.rerun()
    with n2:
        st.markdown(f"#### Page {cp} / {total}")
    with n3:
        if st.button("Next ▶️") and cp < total:
            st.session_state.current_page += 1
            st.rerun()

    # render the current page to an image
    page = pdf_doc.load_page(cp - 1)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2× zoom for readability
    img_data = pix.tobytes("png")

    # layout: viewer + description
    vc, dc,author = st.columns([3, 1,1])
    with vc:
        st.image(img_data, use_column_width=True)
    with dc:
        desc = st.text_area("Description for this page", height=500)
    with author:
        author_name = st.text_input("Author Name", placeholder="Enter author name:")
        if st.button("Submit"):
            submit(st.session_state.pdf_name, author_name, st.session_state.current_page, desc)
            # Here you would call your API to insert into the database
            # insert_into_db(st.session_state.pdf_name, cp, desc)
            st.success("✅ Saved!")

# ---- PAGE 3: HISTORY CHECK PAGE----
#TODO: A page for user to check the current completeness
#TODO: It shows: the uploaded files,  the completeness percentage


# ---- PAGE 4: Search Page ----