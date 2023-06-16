import asyncio

from core.database import geo
from core.models import Municipality

municipality_collection = geo.Municipality


async def fetch_all_municipalities() -> list[Municipality]:
    """
    Fetches all municipality documents from the collection
    and returns them as a list of Municipality objects.
    """
    municipalities = []
    cursor = municipality_collection.find({})
    async for document in cursor:
        municipalities.append(Municipality(**document))

    return municipalities


async def fetch_municipality_by_id(m_id: int) -> dict[str, str] | None:
    """
    Retrieves a municipality document from the collection based on the given ID.
    """
    document = await municipality_collection.find_one({"m_id": m_id})
    return document


async def create_municipality(municipality: Municipality) -> Municipality:
    """
    Inserts a new municipality document into the collection
    and returns the created municipality.
    """
    await municipality_collection.insert_one(municipality.dict())
    return municipality


async def update_municipality(
    m_id: int,
    name: str,
    state: str,
) -> dict[str, str] | None:
    """
    Updates the name and state fields of a municipality document
    identified by the given ID, and returns the updated document.
    """
    await municipality_collection.update_one(
        {"m_id": m_id},
        {
            "$set": {
                "name": name,
                "state": state,
            }
        },
    )

    document = await municipality_collection.find_one({"m_id": m_id})
    return document


async def remove_municipality(m_id: int) -> bool:
    """
    Deletes a municipality document from the collection based
    on the given ID, and returns True if the deletion was successful.
    """
    municipality_exists = await municipality_collection.find_one({"m_id": m_id})
    if municipality_exists:
        await municipality_collection.delete_one({"m_id": m_id})
        return True
    return False


async def remove_all_municipalities() -> None:
    """Removes all municipalities from the database"""
    x = await municipality_collection.delete_many({})
    print(f"Removed all ({x.deleted_count}) municipalities from the database.")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(remove_all_municipalities())
        # loop.run_until_complete(remove_municipality(99999))
    except KeyboardInterrupt:
        pass
