from archydra.Filters import Selector
from archydra.Producers import FileProducer
from pathlib import Path
if __name__ == "__main__":
    fp = FileProducer(Path("./tests/test_urls.txt"))
    s = Selector([fp])
    for i in s.get_urls():
        print(i)