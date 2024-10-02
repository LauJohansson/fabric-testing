import argparse


def validate_args(args, parser: argparse):
    # Custom validation for client-id and client-secret
    if (args.client_id and not args.client_secret) or (
        args.client_secret and not args.client_id
    ):
        parser.error("Both --client-id and --client-secret must be provided together.")

    if args.service_principal and (not args.client_id or not args.client_secret):
        parser.error(
            "Expecting service principal "
            "but missing either --client-id or --client-secret."
        )
