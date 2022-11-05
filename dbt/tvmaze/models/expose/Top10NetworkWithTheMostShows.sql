{{
    config(
        materialized='view',
        database='TVSHOW',
        schema='EXPOSE'
    )
}}

select ns.name as Network_Name, count(ts.show_id) as number_of_shows
from {{ ref('episode_staging') }} es
join {{ ref('network_staging') }} ns
    on es.network_id = ns.network_id
join {{ ref('tvshow_staging') }} ts
    on es.show_id = ts.show_id
group by Network_Name
order by number_of_shows desc
limit 10