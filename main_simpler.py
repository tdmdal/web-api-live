from fastapi import FastAPI, HTTPException
from typing import Optional
import random

app = FastAPI(title="Alien Species API")

# Sample aliens dataset
aliens = [
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

@app.get("/aliens/random", summary="Get a random alien")
def get_random_alien():
    return random.choice(aliens)

@app.get("/species", summary="List all available species")
def get_species():
    return [alien["species"] for alien in aliens]

@app.get("/habitats", summary="List all available habitats")
def get_habitats():
    return list(set(alien["habitat"] for alien in aliens))

@app.get("/sizes", summary="List all available sizes")
def get_sizes():
    return list(set(alien["size"] for alien in aliens))

@app.get("/aliens/species/{species_name}", summary="Get alien by species name")
def get_alien_by_species(species_name: str):
    for alien in aliens:
        if alien["species"].lower() == species_name.lower():
            return alien
    raise HTTPException(status_code=404, detail="Alien species not found")

@app.get("/aliens", summary="Get aliens by optional filters")
def get_aliens(habitat: Optional[str] = None, size: Optional[str] = None):
    filtered = aliens
    if habitat:
        filtered = [alien for alien in filtered if alien["habitat"].lower() == habitat.lower()]
    if size:
        filtered = [alien for alien in filtered if alien["size"].lower() == size.lower()]
    return filtered



