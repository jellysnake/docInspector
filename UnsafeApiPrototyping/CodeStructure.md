# Overview

This only pertains to the Unsafe API classes. The other classes used to interact with the api are provided by Google.

The api is broken into two 'layers', _Document_ and _Revisions_. Revisions is then further broken down into both _RevisionMetadata_ and _ChangeData_.

## `Document`

This represents the overall document at large. It mainly contains metadata about the document and the revisions it contains, with the data being contained with the `revisions` classes.
Notably it also contains information about the users

## Revisions
This is the section that contains all the information about specific revisions. The overall information is contained within `Document`.

### `RevisionMetadata`
This contains information about the metadata for each revision. This includes things like who has edited it, it's start and end id's and _apparently_ the end time of the revision.

### `ChangeData`
This contains the direct information about the changes in the revision. This is mainly the number of additions and removals each editor has made.

## Misc Classes
These are classes that don't fit into either of the two major levels above

### `UnsafeRequester`
This class is the one responsible for performing the actual HTTP calls to the api. It simply abstracts away the URL's used, and does nothing more than return the JSON that the request gave.

### `User`
This represents a single user. Each user is identified by the color their edits are shown in. This is because it is the only constant between the higher up `Document` level and the `ChangeData` level.
This color is treated as the user ID and is used to link the user from the changes to the user information provided by the Document level.