# Contributing

## Development Setup

1. Fork and clone the repository
2. Follow the setup steps in the [README](README.md)
3. Start a local database: `python scripts/db_util/run_dev_db.py`
4. Seed sample data: `python scripts/db_util/seed_data.py`

## Branch Naming

- `feature/description` — new features
- `fix/description` — bug fixes
- `docs/description` — documentation
- `refactor/description` — refactoring

## Commit Messages

Follow conventional commits:

```
type(scope): description
```

Examples:
- `feat(auth): add token expiry validation`
- `fix(licenses): handle null expiry date`
- `docs(readme): update setup instructions`

## Code Style

- Python: format with `black`, sort imports with `isort`
- TypeScript: follow existing patterns, no `any` unless necessary

## Pull Requests

1. Branch from `master`
2. Add tests for new functionality
3. Ensure existing tests pass
4. Submit a PR with a clear description of what changed and why

## Reporting Issues

Include:
- Steps to reproduce
- Expected vs actual behavior
- Python/Node version and OS
- Relevant logs or error messages
