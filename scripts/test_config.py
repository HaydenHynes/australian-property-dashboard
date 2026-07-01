"""
Test the application configuration.
"""

from backend.core.config import PROJECT_ROOT
from backend.core.config import RAW_DATA_DIR

def main() -> None:
  print("Project Root:")
  print(PROJECT_ROOT)
  
  print()
  
  print("Raw Data Directory:")
  print(RAW_DATA_DIR)
  
if __name__ == "__main__":
  main()
  