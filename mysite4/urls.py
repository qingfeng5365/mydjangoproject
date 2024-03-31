"""mysite4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,re_path
from django.views.static import serve
from django.conf import settings

from app01.views import depart,user,task,admin,account,test,file,image,avatar

urlpatterns = [

    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT},name='media'),
    
    # path('admin/', admin.site.urls),
    
    #首页
    path('',account.login),
    path('avatar/get/',avatar.avatar_get),

    #部门管理
    path('depart/list/',depart.depart_list),
    path('depart/add/',depart.depart_add),
    path('depart/delete/',depart.depart_delete),
    path('depart/<int:nid>/edit/',depart.depart_edit),
    path('depart/jump/',depart.depart_jump),
    path('depart/batchAdd/',depart.depart_batchAdd),
    path('depart/batchDelete/',depart.depart_batchDelete),

    #用户管理
    path('user/list/',user.user_list),
    path('user/add/',user.user_add),
    path('user/<int:nid>/edit/',user.user_edit),
    path('user/<int:nid>/delete/',user.user_delete),
    path('user/jump/',user.user_jump),

    #任务管理
    path('task/list/',task.task_list),
    path('task/add/',task.task_add),
    path('task/info/',task.task_info),
    path('task/edit/',task.task_edit),
    path('task/delete/',task.task_delete),
    path('task/jump/',task.task_jump),

    #文件管理
    path('file/list/',file.file_list),
    path('file/jump/',file.file_jump),
    path('file/add/',file.file_add),
    path('file/<int:nid>/edit/',file.file_edit),
    path('file/delete/',file.file_delete),

    #图片管理
    path('image/list/',image.image_list),
    path('image/jump/',image.image_jump),
    path('image/delete/',image.image_delete),
    path('image/add/',image.image_add),
    path('image/info/',image.image_info),
    path('image/edit/',image.image_edit),

    #管理员
    path('admin/list/',admin.admin_list),
    path('admin/add/',admin.admin_add),
    path('admin/<int:nid>/edit/',admin.admin_edit),
    path('admin/<int:nid>/delete/',admin.admin_delete),
    path('admin/<int:nid>/reset/',admin.admin_reset),
    path('admin/jump/',admin.admin_jump),

    #登录
    path('login/',account.login),
    path('image/code/',account.image_code),
    path('logout/',account.logout),

    #测试
    path('test/list/',test.test_list),
    path('test/ajax/',test.test_ajax),

]


