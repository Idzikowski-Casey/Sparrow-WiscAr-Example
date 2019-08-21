from sys import exit
from os import environ, listdir, path
from datetime import datetime
from click import command, option, echo, secho, style
from pathlib import Path
from sparrow.database import get_or_create
from sparrow.import_helpers import BaseImporter

from .extract_tables import extract_data_tables
from .insert_data import extract_analysis

class MAPImporter(BaseImporter):
    authority = "WiscAr"
    def __init__(self, db, **kwargs):
        super().__init__(db)
        self.verbose = kwargs.pop("verbose", False)

    def import_datafile(self, fn, rec, **kwargs):
        """
        Import an original data file
        """
        return
        #extract_analysis(self.db, fn, verbose=self.verbose)

