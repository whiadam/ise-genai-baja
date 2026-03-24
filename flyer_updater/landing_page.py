import streamlit as st  

def render_landing_page():
    st.title("Flyer Updater")

    uploaded_file = st.file_uploader(
        "Upload a flyer image",
        type=["png", "jpg", "jpeg", "pdf"],
        accept_multiple_files=False,
    )

    camera_image = st.camera_input("Or take a photo")

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Flyer", use_container_width=True)
    elif camera_image:
        st.image(camera_image, caption="Captured Photo", use_container_width=True)

    if st.button("Submit"):
        if uploaded_file or camera_image:
            st.success("Flyer submitted successfully!")
        else:
            st.warning("Please upload or capture an image first.")
