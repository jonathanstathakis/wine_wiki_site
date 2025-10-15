/*
Join left and right wines based on whether the wine text matches then insert the matched wines into the autofillpending table.
* */
-- select id, pub_date from wine_wiki_winelistedition;
-- TODO: finish perculating autofilledition_id through to autofillpending values 
-- so that deletion of autofilleditions clears the autofillpending table too.
begin;


-- create temp table autofillpending_staging as 
with 
    -- get left edition raw wine list fields
    wlr_left as (
    select 
    wlr.id as id,
    wlr.vintage as vintage,
    wlr.prod_wine_name as prod_wine_name,
    wlr.geo_int as geo_int,
    wlr.vol,
    afe.id as autofilledition_id
    from
        wine_wiki_autofilleditions afe
    left join
        wine_wiki_winelistraw wlr
    on
        afe.edition_left_id  = wlr.winelistedition_id

  ), -- get right edition raw wine list fields
    wlr_right as (
    select 
    wlr.id as id,
    wlr.vintage as vintage,
    wlr.prod_wine_name as prod_wine_name,
    wlr.geo_int as geo_int,
    wlr.vol,
    afe.id as autofilledition_id
    from
        wine_wiki_autofilleditions afe
    left join
        wine_wiki_winelistraw wlr
    on
        afe.edition_right_id  = wlr.winelistedition_id),

    -- join left and right editions on raw wine text.
    wlr_joined as (
  select
    l.id as left_id,
    r.id as right_id,
    l.vintage,
    l.prod_wine_name,
    l.geo_int,
    l.vol,
    l.vintage || l.prod_wine_name || l.geo_int || l.vol as left_join_key,
    r.vintage || r.prod_wine_name || r.geo_int || r.vol as right_join_key,
    l.autofilledition_id as autofilledition_id
  from
    wlr_left l
  inner join
    wlr_right r
  on
    l.vintage = r.vintage
  and
    l.prod_wine_name = r.prod_wine_name
  and
    l.geo_int = r.geo_int
  and
    l.vol = r.vol
),
  -- join with winelistdisplay
  with_wine_ids as (
  select
    wlr.left_id as left_wlr_id,
    wlr.right_id as right_wlr_id,
    wlr.left_join_key as left_join_key,
    wlr.right_join_key as right_join_key,
    wld_left.id as wld_id_left,
    wld_right.id as wld_id_right,
    wld_left.wine_id as wine_id_left,
    wld_right.wine_id as wine_id_right,
    wlr.autofilledition_id as autofilledition_id
  from
    wlr_joined wlr
  left join
    wine_wiki_winelistdisplay wld_left
  on
    wlr.left_id = wld_left.winelistraw_id
  left join
    wine_wiki_winelistdisplay wld_right
  on
    wlr.right_id = wld_right.winelistraw_id
  where wine_id_right is not null
),

autofill_pending as (
  select wld_id_left, wld_id_right, wine_id_right as wine_id, autofilledition_id from with_wine_ids)

select 
  count(*)
 from
-- wlr_right
autofill_pending
;

-- select *, count(wine_id) from autofillpending_staging group by wine_id order by count(wine_id) desc;
-- wine_id = 223 duplicated twice.
-- select left and right wine text data where wine_id = 223.
-- select 
-- wld_id_left,
-- l.vintage,
-- l.geo_int,
-- l.prod_wine_name,
-- l.vol,
-- l.section_path,
-- wld_id_right,
-- r.vintage,
-- r.geo_int,
-- r.prod_wine_name,
-- r.vol,
-- r.section_path
--   from autofillpending_staging afps
-- left join
--   wine_wiki_winelistdisplay l
-- on
--   afps.wld_id_left = l.id
-- left join
--   wine_wiki_winelistdisplay r
-- on
--   afps.wld_id_right = r.id
-- where afps.wine_id = 223
-- ;

-- -- insert into autofillpending;
-- insert into wine_wiki_autofillpending (
--   autofilledition_id,
--   wine_list_left_id,
--   wine_list_right_id,
--   wiki_id,
--   review
--   )
--   select
--     autofilledition_id,
--     wld_id_left,
--     wld_id_right,
--     wine_id as wiki_id,
--     true as review
-- from
--     autofillpending_staging;

-- TODO: solve non-unique wine problem. We expect one wine per row, but I think
-- we saw taht several rows had teh same wine.
-- TODO: to solve above, go back to ETL and extract variety then rerun everything to get back here.
rollback;
