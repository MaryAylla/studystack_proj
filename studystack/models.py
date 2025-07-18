
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

summary_tags = db.Table('summary_tags',
    db.Column('summary_id', db.Integer, db.ForeignKey('summaries.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    summaries = db.relationship('Summary', back_populates='subject')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    summaries = db.relationship('Summary', secondary=summary_tags, back_populates='tags')

class Summary(db.Model):
    __tablename__ = 'summaries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    subject = db.relationship('Subject', back_populates='summaries')
    
    tags = db.relationship('Tag', secondary=summary_tags, back_populates='summaries')