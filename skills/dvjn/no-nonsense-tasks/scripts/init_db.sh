#!/usr/bin/env bash
# Initialize the task tracker database with migration support

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

DB_DIR=$(dirname "$DB_PATH")
MIGRATIONS_DIR="$SCRIPT_DIR/../migrations"

# Create directory if it doesn't exist
mkdir -p "$DB_DIR"

# Create migrations tracking table if it doesn't exist
sqlite3 "$DB_PATH" <<EOF
CREATE TABLE IF NOT EXISTS schema_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    migration_name TEXT NOT NULL UNIQUE,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
EOF

echo "Database location: $DB_PATH"
echo "Checking for migrations..."
echo ""

# Apply each migration in order
applied_count=0
skipped_count=0

for migration_file in "$MIGRATIONS_DIR"/*.sql; do
	if [ ! -f "$migration_file" ]; then
		continue
	fi

	migration_name=$(basename "$migration_file")

	# Escape single quotes for SQL
	migration_name_esc=$(sql_escape "$migration_name")

	# Check if migration has already been applied
	already_applied=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM schema_migrations WHERE migration_name = '$migration_name_esc';")

	if [ "$already_applied" -eq 1 ]; then
		echo "⊘ Skipped: $migration_name (already applied)"
		((skipped_count++))
	else
		echo "→ Applying: $migration_name"

		# Apply the migration
		if sqlite3 "$DB_PATH" <"$migration_file"; then
			# Record successful migration
			sqlite3 "$DB_PATH" "INSERT INTO schema_migrations (migration_name) VALUES ('$migration_name_esc');"
			echo "✓ Applied: $migration_name"
			((applied_count++))
		else
			echo "✗ Failed: $migration_name"
			exit 1
		fi
	fi
done

echo ""
echo "Migration summary:"
echo "  Applied: $applied_count"
echo "  Skipped: $skipped_count"
echo ""
echo "✓ Database ready at: $DB_PATH"
