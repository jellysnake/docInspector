from DocInspector.DocStats import DocStats


def collectIndividualStats(stats: DocStats, service):
    """
    Loads stats for individual contributions out of the official api.
    This at present only includes an incomplete list of editors

    :param stats: The stat object to insert data into
    :param service: The google drive v2 service.
    :param args: The program arguments. See `docInspector.py#parseArguments` for description of arguments
    """
    # Call the data from the api
    rev_meta = service.revisions().list(fileId=stats.general.id).execute()

    # Collect all editors, excluding duplicates
    editors = set()
    for revision in rev_meta["items"]:
        if "lastModifyingUserName" in revision:
            editor = revision["lastModifyingUserName"]
            editors.add(editor)

    # Insert editors
    for editor in editors:
        stats.individuals.makeEditor(editor).name = editor
