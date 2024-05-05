<table style="border: none"><tbody style="border: none"><tr style="border: none">
<td style="border: none">

## Gunicorn

This is an unmaintained fork for **testing & integration**.

* See gunicorn [Upstream Repository](https://github.com/benoitc/gunicorn), [PyPI]( https://pypi.python.org/pypi/gunicorn) and [Docs](https://docs.gunicorn.org)

### License

Gunicorn is released under the MIT License. See the [LICENSE](LICENSE) file for more
details.

### CI

[![CI:packaging](https://github.com/pajod/gunicorn/actions/workflows/packaging.yml/badge.svg)](https://github.com/pajod/gunicorn/actions/workflows/packaging.yml)
[![CI:CodeQL](https://github.com/pajod/gunicorn/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/pajod/gunicorn/actions/workflows/github-code-scanning/codeql)
[![CI:lint](https://github.com/pajod/gunicorn/actions/workflows/lint.yml/badge.svg)](https://github.com/pajod/gunicorn/actions/workflows/lint.yml)
[![CI:tox](https://github.com/pajod/gunicorn/actions/workflows/tox.yml/badge.svg)](https://github.com/pajod/gunicorn/actions/workflows/tox.yml)

</td>
<td style="border: none">

### Notable changes tested in this repository

 * no ASGI support
 * no HTTP2 support
 * no dirty worker
 * no ctl interface
 * no daemonize hack
 * no requirement on mkdocs-material to build docs
 * no `--casefold-http-method` / `--strip-header-spaces` / `--permit-obsolete-folding`
 * reduced test & docs dependencies
 * no implicit --config=$PWD/gunicorn.conf.py execution
 * added type stubs
 * regression test for basic nginx setup
 * less permissive HTTP parser validation
 * no paste deploy support
 * permit `--reload-extra-files` without `--reload`
 * new `--on-fatal=`

</tbody>
</tr></tbody></table>

### Status Images

![gunicorn upstream Stats by Repobeats](https://repobeats.axiom.co/api/embed/c1f1846401d9b4913dd9019aead4b1883e954739.svg "Repobeats analytics image")
