from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, CheckConstraint, UniqueConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class UserTable(Base):
    __tablename__ = 'user_table'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    version = Column(Integer, nullable=False, server_default='1')
    login = Column(Text, nullable=False)
    password_hash = Column(String(40), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())

class ObservationGroups(Base):
    __tablename__ = 'observation_groups'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    name = Column(String(100))
    description = Column(Text)
    status = Column(String(20), server_default='active')
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())

class Observations(Base):
    __tablename__ = 'observations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey('user_table.id', ondelete='CASCADE'), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('observation_groups.id', ondelete='CASCADE'), nullable=False)
    observation_time = Column(DateTime(timezone=True), nullable=False)
    right_ascension = Column(Float, nullable=False)  # Изменено на Float
    declination = Column(Float, nullable=False)      # Изменено на Float
    observer_name = Column(String(100))
    observation_notes = Column(Text)
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())

class OrbitalParameters(Base):
    __tablename__ = 'orbital_parameters'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    group_id = Column(UUID(as_uuid=True), ForeignKey('observation_groups.id', ondelete='CASCADE'), nullable=False)
    semi_major_axis = Column(Float, nullable=False)      # Изменено на Float
    eccentricity = Column(Float, nullable=False)         # Изменено на Float
    inclination = Column(Float, nullable=False)          # Изменено на Float
    longitude_ascending_node = Column(Float, nullable=False)  # Изменено на Float
    argument_perihelion = Column(Float, nullable=False)       # Изменено на Float
    time_perihelion = Column(DateTime(timezone=True), nullable=False)
    calculation_date = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    used_observations_count = Column(Integer, nullable=False)

class CloseApproaches(Base):
    __tablename__ = 'close_approaches'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    group_id = Column(UUID(as_uuid=True), ForeignKey('observation_groups.id', ondelete='CASCADE'), nullable=False)
    orbital_parameters_id = Column(UUID(as_uuid=True), ForeignKey('orbital_parameters.id', ondelete='CASCADE'), nullable=False)
    approach_time = Column(DateTime(timezone=True), nullable=False)
    distance_au = Column(Float, nullable=False)  # Изменено на Float
    distance_km = Column(Float, nullable=False)  # Изменено на Float
    calculation_date = Column(DateTime(timezone=True), server_default=func.current_timestamp())