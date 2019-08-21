# Configures environment for WiscAr lab

export PROJECT_DIR="$(git rev-parse --show-toplevel)"
export SPARROW_PATH="$PROJECT_DIR/Sparrow"
export SPARROW_CONFIG="$SPARROW_PATH/config/WiscAr.cfg"
export SPARROW_BACKUP_DIR="$PROJECT_DIR/backups"
export SPARROW_SECRET_KEY="GraniteAndesiteBasaltGabbro"
export SPARROW_LAB_NAME="WiscAr"

export SPARROW_SITE_CONTENT="$PROJECT_DIR/site-content"

pipeline="$PROJECT_DIR/import-pipeline"
export SPARROW_INIT_SQL="$pipeline/sql"
export SPARROW_COMMANDS="$pipeline/bin"

# Keep volumes for this project separate from those for different labs
export COMPOSE_PROJECT_NAME="WiscAr"

export SPARROW_DATA_DIR="$PROJECT_DIR/Data"
export MAPBOX_API_TOKEN="pk.eyJ1IjoiZGF2ZW5xdWlubiIsImEiOiJjanZ1eWwxMjAwNmRvM3lzNTNqN2d0OHdzIn0.kmDqABs8gHCaihj8UdnQKg"

