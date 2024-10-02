import argparse


def validate_args(args, parser: argparse):
    # Use getattr to safely access attributes with a default value of None
    client_id = getattr(args, "client_id", None)
    client_secret = getattr(args, "client_secret", None)

    # Custom validation for client-id and client-secret
    if (client_id and not client_secret) or (client_secret and not client_id):
        parser.error("Both --client-id and --client-secret must be provided together.")

    if getattr(args, "service_principal", False) and (
        not client_id or not client_secret
    ):
        parser.error(
            "Expecting service principal but missing "
            "either --client-id or --client-secret."
        )
