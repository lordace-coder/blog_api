from rest_framework.permissions import IsAdminUser


class StaffEditOnly:
    permission_classes = [IsAdminUser]
    