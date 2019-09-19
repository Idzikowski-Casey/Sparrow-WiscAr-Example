import numpy as N

from os import environ, listdir, path
from datetime import datetime
from click import command, option, echo, secho, style
from pathlib import Path
from sparrow.database import get_or_create
from sparrow.import_helpers import BaseImporter, SparrowImportError
from pandas import read_excel, isna

def print_dataframe(df):
    secho(str(df.fillna('—'))+'\n', dim=True)

def row_to_mapping(row):
    print(row)
    def get(key):
        v = row['key']
        return v if not isna(v) else None

    return dict(
        location=[get('longitude'), get('latitude')],
        elevation=get('elevation (m)'),

        depth=get('depth (m)'))

def confirm_matching_irradiation(session, row):
    irr = session.get_attribute("Irradiation ID")
    # Sessions should not have two Irradiation IDs
    assert len(irr) == 1
    v = irr[0].value
    v1 = str(row['Irradiation'])
    if not v.startswith(v1):
        raise SparrowImportError(f"Irradiation mismatch")
    print(f"  Irradiation {v}")

class MetadataImporter(BaseImporter):
    authority = "WiscAr"
    def __init__(self, db, metadata_file, **kwargs):
        super().__init__(db)
        self.verbose = kwargs.pop("verbose", False)
        self.iterfiles([metadata_file])

    def import_datafile(self, fn, rec, **kwargs):
        """
        Import an original data file
        """
        verbose = self.verbose
        # Extract data tables from Excel sheet

        df = read_excel(fn, sheet_index=0)
        n = len(df)
        print(f"{n} rows")
        # Group everything

        self.import_samples(df)

    def import_samples(self, df):
        groups = df.groupby("sample_name")
        samples = groups.first()
        # Just get the first of each group for now
        # We might not want to assume sample ID uniqueness
        print(f"{len(samples)} unique sample names")

        # Import individual samples
        for i, row in samples.iterrows():
            try:
                self.import_sample(row)
                self.db.session.commit()
            except Exception as exc:
                secho(exc.__class__.__name__+": "+str(exc), fg='red')
                self.db.session.rollback()

        self.db.session.flush()

    def import_sample(self, row):
        name = str(row.name)
        s = self.sample(name=name)
        echo(f"Sample {name}")
        if s._created:
            secho(f"  created", fg='yellow')
        else:
            secho(f"  found existing", fg='green')
        n = len(s.session_collection)
        echo(f"  {n} sessions")
        # Check that irradiation matches
        session = None
        if n > 0:
            session = s.session_collection[0]
            confirm_matching_irradiation(session, row)

        lon = row['longitude']
        lat = row['latitude']
        if not (isna(lon) or isna(lat)):
            loc = self.location(lon,lat)
            print(loc)
            s.location = loc

        lith = row['lithology']
        if not isna(lith):
            print(lith)
            s._material = self.material(lith)
        self.db.session.flush()

        if n > 1:
            secho("  More than one session for this sample\n  skipping project import", fg='red', dim=True)
            return

        self.import_project(row, session)

    def import_project(self, row, session):
        pass


