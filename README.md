<table style="border: none"><tbody style="border: none"><tr style="border: none">
<td style="border: none">

## Gunicorn

This is an unmaintained fork for **testing & integration**.

* See gunicorn [Upstream Repository](https://github.com/benoitc/gunicorn), [PyPI]( https://pypi.python.org/pypi/gunicorn) and [Docs](https://docs.gunicorn.org)

### License

Gunicorn is released under the MIT License. See the [LICENSE](LICENSE) file for more
details.

### CI

[![CI:buildpackage](https://github.com/pajod/gunicorn/actions/workflows/buildpackage.yml/badge.svg)](https://github.com/pajod/gunicorn/actions/workflows/buildpackage.yml)
[![CI:CodeQL](https://github.com/pajod/gunicorn/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/pajod/gunicorn/actions/workflows/github-code-scanning/codeql)
[![CI:lint](https://github.com/pajod/gunicorn/actions/workflows/lint.yml/badge.svg)](https://github.com/pajod/gunicorn/actions/workflows/lint.yml)
[![CI:tox](https://github.com/pajod/gunicorn/actions/workflows/tox.yml/badge.svg)](https://github.com/pajod/gunicorn/actions/workflows/tox.yml)

</td>
<td style="border: none">

### Notable changes tested in this repository

 * request smuggling vulnerabilities: [PR #3059](https://github.com/benoitc/gunicorn/pull/3059) [PR #3113](https://github.com/benoitc/gunicorn/pull/3113)
 * configuration mismatch for SCRIPT_NAME: [PR #2804](https://github.com/benoitc/gunicorn/pull/2804)
 * [Building a debian/ubuntu](.github/workflows/ubuntu.yml) package without pulling updated dependencies
   * Ubuntu 22.04 may be willing to stick to setuptools 59 until **April 2032**

</tbody>
</tr></tbody></table>
