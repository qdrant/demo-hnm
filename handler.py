from typing import Dict, Text, List, Union

from PIL import Image

import conf
from img2vec_pytorch import Img2Vec
from qdrant_client import QdrantClient
from qdrant_client.http.models import FieldCondition, Filter, MatchValue, \
    RecommendRequest


class QdrantSearch:
    """
    A handler of all the search operations, allowing to look for similar items
    based on a provided file and selected search criteria.
    """

    def __init__(self):
        self.client = QdrantClient(host=conf.QDRANT_HOST, port=conf.QDRANT_PORT)
        self.img2vec = Img2Vec(
            cuda=False, model=conf.MODEL_NAME, layer_output_size=conf.VECTOR_SIZE
        )

    def find_similar(
        self,
        query: Union[int, Text],
        num_results: int = conf.NUM_RESULTS,
        filters: Dict[Text, List[Text]] = {},
    ):
        """
        Queries Qdrant server for the similar entries for a provided query.
        A query might be either an id of the point or anything that might be
        directly converted to PIL Image instance and then vectorized.
        :param query:
        :param num_results:
        :param filters:
        :return:
        """
        if isinstance(query, int):
            response = self.client.http.points_api.recommend_points(
                collection_name=conf.COLLECTION_NAME,
                recommend_request=RecommendRequest(
                    positive=[query],
                    negative=[],
                    filter=self._build_query_filters(filters),
                    with_payload=True,
                    top=num_results,
                )
            )

            return response.result

        img = Image.open(query).convert("RGB")
        state_vector = self.img2vec.get_vec(img, tensor=False)
        return self.client.search(
            collection_name=conf.COLLECTION_NAME,
            query_vector=state_vector.tolist(),
            query_filter=self._build_query_filters(filters),
            append_payload=True,
            top=num_results,
        )

    def _build_query_filters(self, filters: Dict[Text, List[Text]]) -> Filter:
        must_criteria = []
        for field_name, field_values in filters.items():
            if 0 == len(field_values):
                continue
            field_filter = Filter(
                should=[
                    FieldCondition(key=field_name, match=MatchValue(value=field_value))
                    for field_value in field_values
                ]
            )
            must_criteria.append(field_filter)

        return Filter(must=must_criteria)
