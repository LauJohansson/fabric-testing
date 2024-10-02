def load_fetch_url(file_name: str = "fetch_url.txt") -> str:
    """
    Reads the URL from a .txt file and returns it.

    Returns:
        str: The URL stored in the file.
    """
    # Open the file in read mode
    with open(file_name, "r") as file:
        # Read the contents of the file and return it
        fetch_url = file.read().strip()
    return fetch_url
