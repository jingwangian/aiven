-- create cputimes
create table if not exists cpu_metric (
  machine_id int not null,
  "user" float, 
  nice float, 
  system float, 
  idle float,
  created_at TIMESTAMPTZ not null);

-- create mem_metric
create table if not exists mem_metric(
  machine_id int not null, 
  total bigint, 
  available bigint, 
  percent float, 
  used bigint, 
  free bigint,
  created_at TIMESTAMPTZ not null);

-- create disk_metric
create table if not exists disk_metric(
  time TIMESTAMPTZ default CURRENT_TIMESTAMP,
  machine_id int, 
  total bigint, 
  used bigint, 
  free bigint, 
  percent float,
  created_at TIMESTAMPTZ not null);

