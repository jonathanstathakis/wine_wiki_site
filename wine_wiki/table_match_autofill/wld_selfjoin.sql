/*
Join left and right wines based on whether the wine text matches then insert the matched wines into the autofillpending table.
* */
create temp table autofillpending_staging as 
with 
    -- get left edition raw wine list fields where winelistdisplay not joined to wine
    wlr_left as (
    select 
    wlr.id as id,
    wlr.vintage as vintage,
    wlr.prod_wine_name as prod_wine_name,
    wlr.geo_int as geo_int,
    wlr.vol,
    wlr.varietal,
    afe.id as autofilledition_id
    from
        wine_wiki_autofilleditions afe
    left join
        wine_wiki_winelistraw wlr
    on
        afe.edition_left_id  = wlr.winelistedition_id
    left join
        wine_wiki_winelistdisplay d
    on
        d.winelistraw_id = wlr.id
    where
        d.wine_id is null

  ), -- get right edition raw wine list fields
    wlr_right as (
    select 
    wlr.id as id,
    wlr.vintage as vintage,
    wlr.prod_wine_name as prod_wine_name,
    wlr.geo_int as geo_int,
    wlr.vol,
    wlr.varietal,
    afe.id as autofilledition_id
    from
        wine_wiki_autofilleditions afe
    left join
        wine_wiki_winelistraw wlr
    on
        afe.edition_right_id  = wlr.winelistedition_id
    left join
        wine_wiki_winelistdisplay d
    on
        d.winelistraw_id = wlr.id
    where
        d.wine_id is not null
),

    -- join left and right editions on raw wine text.
    wlr_joined as (
  select
    l.id as left_id,
    r.id as right_id,
    l.vintage,
    l.prod_wine_name,
    l.geo_int,
    l.vol,
    l.vintage || l.prod_wine_name || l.geo_int || l.varietal || l.vol as left_join_key,
    r.vintage || r.prod_wine_name || r.geo_int || l.varietal || r.vol as right_join_key,
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
*
 from
autofill_pending
;

-- insert into autofillpending;
insert into wine_wiki_autofillpending (
  autofilledition_id,
  wine_list_left_id,
  wine_list_right_id,
  wiki_id,
  review
  )
  select
    autofilledition_id,
    wld_id_left,
    wld_id_right,
    wine_id as wiki_id,
    true as review
from
    autofillpending_staging;
