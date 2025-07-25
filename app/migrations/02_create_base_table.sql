CREATE table if not exists base_table
(
    id serial primary key,
    name text not null,
    doc text,
    description text,
    vector vector(1536) -- Adjust the dimension as needed
);