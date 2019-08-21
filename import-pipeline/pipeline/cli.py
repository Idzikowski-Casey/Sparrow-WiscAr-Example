from os import environ, listdir, path
from click import command, option, echo, secho, style
from pathlib import Path
from sparrow import Database
from .importer import MAPImporter

@command(name="import-map")
@option('--redo','-r', is_flag=True, default=False)
@option('--stop-on-error', is_flag=True, default=False)
@option('--verbose','-v', is_flag=True, default=False)
def cli(redo=False, stop_on_error=False, verbose=False):
    """
    Import WiscAr MAP spectrometer data (ArArCalc files) in bulk.
    """
    varname = "SPARROW_DATA_DIR"
    env = environ.get(varname, None)
    if env is None:
        v = style(varname, fg='cyan', bold=True)
        echo(f"Environment variable {v} is not set.")
        secho("Aborting", fg='red', bold=True)
        return
    path = Path(env)
    assert path.is_dir()

    db = Database()
    importer = MAPImporter(db)
    importer.iterfiles(path.glob("**/*.xls"), redo=redo)
