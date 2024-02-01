# API
## Version: 1.0

### /article/{id}

#### GET
##### Description:

Get the details of an article.

##### Parameters

| Name | Located in | Description                                            | Required | Schema |
| ---- | ---------- | ------------------------------------------------------ | -------- | ------ |
| id   | path       | Identifier of the article, ex: oai:arXiv.org:0912.0228 | Yes      | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200  | Success     |

### /authors

#### GET
##### Description:

List all of the authors present in the database.

##### Responses

| Code | Description |
| ---- | ----------- |
| 200  | Success     |

### /records

#### POST
##### Description:

Adds a new record to the database. The record must be provided as an XML string in the OAI-PHM type in the request body.

##### Parameters

| Name    | Located in | Description | Required | Schema            |
| ------- | ---------- | ----------- | -------- | ----------------- |
| payload | body       |             | Yes      | [Record](#Record) |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200  | Success     |

#### GET
##### Description:

Fetches a list of records from the database. The records can be filtered by limit, category, author, and date.

##### Parameters

| Name     | Located in | Description                          | Required | Schema  |
| -------- | ---------- | ------------------------------------ | -------- | ------- |
| limit    | query      | Limit the number of records returned | No       | integer |
| category | query      | Category of the records to return    | No       | string  |
| author   | query      | Author of the records to return      | No       | string  |
| date     | query      | Date of the records to return        | No       | string  |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200  | Success     |

### /summary/{id}

#### GET
##### Description:

Fetches the summary of the article with the given identifier.

##### Parameters

| Name | Located in | Description                                            | Required | Schema |
| ---- | ---------- | ------------------------------------------------------ | -------- | ------ |
| id   | path       | Identifier of the article, ex: oai:arXiv.org:0912.0228 | Yes      | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200  | Success     |

### Models


#### Record

| Name | Type   | Description                              | Required |
| ---- | ------ | ---------------------------------------- | -------- |
| xml  | string | The XML string of the record to be added | Yes      |