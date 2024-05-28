from item_service.models.models import Base

def entity_to_dict(entity: Base):
    result_dict = entity.__dict__
    result_dict.pop('_sa_instance_state', None)
    return result_dict