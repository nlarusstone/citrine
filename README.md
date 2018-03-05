# APIs
This API can be accessed at https://obscure-beyond-29233.herokuapp.com/
This API allows users to add materials to a database and search through that database.
Materials are specified as "compounds" and information about them is referred to as "properties".
This API is case sensitive.

## Endpoint: /data/add
This endpoint allows a user to add data to our database.
This endpoint only responds to POST requests.
The body of the POST request MUST contain a JSON object that has a "compound" field.
The body may optionally contain a JSON array of "properties".

Here is an example request body:
{
  "compound": "GaN",
  "properties": [
    {
      "propertyName": "Band gap",
      "propertyValue": "3.4"
    }
  ]
}

Note that although this API does not currently allow updating, submitting a compound without any properties will still create that compound in the database.

## Endpoint: /data/search
This endpoint allows a user to search through the database.
As above, this endpoint only responds to POST requests.
However, there are no required fields here.
Any fields other than "compound" or "properties" will be ignored.
If multiple properties are specified or a compound and properties are both specified, then the search will return an OR of all records that satisfy any of the criteria.

Search criteria for compounds:
Requires a JSON object with a logic field (can be "contains" or "eq") and a value field (which is what we're searching for).

Search criteria for properties:
Requires a JSON array where each object has a name field, a value field, and a logic field.
The logic field can be one of "gt", "gte", "lt", "lte", "eq".

Here's an example request body:
{
  "compound": {
    "logic": "contains",
    "value": "Ga"
  },
  "properties": [
    {
      "name": "Band gap",
      "value": "3.4",
      "logic": "gt"
    },
    {
      "name": "Color",
      "value": "White",
      "logic": "eq"
    }
  ]
}

# Future work
This API is incomplete and requires further development in a few areas.
First of all, the API as written only supports create and read operations.
A full implementation would allow updates and deletes (through PATCH and DELETE requests.
Secondly, the API is currently case sensitive to all fields--a future version might want to make only compound names case sensitive, while property names and/or values are case insensitive.
Thirdly, this API does not have any rate limiting, which leaves it open for potential abuse.
Finally, the API is hosted on the free tier of Heroku with a free sandbox instance of MongoDB, neither of which scales very well.
Putting this in production would require more work including potentially adding load balancers and implementing a master-slave database scheme (depending on how many materials we had).
One minor point is that the endpoints do not align very well with REST practices since they are verbs.
Instead, one might change the add end point to /data/materials and allow GET requests to read all of the materials in the database and POST requests to add to the materials.

# Deployment
This API is currently deployed on Heroku and should be accessible at https://obscure-beyond-29233.herokuapp.com/
If you need to deploy it locally, running heroku local web from the root directory should work (assuming heroku cli tools are installed)
