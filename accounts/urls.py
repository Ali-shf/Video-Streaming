from django.urls import path
from accounts import views

urlpatterns = [
    # Auth
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("refresh/", views.RefreshTokenView.as_view(), name="token_refresh"),
    path("logout/", views.LogoutUserView.as_view(), name="logout"),

    # User Self-Profile
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),
    path("profile/update/", views.UpdateUserProfileView.as_view(), name="update_profile"),

    # Admin Operations
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("user/detail/", views.UserDetailView.as_view(), name="user_detail"),
    path("user/update/", views.UpdateUserView.as_view(), name="admin_update_user"),
    path("user/delete/", views.DeleteUserView.as_view(), name="delete_user"),
    path("user/role/", views.ChangeUserRoleView.as_view(), name="change_user_role"),
]
