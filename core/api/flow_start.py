from fastapi import APIRouter
from workflow import main_flow

router = APIRouter()


@router.get("/import")
def import_xvideos(address: str, bucket_name: str, blurb: str, area: str, class_tag: str) -> dict:
    """ start execute one task """
    return main_flow.execute(
        address,
        bucket_name,
        main_flow.InsertManage(blurb, area, class_tag)
    )
