{{
    config(
        materialized='view',
        database='TVSHOW',
        schema='EXPOSE'
    )
}}

select ns.name as Network_Name,
       Avg(
           Case When ts.rating is null then 0
                Else ts.rating
           end
       ) as Avg_Rating
from {{ ref('episode_staging') }} es
join {{ ref('network_staging') }}  ns
    on es.network_id = ns.network_id
join {{ ref('tvshow_staging') }} ts
    on es.show_id = ts.show_id
group by Network_Name
order by Avg_Rating desc
limit 10