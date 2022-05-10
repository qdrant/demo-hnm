import functools
import json
import glob

from PIL import Image

import conf
import streamlit as st

from handler import QdrantSearch
from helper import create_image_path, set_query, create_columns_grid, \
    get_query_image

qdrant_search = QdrantSearch()

st.set_page_config(
    page_title="Ecommerce visual search",
    menu_items={
        "Get help": "https://discord.gg/tdtYvXjC4h",
        "Report a bug": "https://github.com/qdrant/qdrant",
        "About": "https://qdrant.tech",
    },
)
st.button("Clear", on_click=st.session_state.clear)
st.title("Find similar clothes!")
st.caption(
    "This search engine has been trained using H&M data, provided in "
    "H&M Personalized Fashion Recommendations Kaggle competition: "
    "https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/\n\n"
    "The following tools have been used to create this demo: \n"
    "- ResNet18 for embeddings\n"
    "- Qdrant as a vector database (https://qdrant.tech/)\n"
    "- Streamlit as a frontend layer"
)

# Main view with the possibility to upload file / take photo
if "query" not in st.session_state:
    main_container = st.container()
    with main_container:
        # Image upload handling
        st.subheader("Send a photo")
        uploaded_file = main_container.file_uploader(
            "upload a file", type=["jpg", "png"], accept_multiple_files=False
        )
        if uploaded_file:
            set_query(uploaded_file)
            st.experimental_rerun()

        # Prepared examples
        st.subheader("Or select one of the examples")
        example_paths = glob.glob(f"{conf.EXAMPLES_DIR}/*.jpg")
        example_columns = create_columns_grid(len(example_paths))
        for file_path, col in zip(example_paths, example_columns):
            img = Image.open(file_path)
            col.image(img, use_column_width=True)
            col.button(
                "Select",
                key=file_path,
                on_click=functools.partial(set_query, query=file_path),
            )
else:
    # File has been provided so the search might be performed
    selected_filters = {}
    with st.sidebar, open("filters.json", "r") as fp:
        st.empty()

        available_filters = json.load(fp)
        for filter_config in available_filters:
            filter_key = filter_config["name"]
            selected_filters[filter_key] = st.multiselect(
                label=filter_config["display_name"],
                options=filter_config["values"],
            )

    with st.container():
        st.subheader("Looking for")

        left_col, right_col = st.columns([1, 3])
        left_col.image(get_query_image(), width=100)
        for field_name, field_values in selected_filters.items():
            if 0 == len(field_values):
                continue
            right_col.caption(", ".join(field_values))

        st.subheader("Suggested items")
        hits = qdrant_search.find_similar(
            st.session_state["query"], filters=selected_filters
        )

        if 0 == len(hits):
            st.warning("We couldn't find any item matching selected criteria")

        columns = create_columns_grid(len(hits))
        for hit_point, col in zip(hits, columns):
            image_path = create_image_path(hit_point.id)
            img = Image.open(image_path)

            col.caption(hit_point.payload["prod_name"])
            col.image(img)
            col.progress(hit_point.score)
            col.text(f"Score: {hit_point.score}")
            col.button(
                "Select",
                key=hit_point.id,
                on_click=functools.partial(set_query, query=hit_point.id),
            )
