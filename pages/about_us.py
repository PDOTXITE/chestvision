import streamlit as st

# Set the page layout to wide
st.set_page_config(layout="wide")

def main():
    # CSS for basic styling and layout to allow full width
    st.markdown(
        """
        <style>
        .container {
            font-family: Arial, sans-serif;
            padding: 20px;
            margin: auto;
            width: 100%;
        }
        .title {
            font-size: 2em;
            margin-bottom: 10px;
            text-align: center;
        }
        .content {
            font-size: 1em;
            text-align: justify;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Content for the "About Us" page
    st.markdown(
        """
        <div class="container">
            <div class="title">About Us</div>
            <div class="content">
                This software is a work developed by Miss Phetdau Dueramae and Miss Nattakorn Pansiri from Princess Chulabhorn Science High School Satun under the provision of Miss Kesinee Kongseng under Multi Label Classification of 14 Common Thorax Disease Platform From Chest X-ray Images Using Transfer Learning Technique, which has been supported by the National Science and Technology Development Agency (NSTDA), in order to encourage pupils and students to learn and practice their skills in developing software. Therefore, the intellectual property of this software shall belong to the developer and the developer gives NSTDA a permission to distribute this software as “as is” and non-modified software for a temporary and non-exclusive use without remuneration to anyone for his or her own purpose or academic purpose, which are not commercial purposes. In this connection, NSTDA shall not be responsible to the user for taking care, maintaining, training, or developing the efficiency of this software. Moreover, NSTDA shall not be liable for any error, software efficiency and damages in connection with or arising out of the use of the software.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
