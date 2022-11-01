drop database if exists user_contacts;
create database user_contacts;

drop table if exists user_contacts.UserContacts;
create table user_contacts.UserContacts
(
    user_id            int     not null,
    is_active          boolean not null,
    primary_email_id   int     null,
    primary_phone_id   int     null,
    primary_address_id int     null,
    constraint UserContacts_pk
        primary key (user_id)
);

drop table if exists user_contacts.email;
create table user_contacts.email
(
    user_id       int                                 not null,
    email_id      int                                 not null auto_increment,
    is_active     boolean                             not null,
    email_type    enum ('Personal', 'School', 'Work') not null,
    email_address varchar(255)                        not null,
    constraint email_pk
        primary key (email_id),
    constraint email_usercontacts_null_fk
        foreign key (user_id) references user_contacts.usercontacts (user_id)
);

drop table if exists user_contacts.phone;
create table user_contacts.phone
(
    user_id      int                             not null,
    phone_id     int                             not null auto_increment,
    is_active    boolean                         not null,
    phone_type   enum ('Home', 'Work', 'Mobile') not null,
    phone_number varchar(31)                     not null,
    primary key (phone_id),
    constraint phone_usercontacts_null_fk
        foreign key (user_id) references user_contacts.usercontacts (user_id)
);

drop table if exists user_contacts.address;
create table user_contacts.address
(
    user_id       int                                          not null,
    address_id    int                                          not null auto_increment,
    is_active     boolean                                      not null,
    address_type  enum ('Permanent', 'Temporary', 'Mail-only') not null,
    address_line1 varchar(255)                                 not null,
    address_line2 varchar(255)                                 null,
    city          varchar(255)                                 not null,
    state         varchar(63)                                  not null,
    zip           varchar(15)                                  not null,
    primary key (address_id),
    constraint address_usercontacts_null_fk
        foreign key (user_id) references user_contacts.usercontacts (user_id)
);

alter table user_contacts.usercontacts
    add constraint usercontacts_address_null_null_fk
        foreign key (user_id, primary_address_id) references user_contacts.address (user_id, address_id);

alter table user_contacts.usercontacts
    add constraint usercontacts_email_null_null_fk
        foreign key (user_id, primary_email_id) references user_contacts.email (user_id, email_id);

alter table user_contacts.usercontacts
    add constraint usercontacts_phone_null_null_fk
        foreign key (user_id, primary_phone_id) references user_contacts.phone (user_id, phone_id);

