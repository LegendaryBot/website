from django.core.cache import cache


def is_server_admin(func):
    def decorator(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        servers = cache.get(f"discord_admin_cache:{request.user.id}")
        for server in servers:
            if server['id'] == int(kwargs.get("guild_id")):
                return func(request, *args, **kwargs)
        return False
    return decorator