def save_fetch_url_log(fetch_url: str, file_name: str = "fetch_url.txt") -> None:
    """
    Writes the given URL to a .txt file.

    Args:
        fetch_url (str): The URL to be written into the file.
    """
    # Open a file named "output.txt" in write mode
    with open(file_name, "w") as file:
        # Write the URL string to the file
        file.write(fetch_url)
