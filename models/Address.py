from .BaseModel import Base, BaseQueryModel

class Address(Base):
    __tablename__ = 'address'
    __table_args__ = {'autoload': True}


class AddressQueryModel(BaseQueryModel):

    def get_addresses_by_user_id(self, user_id):
        addresses = self.session.query(Address).filter(
            Address.user_id == user_id).filter(Address.is_active == True).all()
        return addresses

    def get_address_by_user_id_and_address_id(self, user_id, address_id):
        address = self.session.query(Address).filter(
            Address.user_id == user_id).filter(
            Address.address_id == address_id).filter(Address.is_active == True).first()
        return address

    def add_address_by_user_id(self, user_id, address_id, address_info=None):
        inactive_user_address = self.session.query(Address).filter(
            Address.user_id == user_id).filter(
            Address.address_id == address_id).filter(Address.is_active == False).first()
        if inactive_user_address:
            inactive_user_address.is_active = True
            if address_info:
                for key, value in address_info.items():
                    setattr(inactive_user_address, key, value)
            self.session.commit()
        else:
            address = Address(
                user_id=user_id,
                address_id=address_id,
                is_active=True
            )
            if address_info:
                for key, value in address_info.items():
                    setattr(address, key, value)

            self.session.add(address)
            self.session.commit()
        

    def update_address_by_user_id_and_address_id(self, user_id, address_id, address_info=None):
        address = self.session.query(Address).filter(
            Address.user_id == user_id).filter(
            Address.address_id == address_id).filter(Address.is_active == True).first()
        if address_info:
            for key, value in address_info.items():
                setattr(address, key, value)
        self.session.commit()

    def delete_address_by_user_id_and_address_id(self, user_id, address_id):
        address = self.session.query(Address).filter(
            Address.user_id == user_id).filter(
            Address.address_id == address_id).filter(Address.is_active == True).first()
        address.is_active = False
        self.session.commit()

    def delete_address_by_user_id(self, user_id):
        addresses = self.session.query(Address).filter(
            Address.user_id == user_id).filter(Address.is_active == True).all()
        for address in addresses:
            address.is_active = False
        self.session.commit()
