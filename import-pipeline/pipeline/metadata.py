from os import environ, listdir, path
from datetime import datetime
from click import command, option, echo, secho, style
from pathlib import Path
from sparrow.database import get_or_create
from sparrow.import_helpers import BaseImporter, SparrowImportError

from .extract_tables import extract_data_tables

def print_dataframe(df):
    secho(str(df.fillna('—'))+'\n', dim=True)

class MetadataImporter(BaseImporter):
    authority = "WiscAr"
    def __init__(self, db, **kwargs):
        super().__init__(db)
        self.verbose = kwargs.pop("verbose", False)
        self.create_parameters()

    def import_datafile(self, fn, rec, **kwargs):
        """
        Import an original data file
        """
        verbose = self.verbose
        # Extract data tables from Excel sheet

        # File modification time is right now the best proxy
        # for creation date (note: sessions will be duplicated
        # if input files are changed)
        mod_time = datetime.fromtimestamp(path.getmtime(fn))

        try:
            assert True
        except Exception as exc:
            raise SparrowImportError(str(exc))
        if verbose:
            print_dataframe(incremental_heating)
            print_dataframe(info)
            print_dataframe(results.transpose())

        sample = self.sample(name=info.pop('Sample'))
        target = self.material(info.pop('Material'))
        instrument = self.db.get_or_create(
            self.m.instrument,
            name="MAP 215-50")
        method = self.method("Ar/Ar "+info.pop("Type"))
        self.add(sample, target, instrument, method)
        self.db.session.flush()

        session = self.db.get_or_create(
            self.m.session,
            sample_id=sample.id,
            instrument=instrument.id,
            technique=method.id,
            date=mod_time,
            target=target.id)
        session.date_precision = "day"
        self.add(session)
        self.db.session.flush()


        info = self.general_info(session, info)
        session.data = info.to_dict()

        for i, step in enumerate(incremental_heating.iterrows()):
            self.import_heating_step(i, step, session, incremental_heating)

        # Import results table
        try:
            res = results.loc["Age Plateau"]
            self.import_age_plateau(session, res)
        except KeyError:
            pass

        res = results.loc["Total Fusion Age"]
        self.import_fusion_age(session, res)

        # This function returns the top-level
        # record that should be linked to the datafile
        self.db.session.flush()
        yield session
