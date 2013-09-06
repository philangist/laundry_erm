import redis
import ast

def get_redis_client(host='localhost', port=6379, db=0):
    return redis.StrictRedis(host, port, db)

def set_contact_info(first_name, last_name, contact_info,
        redis_client):
    full_name = "{} {}".format(first_name, last_name)
    """
    existing_contact_info = get_contact_info(first_name, last_name,
        redis_client)
    if existing_contact_info:
        if contact_info not in existing_contact_info:
            existing_contact_info += (contact_info)
            contact_info = existing_contact_info
    else:
    """    
    contact_info = contact_info
    redis_client.set(full_name, contact_info)

def get_contact_info(first_name, last_name, redis_client):
    full_name = "{} {}".format(first_name, last_name)
    contact_info = redis_client.get(full_name)
    if contact_info:
        contact_info = ast.literal_eval(contact_info)
    return contact_info
