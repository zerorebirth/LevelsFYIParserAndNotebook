def pytest_addoption(parser):
    parser.addoption("--s", action="store", default="default name")
    parser.addoption("--max_offset", action="store", default="default name")
