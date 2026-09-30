def commit_diff(service: str, version: str) -> str:
    return ("commit 9f3c2ab (tag: v2.4.1)\n--- a/config/database.env\n+++ b/config/database.env\n"
            "-DATABASE_POOL_SIZE=20\n+DATABASE_POOL_SIZE=0\n")
