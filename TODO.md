# Magisk Hub — Remaining Tasks & Roadmap

Last Updated: October 4, 2026

## 1. High Priority
- [ ] **Orphaned Guide Resolution**:
  - `content/modules/aclipboardmanager.md` exists without a matching `modules/aclipboardmanager.json`.
  - Add module metadata or prune guide.
- [ ] **URL Filter State Synchronization**:
  - Sync platform, category, and search queries with URL parameters (`?platform=...&category=...`) for shareable filtered links.
- [ ] **Batch Audit Remaining Guides (~190 modules)**:
  - Extend the zero-emoji, zero-ASCII-diagram, verified technical spec audit across the remaining 190 guides.

## 2. Platform & Tooling
- [ ] **Download Link Health Check**: Automated testing script for GitHub release asset URLs.
- [ ] **CI Release Sync Verification**: Test GitHub Actions `sync-releases.yml` cron workflow.
- [ ] **Extreme Viewport Testing (320px)**: Validate on ultra-compact mobile screens.
