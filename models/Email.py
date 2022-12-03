from .BaseModel import Base, BaseQueryModel

class Email(Base):
    __tablename__ = 'email'
    __table_args__ = {'autoload': True}


class EmailQueryModel(BaseQueryModel):

    def get_emails_by_user_id(self, user_id):
        emails = self.session.query(Email).filter(
            Email.user_id == user_id).filter(Email.is_active == True).all()
        return emails

    def get_email_by_user_id_and_email_id(self, user_id, email_id):
        email = self.session.query(Email).filter(
            Email.user_id == user_id).filter(
            Email.email_id == email_id).filter(Email.is_active == True).first()
        return email

    def add_email_by_user_id(self, user_id, email_id, email_info=None):
        inactive_user_email = self.session.query(Email).filter(
            Email.user_id == user_id).filter(
            Email.email_id == email_id).filter(Email.is_active == False).first()
        if inactive_user_email:
            inactive_user_email.is_active = True
            if email_info:
                for key, value in email_info.items():
                    setattr(inactive_user_email, key, value)
            self.session.commit()
        else:
            email = Email(
                user_id=user_id,
                email_id=email_id,
                is_active=True
            )
            if email_info:
                for key, value in email_info.items():
                    setattr(email, key, value)

            self.session.add(email)
            self.session.commit()


    def update_email_by_user_id_and_email_id(self, user_id, email_id, email_info=None):
        email = self.session.query(Email).filter(
            Email.user_id == user_id).filter(
            Email.email_id == email_id).filter(Email.is_active == True).first()
        if email_info:
            for key, value in email_info.items():
                setattr(email, key, value)
        self.session.commit()

    def delete_email_by_user_id_and_email_id(self, user_id, email_id):
        email = self.session.query(Email).filter(
            Email.user_id == user_id).filter(
            Email.email_id == email_id).filter(Email.is_active == True).first()
        email.is_active = False
        self.session.commit()

    def delete_email_by_user_id(self, user_id):
        emails = self.session.query(Email).filter(
            Email.user_id == user_id).filter(Email.is_active == True).all()
        for email in emails:
            email.is_active = False
        self.session.commit()
