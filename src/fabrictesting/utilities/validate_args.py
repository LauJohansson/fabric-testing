import argparse


def validate_args(args, parser: argparse):
    """
    Validates command-line arguments for the fabric-testing CLI commands.

    This function performs custom validation to ensure that certain
    argument combinations are provided correctly.
    Specifically, it checks the following conditions:

    1. If either `--client-id` or `--client-secret` is provided, both must be present.
    2. If `--service-principal` is set to `True`,
        both `--client-id` and `--client-secret` must be provided together.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        parser (argparse.ArgumentParser): The argument parser instance used
                                        to display error messages.

    Raises:
        SystemExit: If validation fails, `parser.error()` is called,
        which raises a `SystemExit` exception to halt execution
        and display an error message.

    """
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
