from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
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
    password_hash = Column(String(40), nullable=False)  # bytea represented as String for simplicity
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint('length(login) >= 6 AND length(login) <= 20', name='user_table_login_check'),
        CheckConstraint('octet_length(password_hash::bytea) = 40', name='user_table_password_hash_check'),
        UniqueConstraint('login', name='user_login_unique'),
    )

class ObservationGroups(Base):
    __tablename__ = 'observation_groups'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    name = Column(String(100))
    description = Column(Text)
    status = Column(String(20), server_default='active')
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint("status IN ('active', 'processing', 'completed', 'error')", name='observation_groups_status_check'),
    )

class Observations(Base):
    __tablename__ = 'observations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey('user_table.id', ondelete='CASCADE'), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('observation_groups.id', ondelete='CASCADE'), nullable=False)
    observation_time = Column(DateTime(timezone=True), nullable=False)
    right_ascension = Column(String(50), nullable=False)  # Using String instead of DOUBLE PRECISION for compatibility
    declination = Column(String(50), nullable=False)      # Using String instead of DOUBLE PRECISION for compatibility
    observer_name = Column(String(100))
    observation_notes = Column(Text)
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint('right_ascension::double precision >= 0 AND right_ascension::double precision < 360', name='valid_ra'),
        CheckConstraint('declination::double precision >= -90 AND declination::double precision <= 90', name='valid_dec'),
    )

class OrbitalParameters(Base):
    __tablename__ = 'orbital_parameters'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    group_id = Column(UUID(as_uuid=True), ForeignKey('observation_groups.id', ondelete='CASCADE'), nullable=False)
    semi_major_axis = Column(String(50), nullable=False)  # Using String instead of DOUBLE PRECISION
    eccentricity = Column(String(50), nullable=False)     # Using String instead of DOUBLE PRECISION
    inclination = Column(String(50), nullable=False)      # Using String instead of DOUBLE PRECISION
    longitude_ascending_node = Column(String(50), nullable=False)  # Using String instead of DOUBLE PRECISION
    argument_perihelion = Column(String(50), nullable=False)       # Using String instead of DOUBLE PRECISION
    time_perihelion = Column(DateTime(timezone=True), nullable=False)
    calculation_date = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    used_observations_count = Column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint('semi_major_axis::double precision > 0', name='positive_semi_major_axis'),
        CheckConstraint('eccentricity::double precision >= 0', name='valid_eccentricity'),
        CheckConstraint('inclination::double precision >= 0 AND inclination::double precision <= 180', name='valid_inclination'),
        CheckConstraint('longitude_ascending_node::double precision >= 0 AND longitude_ascending_node::double precision < 360 AND argument_perihelion::double precision >= 0 AND argument_perihelion::double precision < 360', name='valid_angles'),
    )

class CloseApproaches(Base):
    __tablename__ = 'close_approaches'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
    group_id = Column(UUID(as_uuid=True), ForeignKey('observation_groups.id', ondelete='CASCADE'), nullable=False)
    orbital_parameters_id = Column(UUID(as_uuid=True), ForeignKey('orbital_parameters.id', ondelete='CASCADE'), nullable=False)
    approach_time = Column(DateTime(timezone=True), nullable=False)
    distance_au = Column(String(50), nullable=False)  # Using String instead of DOUBLE PRECISION
    distance_km = Column(String(50), nullable=False)  # Using String instead of DOUBLE PRECISION
    calculation_date = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint('distance_au::double precision > 0 AND distance_km::double precision > 0', name='positive_distance'),
    )