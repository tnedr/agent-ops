# PyPI API Token Storage

**Date:** 2025-11-06  
**Status:** ✅ Secure

## Location

The PyPI API token is stored in **GitHub Secrets**, not in the repository.

## Access

1. GitHub repository: `Settings` > `Secrets and variables` > `Actions`
2. Secret name: `PYPI_API_TOKEN`

## Usage in Workflow

The token is referenced in `.github/workflows/release.yml`:

```yaml
env:
  TWINE_USERNAME: __token__
  TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

## Security

- ✅ Token is **not** in git history
- ✅ Only accessible to GitHub Actions workflows
- ✅ Not visible in repository files

## Creating/Updating Token

1. PyPI: `Account settings` > `API tokens` > `Add API token`
2. GitHub: `Settings` > `Secrets and variables` > `Actions` > `New repository secret`
3. Name: `PYPI_API_TOKEN`
4. Value: PyPI API token (e.g., `pypi-...`)

