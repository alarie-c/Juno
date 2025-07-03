def read_src(path: str) -> str | None:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
    return None

def main():
    path = 'main.juno'
    src = read_src(path)
    print(src)

if __name__ == '__main__':
    main()