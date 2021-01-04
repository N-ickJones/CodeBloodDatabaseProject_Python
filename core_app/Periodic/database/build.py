import sys
from core_app.Periodic.database.tables import Tables
# from core_app.Periodic.database.fill import TableFill


def main(argv):
    Tables()
    # TableFill()


if __name__ == "__main__":
    main(sys.argv)
