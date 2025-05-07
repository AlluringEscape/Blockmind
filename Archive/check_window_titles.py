import pygetwindow as gw

def list_all_windows():
    titles = gw.getAllTitles()
    print("\n🪟 All Window Titles Detected:")
    for title in titles:
        if title.strip():
            print(f" - {title}")

if __name__ == "__main__":
    list_all_windows()
