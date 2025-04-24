from backend.core.alias_resolver import resolve_canonical_name
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m cli.scripts.test_alias_resolver '<venue name>' [--verbose]")
        sys.exit(1)

    input_name = sys.argv[1]
    verbose = "--verbose" in sys.argv

    result = resolve_canonical_name(input_name, verbose=verbose)
    # print(f"\n🧪 Resolved '{input_name}' → {result}")