from fastapi import HTTPException

def verify_element(element, message: str, status_code: int):
    if not element:
        print(HTTPException(status_code=status_code, detail=message))
        return None
    
    return True

def verify_elements(element, message: str, status_code: int):
    if not element:
        print(HTTPException(status_code=status_code, detail=message))
        return []
    
    return True

async def find_one_element(
        parent_element: object,
        selector: str,
        error_message: str,
        status_code: int
):
    element = parent_element.select_one(selector)
    verify_element(
        element=element,
        message=error_message,
        status_code=status_code
    )

    return element

async def find_all_elements(
        parent_element: object, 
        selector: str,
        error_message: str,
        status_code: int
):
    elements = parent_element.select(selector)
    verify_elements(
        element=elements,
        message=error_message,
        status_code=status_code
    )

    return elements