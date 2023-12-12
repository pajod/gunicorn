import fcntl
import grp
import os
import pwd


def resolve_uid(val):
    return pwd.getpwnam(val).pw_uid


def resolve_gid(val):
    return grp.getgrnam(val).gr_gid


def assert_cloexec(fd):
    # Python 3.4+: file descriptors created by Python non-inheritable by default
    fd_flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    # mind the difference between os.O_CLOEXEC and fcntl.FD_CLOEXEC
    if not fd_flags | fcntl.FD_CLOEXEC:
        raise AssertionError("Expected FD_CLOEXEC set on fd %r" % fd)


def assert_nonblock(fd):
    # mind the difference between F_GETFD and F_GETFL
    fl_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    if not fl_flags | os.O_NONBLOCK:
        raise AssertionError("Expected O_NONBLOCK set on fd %r" % fd)


if hasattr(os, "pipe2"):
    # atomic
    def pipe2():
        read_write = os.pipe2(os.O_NONBLOCK | os.O_CLOEXEC)
        for fd in read_write:
            assert_cloexec(fd)
            assert_nonblock(fd)
        return read_write

    close_on_exec = assert_cloexec
else:

    def close_on_exec(fd):
        flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        flags |= fcntl.FD_CLOEXEC
        fcntl.fcntl(fd, fcntl.F_SETFD, flags)

    def set_non_blocking(fd):
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        flags |= os.O_NONBLOCK
        fcntl.fcntl(fd, fcntl.F_SETFL, flags)

    def pipe2():
        # race condition
        read_write = os.pipe()
        for fd in read_write:
            set_non_blocking(fd)
            close_on_exec(fd)
        return read_write


def get_username(uid):
    """get the username for a user id"""
    return pwd.getpwuid(uid).pw_name


def set_owner_process(uid, gid, initgroups=False):
    """set user and group of workers processes"""

    # FIXME: odd inconsistency with 0/None
    if gid:
        if uid:
            try:
                username = get_username(uid)
            except KeyError:
                initgroups = False

        # versions of python < 2.6.2 don't manage unsigned int for
        # groups like on osx or fedora
        if gid < 0 or gid != abs(gid) & 0x7FFFFFFF:
            raise AssertionError("Unusual gid %r supplied. Refusing 32-bit shenanigans" % (gid))

        if initgroups:
            os.initgroups(username, gid)
        elif gid != os.getgid():
            os.setgid(gid)

    if uid and uid != os.getuid():
        os.setuid(uid)


ALL = [
    "close_on_exec",
    "pipe2",
    "resolve_gid",
    "resolve_uid",
    "set_owner_process",
]
