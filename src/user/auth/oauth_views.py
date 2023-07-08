from rest_framework import response, views


class AuthGitHubView(views.APIView):
    """Authentication with GitHub"""

    def get(self, request, *args, **kwargs):
        print(request)
        return response.Response({"Qweqe": "Weqewqe"})