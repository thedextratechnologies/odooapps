def post_init_hook(env):
    """Assign account numbers to existing eligible companies."""

    partners = (
        env["res.partner"]
        .sudo()
        .with_context(active_test=False)
        .search([
            ("is_company", "=", True),
        ])
    )

    # Check the non-stored credit-limit field in Python,
    # not in the database search domain.
    partners._assign_account_number_if_eligible()
