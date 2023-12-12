def resolve_uid(val):
    raise Unsupported("setuid() unsupported on this platform. Have your service manager setup user/group instead.")


def resolve_gid(val):
    raise Unsupported("setgid() unsupported on this platform. Have your service manager setup user/group instead.")


class Unsupported(RuntimeError):
    pass


def close_on_exec(fd):
    # Python 3.4+: file descriptors created by Python non-inheritable by default
    # FIXME: systemd-inherited fd
    pass


def pipe2():
    raise Unsupported(
        "non-blocking pipe() notsupported on this platform. "
        "The relevant section should be rewritten with Python stdlib selectors "
        "to automatically select a supported method."
    )


def set_owner_process(uid, gid, initgroups=False):
    """set user and group of workers processes"""

    if gid is not None:
        raise Unsupported("setgid() unsupported on this platform. Have your service manager setup user/group instead.")
    if uid is not None:
        raise Unsupported("setuid() unsupported on this platform. Have your service manager setup user/group instead.")


ALL = [
    "close_on_exec",
    "pipe2",
    "resolve_gid",
    "resolve_uid",
    "set_owner_process",
]
