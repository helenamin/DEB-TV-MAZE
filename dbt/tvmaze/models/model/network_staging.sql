{{
    config(
        materialized='table',
        database='TVSHOW',
        schema='MODEL'
    )
}}

SELECT
    DISTINCT(CAST(tmsn.ID AS INTEGER)) AS Network_ID,
    tmsn.name,
    tmsn.officialsite AS Network_Website
FROM {{ source('TVSHOW', 'TV_MAZE_SHOW_NETWORK') }} tmsn
WHERE tmsn.ID IS NOT NULL