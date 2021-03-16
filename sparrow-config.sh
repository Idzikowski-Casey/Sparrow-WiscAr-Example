# Configures environment for WiscAr lab

export PROJECT_DIR="$SPARROW_CONFIG_DIR"
export SPARROW_PATH="$PROJECT_DIR/Sparrow"
#export SPARROW_CONFIG="$SPARROW_PATH/config/WiscAr.cfg"
export SPARROW_BACKUP_DIR="$PROJECT_DIR/backups"
export SPARROW_LAB_NAME="WiscAr"

export SPARROW_SITE_CONTENT="$PROJECT_DIR/site-content"

pipeline="$PROJECT_DIR/import-pipeline"
export SPARROW_INIT_SQL="$pipeline/sql"
export SPARROW_COMMANDS="$pipeline/bin"
export SPARROW_PLUGIN_DIR="$PROJECT_DIR/site-content/backend-plugins"
export SPARROW_ENV="development"
# Keep volumes for this project separate from those for different labs
export COMPOSE_PROJECT_NAME="WiscAr"

export SPARROW_DATA_DIR="$PROJECT_DIR/Data"

overrides="$SPARROW_CONFIG_DIR/sparrow-config.overrides.sh"
[ -f "$overrides" ] && source "$overrides"

