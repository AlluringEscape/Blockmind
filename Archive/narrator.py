def narrate(message):
    print(message)
    with open("logs/story_log.txt", "a", encoding="utf-8") as f:
        from time import strftime
        f.write(f"[{strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")