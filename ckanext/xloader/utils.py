import ckan.plugins as p


def resource_data(id, resource_id):

    if p.toolkit.request.method == "POST":
        try:
            p.toolkit.get_action("xloader_submit")(
                None,
                {
                    "resource_id": resource_id,
                    "ignore_hash": True,  # user clicked the reload button
                },
            )
        except p.toolkit.ValidationError:
            pass

        return p.toolkit.redirect_to(
            "xloader.resource_data", id=id, resource_id=resource_id
        )

    try:
        pkg_dict = p.toolkit.get_action("package_show")(None, {"id": id})
        resource = p.toolkit.get_action("resource_show")(None, {"id": resource_id})
    except (p.toolkit.ObjectNotFound, p.toolkit.NotAuthorized):
        return p.toolkit.abort(404, p.toolkit._("Resource not found"))

    try:
        xloader_status = p.toolkit.get_action("xloader_status")(
            None, {"resource_id": resource_id}
        )
    except p.toolkit.ObjectNotFound:
        xloader_status = {}
    except p.toolkit.NotAuthorized:
        return p.toolkit.abort(403, p.toolkit._("Not authorized to see this page"))

    return p.toolkit.render(
        "xloader/resource_data.html",
        extra_vars={
            "status": xloader_status,
            "resource": resource,
            "pkg_dict": pkg_dict,
        },
    )
