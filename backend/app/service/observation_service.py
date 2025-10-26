from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

def get_coords(db: Session) -> List[List]:
    observations = db.query(Observations).all()
    
    result = []
    for obs in observations:
        result.append([
            obs.observation_time,
            float(obs.right_ascension),
            float(obs.declination)
        ])
    
    return result