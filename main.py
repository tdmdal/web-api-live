from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI(title="Alien Species API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your custom domain
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Alien(BaseModel):
    species: str
    habitat: str
    lifespan: float
    size: str
    weight: float

class ErrorResponse(BaseModel):
    detail: str

# Sample dataset
aliens_data = [
    {"species": "Zentar", "habitat": "Jungle", "lifespan": 120.0, "size": "Large", "weight": 300.0},
    {"species": "Gorlax", "habitat": "Desert", "lifespan": 85.0, "size": "Medium", "weight": 150.0},
    {"species": "Vexor", "habitat": "Ocean", "lifespan": 95.0, "size": "Small", "weight": 50.0},
    {"species": "Plutoid", "habitat": "Mountain", "lifespan": 150.0, "size": "Medium", "weight": 180.0},
    {"species": "Zyphor", "habitat": "Jungle", "lifespan": 200.0, "size": "Large", "weight": 500.0},
    {"species": "Xeltron", "habitat": "Desert", "lifespan": 75.0, "size": "Small", "weight": 40.0},
    {"species": "Mentar", "habitat": "Jungle", "lifespan": 110.0, "size": "Medium", "weight": 280.0},
    {"species": "Draknor", "habitat": "Ocean", "lifespan": 90.0, "size": "Small", "weight": 140.0},
    {"species": "Seltrix", "habitat": "Desert", "lifespan": 130.0, "size": "Large", "weight": 320.0},
    {"species": "Quorin", "habitat": "Mountain", "lifespan": 180.0, "size": "Medium", "weight": 400.0},
]

# Convert raw dicts to Pydantic objects
aliens = [Alien(**data) for data in aliens_data]

@app.get("/aliens/random", response_model=Alien, summary="Get a random alien")
def get_random_alien():
    return random.choice(aliens)

@app.get("/species", response_model=List[str], summary="List all available species")
def get_species():
    return [a.species for a in aliens]

@app.get("/habitats", response_model=List[str], summary="List all available habitats")
def get_habitats():
    return list(set(a.habitat for a in aliens))

@app.get("/sizes", response_model=List[str], summary="List all available sizes")
def get_sizes():
    return list(set(a.size for a in aliens))

@app.get(
    "/aliens/species/{species_name}",
    response_model=Alien,
    responses={404: {"model": ErrorResponse}},
    summary="Get alien by species name"
)
def get_alien_by_species(species_name: str):
    for alien in aliens:
        if alien.species.lower() == species_name.lower():
            return alien
    raise HTTPException(status_code=404, detail="Alien species not found")

@app.get("/aliens", response_model=List[Alien], summary="Get aliens by optional filters")
def get_aliens(habitat: Optional[str] = None, size: Optional[str] = None):
    result = aliens
    if habitat:
        result = [a for a in result if a.habitat.lower() == habitat.lower()]
    if size:
        result = [a for a in result if a.size.lower() == size.lower()]
    return result

