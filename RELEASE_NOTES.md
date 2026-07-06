# Release Notes - Version 23

## Production Release

This is the first production-ready release of StartXNow Career Watch.

### Improvements

- Removed dead code: unused `Provider` model, `get_db()` function, `get_job()` function, `delete_all_jobs()` function, unused imports (`config`, `Session`, `time`, `Callable`, `base_format`)
- Cleaned `config.json`: removed unused `email.enabled` field
- Updated `Procfile` for correct deployment path
- Added `pytz` to `requirements.txt`
- All 32 unit tests pass
- All endpoints verified (Health, Jobs, Today, Report, Email Test, Send Today)

### Features

- 50+ company career page providers with automatic discovery
- Intelligent job filtering (accept/reject roles, location, experience, date)
- Professional HTML email reports with responsive design
- APScheduler running daily at 7:00 PM IST
- Retry logic with graceful failure per provider
- Automatic log rotation (1MB, 5 backups)
- URL hash-based duplicate detection
- Provider execution history and scan history stored in database

### Deployment

Ready for Railway and Render deployment. See README.md for instructions.

### Known Limitations

- Some provider APIs may return empty results or mock data if their public APIs change
- SQLite database is used (suitable for single-instance deployments)
- Email delivery depends on SMTP provider configuration