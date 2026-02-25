from app.db import init_db
from app.pipeline import run_pipeline

def main():
    init_db()
    result = run_pipeline()
    print(result)

if __name__ == "__main__":
    main()