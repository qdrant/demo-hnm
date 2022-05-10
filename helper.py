import itertools
import math
from typing import Union, Text

import streamlit as st
from PIL import Image

import conf


def create_image_path(article_id: int):
    article_id_str = str(article_id).rjust(10, "0")
    return f"{conf.IMAGES_DIR}/{article_id_str[0:3]}/{article_id_str}.jpg"


def set_query(query: Union[int, Text]):
    st.session_state["query"] = query


def get_query_image():
    query = st.session_state["query"]
    if isinstance(query, int):
        image_path = create_image_path(query)
        img = Image.open(image_path)
        return img

    return query


def create_columns_grid(num_columns: int):
    return itertools.chain(
        *[
            st.columns(conf.NUM_RESULTS_PER_ROW)
            for _ in range(math.ceil(num_columns / conf.NUM_RESULTS_PER_ROW))
        ]
    )
