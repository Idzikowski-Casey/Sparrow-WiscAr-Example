# Configures environment for WiscAr lab

export PROJECT_DIR="$(git rev-parse --show-toplevel)"
export SPARROW_PATH="$PROJECT_DIR/Sparrow"
export SPARROW_CONFIG="$SPARROW_PATH/config/WiscAr.cfg"
export SPARROW_BACKUP_DIR="$PROJECT_DIR/backups"
export SPARROW_LAB_NAME="WiscAr"

export SPARROW_SITE_CONTENT="$PROJECT_DIR/site-content"

pipeline="$PROJECT_DIR/import-pipeline"
export SPARROW_INIT_SQL="$pipeline/sql"
export SPARROW_COMMANDS="$pipeline/bin"

# Keep volumes for this project separate from those for different labs
export COMPOSE_PROJECT_NAME="WiscAr"

export SPARROW_DATA_DIR="$PROJECT_DIR/Data"
export SPARROW_DB_PORT="54351"
export SPARROW_HTTP_PORT="50101"
export SPARROW_COMPOSE_OVERRIDES="-f $PROJECT_DIR/docker-compose.overrides.yaml"

overrides="${0:h}/sparrow-config.overrides.sh"
[ -f "$overrides" ] && source "$overrides"
