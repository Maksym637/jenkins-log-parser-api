get_headers = lambda hashed_credentials: {
    "Authorization": f"Basic {hashed_credentials}"
}

swapped_in_half = (
    lambda string: f"{string[len(string) // 2 :]}{string[: len(string) // 2]}"
)
