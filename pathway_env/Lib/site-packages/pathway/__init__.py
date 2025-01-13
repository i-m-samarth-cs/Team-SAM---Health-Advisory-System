from . import _stub_finder  # noqa:F401


def _legacy_warning(name: str) -> str:
    import textwrap

    legacy_version = "1.3.1"

    return textwrap.dedent(
        f"""
            This is probably not the Pathway you are looking for.
            {name!r} is defined by the legacy Pathway package.
            You can install it explicitly requesting version {legacy_version},
            e.g. `pip install "pathway=={legacy_version}"`.
        """
    ).strip("\n")


def _warning() -> str:
    import textwrap
    from platform import platform, python_implementation, python_version

    url = "https://pathway.com/developers/"
    troubleshooting_url = "https://pathway.com/troubleshooting/"

    plat = platform(aliased=True)
    py_version = f"{python_implementation()} {python_version()}"

    return textwrap.dedent(
        f"""
            This is not the real Pathway package.
            Visit {url} to get Pathway.
            Already tried that? Visit {troubleshooting_url} to get help.
            Note: your platform is {plat}, your Python is {py_version}.
        """
    ).strip("\n")


def _warn(warning: str):
    import sys

    sys.stderr.write(warning + "\n")


def __getattr__(name):
    legacy_names = (
        "ALL",
        "FILES",
        "FOLDERS",
        "File",
        "Folder",
        "PathError",
        "PathObject",
        "SomethingElse",
        "new",
    )
    error = f"module {__name__!r} has no attribute {name!r}"
    warning = _legacy_warning(name) if name in legacy_names else _warning()
    _warn(warning)
    error = error + "\n" + warning
    raise AttributeError(error)


_warn(_warning())
