select
    w.*,
    p.name as producer_name
from
    wine_wiki_wine w
left join
    wine_wiki_producer p
on
    w.producer_id = p.id;
