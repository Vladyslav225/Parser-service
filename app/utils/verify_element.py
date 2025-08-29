from fastapi import HTTPException

def verify_element(element, message: str, status_code: int):
    if not element:
        raise HTTPException(status_code=status_code, detail=message)
    
    return True