from fastapi import APIRouter
from workflow import main_flow

router = APIRouter()


@router.get("/start")
def start(address: str, bucket_name: str, blurb: str, area: str, class_tag: str) -> bool:
    """ start execute one task """
    main_flow.execute(
        address,
        bucket_name,
        main_flow.InsertManage(blurb, area, class_tag)
    )
    return True
