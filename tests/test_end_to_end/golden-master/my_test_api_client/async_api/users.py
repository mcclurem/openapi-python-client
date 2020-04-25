from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError
from ..models.a_model import AModel
from ..models.http_validation_error import HTTPValidationError
from ..models.statuses import Statuses


async def get_user_list(
    *, client: Client, statuses: List[Statuses],
) -> Union[
    List[AModel], HTTPValidationError,
]:
    """ Get users, filtered by statuses  """
    url = "{}/tests/".format(client.base_url)

    params = {
        "statuses": statuses,
    }

    async with httpx.AsyncClient() as _client:
        response = await _client.get(url=url, headers=client.get_headers(), params=params,)

    if response.status_code == 200:
        return [AModel.from_dict(item) for item in cast(List[Dict[str, Any]], response.json())]
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
