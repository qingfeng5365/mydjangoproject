from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        #if request.path_info=="/login/":
        # if request.path_info in ["/login/","/image/code/"]:
        #     return
        user_info = request.session.get("user_info")
        if user_info:
            return
        if request.path_info in ["/login/","/image/code/"]:
            return
        return redirect("/login/")
