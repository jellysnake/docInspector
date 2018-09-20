from DocStats import DocStats
from DocumentEditors import findAndPrintEditors
from ModifyDateRange import getDatesModifiedWithin


def collectIndividualStats(stats: DocStats, service, args):
    # Print Document Editors
    rev_meta = service.revisions().list(fileId=stats.general.id).execute()
    editors = set()
    for revision in rev_meta["items"]:
        edits = revision["lastModifyingUserName"]
        editors.add(edits)
    for editor in editors:
        stats.individuals.makeEditor(editor)

    print(editors)
