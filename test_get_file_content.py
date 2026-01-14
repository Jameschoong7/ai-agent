from functions.get_file_content import get_file_content


def test():
    print(get_file_content("calculator","main.py"))
    print(get_file_content("calculator","pkg/calculator.py"))
    print(get_file_content("calculator","/bin/cat"))
    print(get_file_content("calculator","pkg/does_not_exist.py"))
    print(get_file_content("calculator","/bin"))


 
if __name__ == "__main__":
    test()