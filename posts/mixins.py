from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly


class StaffEditOnly:
    permission_classes = [IsAdminUser]

class UserEditOnly:
    permission_classes = [IsAuthenticatedOrReadOnly]