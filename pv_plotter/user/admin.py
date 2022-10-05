from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'email',
        'is_staff',
        'is_active',
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    ('first_name', 'last_name',),
                    ('legal_id_type', 'legal_id',),
                    'username',
                    'address',
                    ('email', 'phone_number',),
                    'photo',
                    'created_at',
                )
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_active'
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'fields': (
                    ('first_name', 'last_name',),
                    ('legal_id_type', 'legal_id',),
                    'address',
                    # 'city',
                    ('email', 'phone_number',),
                    'photo',
                    'created_at',
                )
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_active'
                )
            }
        ),
    )

    readonly_fields = (
        'created_at',
    )

    search_fields = ('email',)

    ordering = ('email',)
