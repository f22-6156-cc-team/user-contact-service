from .BaseModel import Base, BaseQueryModel

class Phone(Base):
    __tablename__ = 'phone'
    __table_args__ = {'autoload': True}


class PhoneQueryModel(BaseQueryModel):
    def get_phones_by_user_id(self, user_id):
        phones = self.session.query(Phone).filter(
            Phone.user_id == user_id).filter(Phone.is_active == True).all()
        return phones

    def get_phone_by_user_id_and_phone_id(self, user_id, phone_id):
        phone = self.session.query(Phone).filter(
            Phone.user_id == user_id).filter(
            Phone.phone_id == phone_id).filter(Phone.is_active == True).first()
        return phone

    def add_phone_by_user_id(self, user_id, phone_info=None):
        phone = Phone(
            user_id=user_id,
            is_active=True
        )
        if phone_info:
            for key, value in phone_info.items():
                setattr(phone, key, value)

        self.session.add(phone)
        self.session.flush()
        
        phone_id = phone.phone_id
        self.session.commit()
        return phone_id

    def update_phone_by_user_id_and_phone_id(self, user_id, phone_id, phone_info=None):
        phone = self.session.query(Phone).filter(
            Phone.user_id == user_id).filter(
            Phone.phone_id == phone_id).filter(Phone.is_active == True).first()
        if phone_info:
            for key, value in phone_info.items():
                setattr(phone, key, value)
        self.session.commit()

    def delete_phone_by_user_id_and_phone_id(self, user_id, phone_id):
        phone = self.session.query(Phone).filter(
            Phone.user_id == user_id).filter(
            Phone.phone_id == phone_id).filter(Phone.is_active == True).first()
        phone.is_active = False
        self.session.commit()
