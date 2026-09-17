from migrations import run_pending


if __name__ == "__main__":
    applied = run_pending()
    print("Applied: " + (", ".join(applied) if applied else "none"))
