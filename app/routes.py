from typing import Annotated

from fastapi import APIRouter, Form, Request
from jinja2_fragments.fastapi import Jinja2Blocks

from app.config import Settings
from app.crud import CRUD
from app.helpers import (
    get_active_members,
    get_profile,
    get_website,
)

settings = Settings()
router = APIRouter()
templates = Jinja2Blocks(settings.TEMPLATE_DIR)


@router.get("/")
def index(request: Request):
    """Home page - generates an image and name of a random artist.

    TODO: Create an htmx request from the `Randomize` button that only
    refreshes the image and name of the random artist.
    """

    db = CRUD().with_table("artist_info")

    context = {
        "request": request,
        "artist_count": len(db.all_items()),
        "random_artist": db.get_random_item(),
    }

    return templates.TemplateResponse("main.html", context)


@router.get("/about")
def about(request: Request):
    """About page - contains info about the site.

    TODO: Create an `hx-get` request on the 'About' link that replaces the
    #body element of the page. Hint: Use Jinja2Blocks to render a fragment.
    Also cover the case where a user navigates directly to `/about`.
    """

    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/catalog")
def catalog(request: Request):
    """Catalog page contains a list of artists in `artist_details` table.
    Each card contains the artist name and active members. Clicking on a card
    sends an `hx-get` request--the response is the artist profile rendered on
    the card.

    TODO: Make the artist card "toggable" (clicking returns to artist/members)
    """

    db = CRUD().with_table("artist_details")
    artists = db.all_items()

    template = "catalog.html"
    context = {
        "request": request,
        "artists": artists,
        "get_website": get_website,
        "get_members": get_active_members,
        "get_profile": get_profile,
    }

    if request.headers.get("HX-Request"):
        id = request.headers.get("HX-Trigger")
        artist = db.find("id", int(id))
        template = "artist/profile.html"
        context["artist"] = artist[0]

    return templates.TemplateResponse(template, context)


@router.get("/search")
def search_get(request: Request):
    """Search page - populate a list of all artists when search is empty."""

    db = CRUD().with_table("artist_details")
    artists = db.all_items()

    context = {
        "request": request,
        "artists": artists,
        "get_website": get_website,
        "get_members": get_active_members,
        "from_search": True,
    }
    block_name = None

    if request.headers.get("HX-Request"):
        block_name = "content"

    return templates.TemplateResponse("catalog.html", context, block_name=block_name)


@router.post("/search")
def search_post(request: Request, search: Annotated[str, Form()]):
    """Search page - Post requests are generated from htmx requests sent on keyup events,
    with a 500ms delay (so as not to bombard the server with requests). Note that the results
    of each POST request are contained within the `artist_card` block in the `catalog.html`
    template. This is the only content sent back to the client (thanks to jinja2-fragments).

    TODO: When user erases search field, receiving a 422 response. Would rather it be the
    same as the GET request, which populates a list of all artists as default."""

    print(search)
    db = CRUD().with_table("artist_details")
    artists = db.search(key="name", value=search)

    context = {
        "request": request,
        "artists": artists,
        "get_website": get_website,
        "get_members": get_active_members,
        "from_search": True,
    }
    block_name = None

    if request.headers.get("hx-request"):
        block_name = "artist_card"

    return templates.TemplateResponse("catalog.html", context, block_name=block_name)
