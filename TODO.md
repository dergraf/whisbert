TODO:
=====
- Wildcard queries MUST address whisper files that can serve the requested time range. This should be fixed, since this is in real-world not really the case
- Test how Whisper performs with concurrent writers. fcntl.flock() is only applied on supporting systems, however with concurrent writers the lock is necessary.
- Benchmarks

