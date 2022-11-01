from .BaseModel import Base, BaseQueryModel

class UserContacts(Base):
    __tablename__ = 'UserContacts'
    __table_args__ = {'autoload': True}


class UserContactsQueryModel(BaseQueryModel):

    def get_user_contacts_by_user_id(self, user_id):
        user_contact = self.session.query(UserContacts).filter(
            UserContacts.user_id == user_id).filter(UserContacts.is_active == True).first()
        return user_contact

    def add_user_contacts_by_user_id(self, user_id, contact_info=None):
        inactive_user_contact = self.session.query(UserContacts).filter(
            UserContacts.user_id == user_id).filter(UserContacts.is_active == False).first()
        if inactive_user_contact:
            inactive_user_contact.is_active = True
            if contact_info:
                for key, value in contact_info.items():
                    setattr(inactive_user_contact, key, value)
            self.session.commit()
        else:
            user_contact = UserContacts(
                user_id=user_id,
                is_active=True
            )
            if contact_info:
                for key, value in contact_info.items():
                    setattr(user_contact, key, value)
            self.session.add(user_contact)
            self.session.commit()

    def update_user_contacts_by_user_id(self, user_id, contact_info=None):
        user_contact = self.session.query(UserContacts).filter(
            UserContacts.user_id == user_id).filter(UserContacts.is_active == True).first()
        if contact_info:
            for key, value in contact_info.items():
                setattr(user_contact, key, value)
        self.session.commit()

    def delete_user_contacts_by_user_id(self, user_id):
        user_contact = self.session.query(UserContacts).filter(
            UserContacts.user_id == user_id).filter(UserContacts.is_active == True).first()
        user_contact.is_active = False
        self.session.commit()
