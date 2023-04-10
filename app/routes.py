from typing import Annotated

from fastapi import APIRouter, Form, Request
from jinja2_fragments.fastapi import Jinja2Blocks

from app.config import Settings
from app.crud import CRUD
from app.helpers import (
    artist_image_list,
    get_active_members,
    get_profile,
    get_website,
    get_wikipedia_entry,
)

settings = Settings()
router = APIRouter()
templates = Jinja2Blocks(settings.TEMPLATE_DIR)


@router.get("/")
def index(request: Request):
    """Home page - generates an image and name of a random artist.

    TODO: Create an htmx request from the `Randomize` button that only
    refreshes the image and name of the random artist.

    SOLUTION:
        1.  Instead of `<a href="/">`, use `<a hx-get="/">`
        2.  Use hx-target to point to the `<div>` element that contains
        the image. (hint: give the element an `id` to target)
        3.  Use Jinja2Blocks to render only the fragment that you need. Enclose
        the fragment with {% block ... %} with appropriate name
        4.  In the route, check for an HX-Request header. If present,
        provide the block_name to render (defined in step 3).
        5.  Update the TemplateResponse to include the block_name.
    """

    db = CRUD().with_table("artist_info")

    block_name = None
    context = {
        "request": request,
        "artist_count": len(db.all_items()),
        "random_artist": db.get_random_item(),
    }

    if request.headers.get("HX-Request"):
        block_name = "main_image"

    return templates.TemplateResponse("main.html", context, block_name=block_name)


@router.get("/about")
def about(request: Request):
    """About page - contains info about the site.

    TODO: Create an `hx-get` request on the 'About' link that replaces the
    #body element of the page. Hint: Use Jinja2Blocks to render a fragment.
    Also cover the case where a user navigates directly to `/about`.

    SOLUTION:
    1.  Instead of `<a href="/about">`, use `<a hx-get="/about">`
    2.  Use hx-target to point to the `<div>` element that contains the
    main content of the site.
    3.  Make sure that you "swap" the entire element
    4.  Add the `/about` endpoint to the url.
    5.  In the route, check for an HX-Request header. If present,
        provide the block_name to render.
    6.  Update the TemplateResponse to include the block_name
    """
    block_name = None
    if request.headers.get("HX-Request"):
        block_name = "content"
    return templates.TemplateResponse("about.html", {"request": request}, block_name=block_name)


@router.get("/catalog")
def catalog(request: Request):
    """Catalog page contains a list of artists in `artist_details` table.
    Each card contains the artist name and active members. Clicking on a card
    sends an `hx-get` request--the response is the artist profile rendered on
    the card.

    TODO: Make the artist card "toggable" (clicking returns to artist/members)

    SOLUTION:
    1.  Created two blocks in `profile.html` for each card state and used unique
    {% block ... %} tags for each div element.
    2.  In the artist profile block, send the artist id back to the route so that
    the db query can fetch the artist name/members again. (hint: you can use htmx
    to send a custom header to the client)
    3.  Add logic in the route to handle each type of card state. (hint: use the `<div>` id
    css selector)
    4.  Update the TemplateResponse to include the corresponding block_name.
    """

    db = CRUD().with_table("artist_details")
    artists = db.all_items()

    block_name = None
    template = "catalog.html"
    context = {
        "request": request,
        "artists": artists,
        "get_website": get_website,
        "get_members": get_active_members,
        "get_profile": get_profile,
    }

    if request.headers.get("HX-Request"):
        template = "artist/profile.html"

        if "toggle" not in request.headers.get("HX-Trigger"):
            id = request.headers.get("HX-Trigger")
            artist = db.find("id", int(id))
            context["artist"] = artist[0]
            block_name = "artist_profile"
        else:
            id = request.headers.get("artist-id")
            artist = db.find("id", int(id))
            context["artist"] = artist[0]
            block_name = "artist_name"

    return templates.TemplateResponse(template, context, block_name=block_name)


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
        block_name = "artist_cards"

    return templates.TemplateResponse("catalog.html", context, block_name=block_name)


@router.get("/detail")
def artist_details(request: Request, doc_id: int | None = None):
    """ Artist details page - Each section contains artist information, including
    images, profile, website, and wikipedia link (if available). The page is set up
    with "infinite scroll" using the htmx `revealed` trigger to send requests.
    """

    db = CRUD().with_table("artist_details")
    block_name = None

    if not request.headers.get("HX-Request"):
        doc_id = 1
    else:
        block_name = "details"

    artist = db.get_by_id(doc_id)
    next_id = doc_id + 1

    context = {
        "request": request,
        "artist": artist,
        "images": artist_image_list,
        "get_website": get_website,
        "get_profile": get_profile,
        "get_members": get_active_members,
        "get_wiki": get_wikipedia_entry,
        "next_id": next_id,
    }

    return templates.TemplateResponse("artist/details.html", context, block_name=block_name)
