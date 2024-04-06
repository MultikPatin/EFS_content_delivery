from fastapi import Query

search_query_validators = Query(
    alias="query",
    title="Search query",
    description="The query to search",
)
