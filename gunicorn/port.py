import sys

if sys.platform.startswith("win"):
    from gunicorn.windows import close_on_exec, pipe2, resolve_gid, resolve_uid, set_owner_process
else:
    from gunicorn.unix import close_on_exec, pipe2, resolve_gid, resolve_uid, set_owner_process

__ALL__ = [
    close_on_exec,
    pipe2,
    resolve_gid,
    resolve_uid,
    set_owner_process,
]
