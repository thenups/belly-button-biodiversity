from app234 import db

class Otu(db.Model):
    __tablename__ = db.Model.metadata.tables['otu']

    def __repr__(self):
        return self.otu_id

class Samples(db.Model):
    __tablename__ = db.Model.metadata.tables['samples']

    def __repr__(self):
        return self.otu_id


class Metadata(db.Model):
    __tablename__ = db.Model.metadata.tables['samples_metadata']

    def __repr__(self):
        return self.otu_id
