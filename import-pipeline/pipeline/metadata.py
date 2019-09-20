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

def format_authorlist(author):
    __ = [a.strip() for a in author.replace(';',',').split(",")]
    if len(__) == 1:
        auths = __[0]
    if len(__) == 2:
        auths = ", ".join(__)
    else:
        auths = __[0]
        if 'et al' not in auths:
            auths += " et al."
    return auths

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

        self.import_sheet(fn, 0)
        self.import_sheet(fn, 1)

    def import_sheet(self, fn, index=0):
        df = read_excel(fn, sheetname=index)
        n = len(df)
        print(f"{n} rows")
        self.import_samples(df)
        self.import_projects(df)

    def import_samples(self, df):
        # Group everything
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

    def import_project(self, name, group):
        (paper_title, link) = name
        author = group['author'].unique()[0]
        first_part = paper_title.split(": ")[0]
        title_summary = " ".join(first_part.split()[:8])+"..."
        if not isna(author):
            auths = format_authorlist(author)

            title_summary = auths+" — "+title_summary

        print(title_summary)

        doi = link.split("doi.org/")[-1]
        if doi.startswith("doi: "):
            doi = doi[5:]
        link = None
        if not doi.startswith("10"):
            link = doi
            doi = None
        print(doi, link)

        def get(key):
            vals = [v for v in group[key].unique() if not isna(v)]
            if len(vals) == 0:
                return None
            return vals[0]

        p = self.project(name=title_summary)

        pub = self.m.publication.get_or_create(
            doi=doi,
            title=get('Title'),
            link=link)

        pub.author = author
        pub.journal = get('journal')
        pub.year = get('year')
        p.publication_collection.append(pub)

        sample_names = [a for a in group.sample_name.unique() if not isna(a)]
        if len(sample_names):
            q = (self.db.session.query(self.m.session)
                .join(self.m.sample)
                .filter(self.m.sample.name.in_(sample_names)))
            p.session_collection += q
        self.db.session.add(p)
        self.db.session.flush()
        print("")

    def import_projects(self, df):
        # Group by publication for now
        projects = df.groupby(["Title", "doi link"])
        for name, group in projects:
            self.import_project(name, group)
