import streamlit as st
from PIL import Image
import io
import zipfile

def overlay_images(base_image, overlay_image, position=(0, 0), scale=1.0):
    overlay_image = overlay_image.resize((int(overlay_image.width * scale), int(overlay_image.height * scale)))
    base_image.paste(overlay_image, position, overlay_image)
    return base_image

st.title("Bulk Image Overlay App")

uploaded_files = st.file_uploader("Choose base images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
overlay_file = st.file_uploader("Choose an overlay image", type=["png", "jpg", "jpeg"])

col1, col2, col3 = st.columns(3)
with col1:
    corner = st.selectbox("Choose corner for overlay", ["Top-left", "Top-right", "Bottom-left", "Bottom-right"])
with col2:
    scale = st.slider("Scale overlay image", 0.1, 2.0, 1.0)
with col3:
    padding = st.number_input("Padding around overlay image", min_value=0, value=0)

bcol1, bcol2 = st.columns(2)

if uploaded_files and overlay_file:
    overlay_image = Image.open(overlay_file).convert("RGBA")
    result_images = []
    for ind, uploaded_file in enumerate(uploaded_files):
        base_image = Image.open(uploaded_file).convert("RGBA")

        if corner == "Top-left":
            position = (padding, padding)
        elif corner == "Top-right":
            position = (base_image.width - int(overlay_image.width * scale) - padding, padding)
        elif corner == "Bottom-left":
            position = (padding, base_image.height - int(overlay_image.height * scale) - padding)
        elif corner == "Bottom-right":
            position = (base_image.width - int(overlay_image.width * scale) - padding, base_image.height - int(overlay_image.height * scale) - padding)

        result_image = overlay_images(base_image, overlay_image, position, scale)
        result_images.append((result_image, uploaded_file.name))
        if ind%2 == 0:
            with bcol1:
                st.image(base_image)
        else:
            with bcol2:
                st.image(base_image)

    if st.button("Download all as zip"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
            for img, name in result_images:
                img_buffer = io.BytesIO()
                img.save(img_buffer, format="PNG")
                name = name.split(".")[0] + "_overlayed.png"
                zip_file.writestr(name, img_buffer.getvalue())
        zip_buffer.seek(0)
        st.download_button("Download ZIP", zip_buffer, "overlayed_images.zip")