import config 


def get_thread_id_from_recipient_id(recipient_id: str) -> str | None:
    try:
        thread_id = config.MAPPING_DATA['mappings'].get(recipient_id)
        return thread_id
    except:
        return None
    
    
def update_thread_id_from_recipient_id(recipient_id: str,
                                       thread_id: str) -> None:
    try:
        config.MAPPING_DATA['mappings'].update({recipient_id: thread_id})
        return None
    except:
        None
