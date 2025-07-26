Create table if not exists college_list (
    id serial primary key,
    name text not null,
    location text not null,
    tier char(1) not null,
    specialization text,
    vector vector(1536) -- Adjust the dimension as needed
);


Create table if not exists company_list (
    id serial primary key,
    name text not null,
    location text not null,
    tier char(1) not null,
    domain_info text,
    sub_domain_info text,
    vector vector(1536) -- Adjust the dimension as needed
);
