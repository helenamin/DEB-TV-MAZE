{{
    config(
        materialized='table',
        database='TVSHOW',
        schema='MODEL'
    )
}}

SELECT
    DISTINCT(CAST(tms.id AS INTEGER)) AS Show_ID,
    tms.url,
    tms.name AS Show_Name,
    tms.type AS Show_Type,
    CAST(tms.ended AS DATE) AS End_Date,
    CASE
        WHEN tms.genres = '[]' THEN null
        ELSE REPLACE(REPLACE(REPLACE(REPLACE(tms.genres,'[','' ),']',''),'"',''),',',' | ')
    END AS genres,
    -- {{ clean_string_list('tms.genres') }} as Genres1,
    CAST(tmsr.average AS DOUBLE) AS Rating,
    tms.status,
    CAST(tms.runtime AS INTEGER) AS Runtime_In_Min,
    CAST(DATEADD(s, tms.updated, '1970-01-01') AS DATE) AS Updated,
    tms.language,
    CASE
        WHEN tmss.days = '[]' THEN null
        ELSE REPLACE(REPLACE(REPLACE(REPLACE(tmss.days,'[','' ),']',''),'"',''),',',' | ')
    END AS Show_Days ,
    tmss.time AS Show_Time,
    TO_DATE(tms.premiered,'YYYY-mm-dd') AS Premiered,
    tms.officialsite AS Show_Website,
    CAST(tms.averageruntime AS INTEGER) AS Avg_Runtime_In_Min
FROM {{ source('TVSHOW', 'TV_MAZE_SHOW') }} tms
JOIN {{ source('TVSHOW', 'TV_MAZE_SHOW_RATING') }} tmsr
    ON tms._airbyte_show_hashid = tmsr._airbyte_show_hashid
JOIN {{ source('TVSHOW', 'TV_MAZE_SHOW_SCHEDULE') }} tmss
    ON tms._airbyte_show_hashid = tmss._airbyte_show_hashid