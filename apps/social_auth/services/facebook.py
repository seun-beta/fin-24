import facebook_business


class Facebook:
    """
    Facebook class to fetch the user info and return it
    """

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the facebook GraphAPI to fetch the user info
        """
        try:
            graph = facebook_business.GraphAPI(access_token=auth_token)
            profile = graph.request("/me?fields=name,email")
            return profile
        except Exception:
            return "The token is invalid or expired."
