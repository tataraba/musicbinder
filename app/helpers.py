# Helper functions for extracting data - It presumes an "artist" dictionary object

import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for FastAPI app. It will run all code before `yield`
    on app startup, and will run code after `yeld` on app shutdown. This method
    runs a subprocess on app startup which is the equivalent of running the
    tailwindcss command `tailwindcss -i ./src/tw.css -o ./css/main.css`.

    Must be passed as a property of the FastAPI app. (app = FastAPI(lifespan=lifespan))
    """

    try:
        subprocess.run(
            [
                "tailwindcss",
                "-i",
                str(settings.STATIC_DIR / "src" / "tw.css"),
                "-o",
                str(settings.STATIC_DIR / "css" / "main.css"),
            ]
        )
    except Exception as e:
        raise RuntimeError from e
    yield


def get_active_members(artist: dict):
    """This returns active members from the artist_details table. This
    method can be used within the Jinja template."""

    if "members" not in artist:
        return [artist["name"]]
    all_members = artist["members"]
    active_members = []
    for member in all_members:
        if member["active"]:
            active_members.append(member["name"])
    return active_members  # limit 14 members


def get_website(artist: dict):
    if "urls" not in artist:
        return artist["uri"]  # send discogs uri if no url found
    return artist["urls"][0]


def get_wikipedia_entry(artist: dict):
    if "urls" not in artist:
        return "No wikipedia entry found"
    wiki_url = [x for x in artist["urls"] if "wikipedia" in x]
    if not wiki_url:
        return "No wikipedia entry found"
    return wiki_url[0]


def get_profile(artist: dict):
    if not artist["profile"]:
        return "No profile available"
    else:
        profile = artist["profile"]
        profile = profile.replace("[", "<").replace("]", ">")
        return profile

def artist_image_list(artist: dict):
    if "images" not in artist:
        return "No images available"
    else:
        image_dict = artist["images"]
        images = [item["resource_url"] for item in image_dict]
        return images
