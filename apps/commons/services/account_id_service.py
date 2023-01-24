from django.conf import settings

import httpx


async def get_account_id(auth_token: str) -> dict:

    base_url = settings.MONO_BASE_URL
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "mono-sec-key": settings.MONO_API_KEY,
    }
    url = f"{base_url}/account/auth"
    data = {"code": auth_token}

    response = await httpx.post(url=url, headers=headers, data=data)

    return response


# curl --request POST \
#      --url https://api.withmono.com/account/auth \
#      --header 'Accept: application/json' \
#      --header 'Content-Type: application/json' \
#      --header 'mono-sec-key: test_sk_adasdsadasddasd' \
#      --data '
# {
#      "code": "code_hgvh46dejqtjvkjk"
# }
